import src as src
import numpy as np
import pandas as pd

def worst_case_break(rating_df, item_col, rating_col, item_group_dict, rand_seed):
    # ranking_df, scores_df = src.avg_rating(rating_df, item_col, rating_col, rand_seed)
    #
    # ranking_list = []
    # # loop through tied chunks
    # for tied_score in scores_df.unique():
    #
    #     # get candidates that are tied
    #     tied_items_list = ranking_df[scores_df == tied_score].to_list()
    #     tied_groups_list = [item_group_dict[i] for i in tied_items_list]
    #
    #     # if items belong to > 1 group we need to fair break the ranks
    #     if len(np.unique(tied_groups_list)) > 1:
    #         name, cnt = np.unique(tied_groups_list,
    #                               return_counts=True)  # need to get a list of lists, since num groups unknown
    #         name, cnt = zip(
    #             *sorted(zip(name, cnt), key=lambda x: x[0], reverse=True))  # order groups largest to smallest
    #         nested_grps = [np.tile(name[i], cnt[i]).tolist() for i in range(0, len(cnt))]
    #         flat_descending_groups =  list(chain.from_iterable(nested_grps))
    #         new_order = src.reorder_candidates(tied_groups_list, tied_items_list, flat_descending_groups)
    #         ranking_list = ranking_list + new_order
    #     else:
    #         ranking_list = ranking_list + tied_items_list  # no need to break since 1 item or same group

    ranking, scores = src.simulate_worst_case(rating_df, item_col, rating_col, item_group_dict, rand_seed)
    return pd.DataFrame(ranking), pd.DataFrame(scores)