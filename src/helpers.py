import numpy as np
import src as src
from itertools import chain
import pandas as pd
def avg_rating(rating_df, item_col, rating_col, rand_seed):
    """
    Function to create the consensus ranking by taking the average rating and breaking ties randomly
    :param rating_df: Rating datasets
    :param item_col: Column name of item IDs
    :param rating_col: Column name of ratings
    :return:
    """
    # Get average scores
    #avg_scores_df = rating_df[[item_col, rating_col]].groupby(by=item_col, dropna=False).mean().round(0).reset_index()
    avg_scores_df = rating_df[[item_col, rating_col]].groupby(by=item_col, dropna=False).mean().reset_index()

    # Shuffle the rows before sorting to randomly break ties
    avg_scores_df = avg_scores_df.sample(frac=1, random_state = rand_seed).reset_index(drop=True)
    final_df = avg_scores_df.sort_values(by=[rating_col], ascending=False)
    ranking = final_df[item_col]
    scores = final_df[rating_col]
    return ranking, scores

def reorder_candidates(tied_groups_list, tied_items_list, target_groups):
    """
    Function to create a list of items based on target group identities
    :param tied_groups_list: Groups of it tied_items_list
    :param tied_items_list: IDs of items
    :param target_groups: Desired group order of items
    :return: List of items
    """
    new_order_list = []
    for grp_name in target_groups:
        indx = tied_groups_list.index(grp_name)
        new_order_list.append(tied_items_list[indx])
        del tied_items_list[indx]
        del tied_groups_list[indx]
    return new_order_list

def simulate_worst_case(rating_df, item_col, rating_col, item_group_dict, rand_seed):
    ranking_df, scores_df = src.avg_rating(rating_df, item_col, rating_col, rand_seed)

    ranking_list = []
    # loop through tied chunks
    for tied_score in scores_df.unique():

        # get candidates that are tied
        tied_items_list = ranking_df[scores_df == tied_score].to_list()
        tied_groups_list = [item_group_dict[i] for i in tied_items_list]

        # if items belong to > 1 group we need to do something
        if len(np.unique(tied_groups_list)) > 1:
            name, cnt = np.unique(tied_groups_list,
                                  return_counts=True)  # need to get a list of lists
            cnt, name = zip(*sorted(zip(cnt, name), key=lambda x: x[0], reverse=True))  # order groups largest to smallest
            #if equal number from each group in this tie block then prioritize the group that has the most candidates above
            if len(np.unique(cnt)) == 1 and len(ranking_list) > 0:
                g = [item_group_dict[i] for i in ranking_list]
                u, g_cnt = np.unique(g, return_counts=True)
                if len(u) == len(np.unique(g_cnt)): #groups do not have the same amount before
                    biggest_prior_group = u[g_cnt == np.max(g_cnt)][0]
                    name = list(name)
                    cnt = list(cnt)
                    big_cnt = cnt[name.index(biggest_prior_group)]
                    cnt.pop(name.index(biggest_prior_group)) #delete big group from cnt
                    name.remove(biggest_prior_group)  # delete big group from name
                    name.insert(0, biggest_prior_group) #add big group to name
                    cnt.insert(0, big_cnt) #add big group to cnt

            nested_grps = [np.tile(name[i], cnt[i]).tolist() for i in range(0, len(cnt))]
            flat_descending_groups = list(chain.from_iterable(nested_grps))
            new_order = src.reorder_candidates(tied_groups_list, tied_items_list, flat_descending_groups)
            ranking_list = ranking_list + new_order
        else:
            ranking_list = ranking_list + tied_items_list  # no need to break since 1 item or same group

    return np.asarray(ranking_list), scores_df.to_numpy()