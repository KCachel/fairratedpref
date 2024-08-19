import numpy as np
import pandas as pd
import copy
import src as src

# References: Feng, Y., & Shah, C. (2022, June).
# Has CEO gender bias really been fixed? adversarial attacking and improving gender fairness in image search.
# In Proceedings of the AAAI Conference on Artificial Intelligence (Vol. 36, No. 11, pp. 11882-11890).

def _epsilon_greedy(current_ranking, epsilon, seed):
    """
    Epsilon-Greedy reranking algorithm.
    :param current_ranking: List to be reranked.
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :param current_ranking_scores: List of scores associated with each item in the ranking.
    :param epsilon: Float epsilon value in [0,1].
    :param seed: Random seed value for reproducibility.
    :return: reranking, Pandas dataframe of items,item_group_reranked_dict, dictionary of items and group membership,  Pandas dataframe  of scores for reranking,
    """


    curr_ranking = copy.deepcopy(current_ranking)
    np.random.seed(seed)  # for reproducibility
    reranking = []
    for i in range(len(curr_ranking)):
        p = np.random.rand()
        if (
            p <= epsilon and i < len(curr_ranking) - 1
        ):  # swap items & can't swap last item
            temp = curr_ranking[i]
            j = np.random.randint(i + 1, len(curr_ranking))
            curr_ranking[i] = curr_ranking[j]
            curr_ranking[j] = temp
            reranking.append(curr_ranking[i])
        else:  # keep original ranking
            reranking.append(curr_ranking[i])

    return reranking

def epsilon_greedy_break(rating_df, item_col, rating_col, item_group_dict, epsilon, rand_seed):
    """
    Baseline from Feng et al. AAAI'22, applied to tied bucket orders
    :param rating_df:
    :param item_col:
    :param rating_col:
    :param item_group_dict:
    :param epsilon:
    :param rand_seed:
    :return:
    """
    # Uncomment to process the random break method
    # ranking_df, scores_df = src.avg_rating(rating_df, item_col, rating_col, rand_seed)
    # ranking_np = ranking_df.to_numpy()
    # scores_np = scores_df.to_numpy()
    ranking_np, scores_np = src.simulate_worst_case(rating_df, item_col, rating_col, item_group_dict, rand_seed)

    fair_ranking_list = []
    # loop through tied chunks
    for tied_score in pd.unique(scores_np):  # pandas unique preserves order

        # get candidates that are tied
        tied_items_list = list(ranking_np[scores_np == tied_score])
        tied_groups_list = [item_group_dict[i] for i in tied_items_list]

        # if items belong to > 1 group we need to fair break the ranks
        if len(np.unique(tied_groups_list)) > 1:
            new_order = _epsilon_greedy(tied_items_list, epsilon, rand_seed)
            fair_ranking_list = fair_ranking_list + new_order
        else:
            fair_ranking_list = fair_ranking_list + tied_items_list  # no need to break since 1 item or same group

    return pd.DataFrame(fair_ranking_list), pd.DataFrame(scores_np)

def epsilon_greedy_full(rating_df, item_col, rating_col, item_group_dict, epsilon, rand_seed):
    """
    Baseline from Feng et al. AAAI'22, applied to full ranking
    :param rating_df:
    :param item_col:
    :param rating_col:
    :param item_group_dict:
    :param epsilon:
    :param rand_seed:
    :return:
    """
    # Uncomment to process the random break method
    # ranking_df, scores_df = src.avg_rating(rating_df, item_col, rating_col, rand_seed)
    # ranking_np = ranking_df.to_numpy()
    # scores_np = scores_df.to_numpy()
    ranking_np, scores_np = src.simulate_worst_case(rating_df, item_col, rating_col, item_group_dict, rand_seed)
    original_items = list(ranking_np)
    original_scores = list(scores_np)

    new_order = _epsilon_greedy(original_items, epsilon, rand_seed)
    new_scores = [original_scores[original_items.index(i)] for i in new_order]


    return pd.DataFrame(new_order), pd.DataFrame(new_scores)