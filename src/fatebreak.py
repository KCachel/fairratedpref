import numpy as np
import pandas as pd
import src as src
from itertools import zip_longest


def fairbreak(rating_df, item_col, rating_col, item_group_dict, rand_seed):
    #ranking_df, scores_df = src.avg_rating(rating_df, item_col, rating_col, rand_seed)
    ranking_np, scores_np = src.simulate_worst_case(rating_df, item_col, rating_col, item_group_dict, rand_seed)


    fair_ranking_list = []
    #loop through tied chunks
    for tied_score in pd.unique(scores_np): #pandas unique preserves order

        #get candidates that are tied
        tied_items_list = list(ranking_np[scores_np == tied_score])
        tied_groups_list = [item_group_dict[i] for i in tied_items_list]

        #if items belong to > 1 group we need to fair break the ranks
        if len(np.unique(tied_groups_list)) > 1:
            name, cnt = np.unique(tied_groups_list, return_counts=True) #need to get a list of lists, since num groups unknown
            name, cnt = zip(*sorted(zip(name, cnt), key=lambda x: x[0], reverse=True)) #order groups largest to smallest
            nested_grp_lists = [np.tile(name[i],cnt[i]).tolist() for i in range(0, len(cnt))]
            interleaved_groups = [x for t in zip_longest(*nested_grp_lists) for x in t if x is not None] #Implementation wise it's faster to interleave groups, than adjust their scores
            new_order = src.reorder_candidates(tied_groups_list, tied_items_list, interleaved_groups)
            fair_ranking_list = fair_ranking_list + new_order
        else:
            fair_ranking_list = fair_ranking_list + tied_items_list #no need to break since 1 item or same group

    return pd.DataFrame(fair_ranking_list), pd.DataFrame(scores_np)



