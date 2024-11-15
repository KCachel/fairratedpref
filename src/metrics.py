# Script for metrics
# References: Geyik, S. C., Ambler, S., & Kenthapadi, K. (2019, July).
# Fairness-aware ranking in search & recommendation systems with application to linkedin talent search.
# In Proceedings of the 25th acm sigkdd international conference on knowledge discovery & datasets mining (pp. 2221-2231).



# NOTE THAT THE ARUL METRIC IN THE PAPER IS CALLED WUTILITY_LOSS HERE

import numpy as np
import pandas as pd
from sklearn.metrics import jaccard_score

def utility_loss(target_item_df, target_score_df, evaluate_item_df):
    """

    :param target_item_df: Target ordering dataframe
    :param target_score_df:  Target order scores dataframe
    :param evaluate_item_df: Ranking to evaluate against the target (also a dataframe)
    :return:
    """
    numerator = 0
    # loop through tied chunks
    target_np = target_item_df.iloc[:,0].to_numpy()
    target_score_np = target_score_df.iloc[:, 0].to_numpy()
    evaluate_np = evaluate_item_df.iloc[:, 0].to_numpy()
    for tied_score in np.unique(target_score_np):
        #compare items in bucket
        target_bucket = target_np[target_score_np == tied_score]
        eval_bucket = evaluate_np[target_score_np == tied_score]
        numerator += len(np.intersect1d(target_bucket, eval_bucket))/len(target_bucket)


    utility_loss_val = 1 - (numerator/ len(np.unique(target_score_np)))
    return utility_loss_val


def wutility_loss(target_item_df, target_score_df, evaluate_item_df):
    """
    Note this is called ARUL (average rating utility loss) in the paper
    :param target_item_df: Target ordering dataframe
    :param target_score_df:  Target order scores dataframe
    :param evaluate_item_df: Ranking to evaluate against the target (also a dataframe)
    :return:
    """
    numerator = []
    # loop through tied chunks
    target_np = target_item_df.iloc[:,0].to_numpy()
    target_score_np = target_score_df.iloc[:, 0].to_numpy()
    evaluate_np = evaluate_item_df.iloc[:, 0].to_numpy()
    unique_scores, count_uni_scores = np.unique(target_score_np, return_counts = True)
    for tied_score in unique_scores:
        #compare items in bucket
        target_bucket = target_np[target_score_np == tied_score]
        eval_bucket = evaluate_np[target_score_np == tied_score]
        numerator.append(len(np.intersect1d(target_bucket, eval_bucket))/len(target_bucket))

    weights =  count_uni_scores/len(target_np)
    utility = np.sum(np.asarray(numerator) * weights)
    utility_loss_val = 1 - utility
    return utility_loss_val



def NDKL(ranking_df, item_group_dict, fair_rep):
    """
    Calculate Normalized Discounted KL-Divergence Score (Geyik et al.) where chunks are num group increments.
    :param ranking_df: Pandas dataframe of ranking(s).
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :param fair_rep EQUAL or PROPORTIONAL
    :return: NDKL value.
    """
    if len(ranking_df.columns) > 1:
        raise AssertionError("NDKL can only be calculated on a single ranking.")

    single_ranking = ranking_df[ranking_df.columns[0]]  # isolate ranking
    single_ranking = np.array(
        single_ranking[~pd.isnull(single_ranking)]
    )  # drop any NaNs

    group_ids = [item_group_dict[c] for c in single_ranking]
    unique_grps = np.unique(list(item_group_dict.values()))
    group_ids = np.asarray(
        [np.argwhere(unique_grps == grp_of_item)[0, 0] for grp_of_item in group_ids]
    )
    all_groups = np.asarray(list(item_group_dict.values()))
    all_group_ids = np.asarray(
        [np.argwhere(unique_grps == grp_of_item)[0, 0] for grp_of_item in all_groups]
    )
    num_groups = len(unique_grps)
    num_items = len(single_ranking)

    if fair_rep == 'PROPORTIONAL':
        #dr = __distributions(group_ids, num_groups)  # Distributions per group
        dr = __distributions(all_group_ids, num_groups)  # Distributions per group
    if fair_rep == 'EQUAL':
        dr = np.tile((1/(num_groups)), num_groups) #for more equal chunks
      # Array of Z scores

    chunks = list(range(num_groups, num_items + num_groups,num_groups))
    Z = __Z_Vector(len(chunks))
    vals = []
    for ind in range(0, len(list(range(num_groups, num_items+ num_groups,num_groups)))):
        end_prefix = chunks[ind]
        P = __distributions(group_ids[0 : end_prefix], num_groups)
        kl = __kl_divergence(P, dr)
        vals.append(Z[ind]*kl)
    result = (1 / np.sum(Z)) * np.sum(vals)
    return result

def NDKL_allpos(ranking_df, item_group_dict, fair_rep):
    """
    Calculate Normalized Discounted KL-Divergence Score (Geyik et al.).
    :param ranking_df: Pandas dataframe of ranking(s).
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :return: NDKL value.
    """
    if len(ranking_df.columns) > 1:
        raise AssertionError("NDKL can only be calculated on a single ranking.")

    single_ranking = ranking_df[ranking_df.columns[0]]  # isolate ranking
    single_ranking = np.array(
        single_ranking[~pd.isnull(single_ranking)]
    )  # drop any NaNs

    group_ids = [item_group_dict[c] for c in single_ranking]
    unique_grps = np.unique(list(item_group_dict.values()))
    group_ids = np.asarray(
        [np.argwhere(unique_grps == grp_of_item)[0, 0] for grp_of_item in group_ids]
    )
    all_groups = np.asarray(list(item_group_dict.values()))
    all_group_ids = np.asarray(
        [np.argwhere(unique_grps == grp_of_item)[0, 0] for grp_of_item in all_groups]
    )
    num_groups = len(unique_grps)
    num_items = len(single_ranking)

    if fair_rep == 'PROPORTIONAL':
        #dr = __distributions(group_ids, num_groups)  # Distributions per group
        dr = __distributions(all_group_ids, num_groups)  # Distributions per group
    if fair_rep == 'EQUAL':
        dr = np.tile((1/(num_groups)), num_groups) #for more equal chunks
    Z = __Z_Vector(num_items)  # Array of Z scores

    #Eq. 4 in Geyik et al.
    return (1 / np.sum(Z)) * np.sum(
        [
            Z[i]
            * __kl_divergence(__distributions(group_ids[0 : i + 1], num_groups), dr)
            for i in range(0, num_items)
        ]
    )

def __kl_divergence(p, q):
    """
    Calculate KL-Divergence between P and Q, with epsilon to avoid divide by zero.
    :param p: Numpy array p distribution.
    :param q: Numpy array q distribution.
    :return: KL-Divergence score.
    """
    epsilon = 0.0000001  # Epsilon is used here to avoid P or Q is equal to 0. "
    p = p + epsilon
    q = q + epsilon

    return np.sum(p * np.log(p / q))

def __distributions(ranking, num_groups):
    """
    Calculate the proportion of each group
    :param ranking: Numpy array of group id represented in the ranking.
    :param num_groups: Int, number of distinct groups
    :return: Numpy array of each group's proportion.
    """
    return np.array(
        [((ranking == i).sum()) / len(ranking) for i in range(0, num_groups)]
    )


def __Z_Vector(k):
    """
    Calculate Z score
    :param k: Int, position of ranking.
    :return: Numpy array of Z values.
    """
    return 1 / np.log2(np.array(range(0, k)) + 2)

def group_fair_rating(rating_df, item_col, rating_col, group_col, unique_real_ratings, unique_groups):

    #unique_real_ratings = np.unique(rating_df[rating_col])
    num_rating_vals = len(unique_real_ratings)
    int_ratings = np.asarray(list(range(0, num_rating_vals))) + 1
    map_real_2_int = dict(zip(unique_real_ratings, int_ratings))

    scores = np.unique(rating_df[rating_col])
    kl_div_scores = []
    num_groups = len(unique_groups)

    dr = np.tile((1 / (num_groups)), num_groups)  # for more equal chunks
    observed_score_list = rating_df[rating_col].to_list()
    for score in unique_real_ratings:
        if score in observed_score_list:
            sub_df = rating_df[rating_df[rating_col] == score]
            group_ranking = sub_df[group_col].to_numpy()
            P = np.array([((group_ranking == i).sum()) / len(group_ranking) for i in unique_groups])
            kl_div_scores.append(__kl_divergence(P, dr))
        else:
            kl_div_scores.append(np.nan)
    weight_fairness = [kl_div_scores[i]*((1/num_rating_vals)*(num_rating_vals - (map_real_2_int[unique_real_ratings[i]] - 1))) for i in range(0, num_rating_vals)]
    gfr = np.nansum(weight_fairness)
    return gfr



