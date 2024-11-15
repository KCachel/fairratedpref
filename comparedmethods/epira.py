import numpy as np
import src as src
import pandas as pd
import comparedmethods as cm
from tqdm import tqdm
#References: https://github.com/KCachel/Fairer-Together-Mitigating-Disparate-Exposure-in-Kemeny-Aggregation/blob/main/src/epira.py
def calc_exposure_ratio(ranking, group_ids):

    unique_grps, grp_count_items = np.unique(group_ids, return_counts=True)
    num_items = len(ranking)
    exp_vals = exp_at_position_array(num_items)
    grp_exposures = np.zeros_like(unique_grps, dtype=np.float64)
    for i in range(0,num_items):
        grp_of_item = group_ids[i]
        exp_of_item = exp_vals[i]
        #update total group exp
        grp_exposures[grp_of_item] += exp_of_item

    avg_exp_grp = grp_exposures / grp_count_items
    #expdp = np.max(avg_exp_grp) - np.min(avg_exp_grp)
    expdpp = np.min(avg_exp_grp)/np.max(avg_exp_grp) #ratio based
    #print("un-normalized expdp: ", expdp)
    #norm_result = expdp / normalizer
    return expdpp, avg_exp_grp

def exp_at_position_array(num_items):
    return np.array([(1/(np.log2(i+1))) for i in range(1,num_items+1)])

def epiRA(consensus, item_group_dict, bnd, grporder):
   """
   Function to perform fair exposure rank aggregation via post-processing a voting rule.
   :param consensus: list of candidates.
   :param item_group_dict: Dictionary where candidates are keys and values are their groups
   :param bnd: Desired minimum exposure ratio of consensus ranking
   :param grporder: True - re orders consensus ranking to preserve within group order. False does not preserve within group order.
   :return: consensus: A numpy array of item ides representing the consensus ranking. ranking_group_ids: a numy array of
    group ids corresponding to the group membership of each item in the consensus.
   """
   num_items = len(consensus)
   consensus_group_ids = np.asarray([item_group_dict[c] for c in consensus])
   current_ranking = np.asarray(consensus)
   current_group_ids = np.asarray(consensus_group_ids)
   unique_grp_strings = list(np.unique(current_group_ids))
   # Their code wants groups to be represented by ints
   consensus_group_ids = [unique_grp_strings.index(v) for v in consensus_group_ids]
   current_group_ids = [unique_grp_strings.index(v) for v in current_group_ids]
   cur_exp, avg_exps = calc_exposure_ratio(current_ranking, current_group_ids)
   exp_at_position = np.array([(1 / (np.log2(i + 1))) for i in range(1, num_items + 1)])
   repositions = 0
   swapped = np.full(len(current_ranking), False) #hold items that have been swapped
   while(cur_exp < bnd ):

       # Prevent infinite loops
       if repositions > ((num_items * (num_items - 1)) / 2):
           print("Try decreasing the bound. If you notice the same pairs of items are being swapped back and forth you can try uncommenting lines with same items swapped.")
           return current_ranking.tolist()
           break

       max_avg_exp = np.max(avg_exps)
       grp_min_avg_exp = np.argmin(avg_exps) #group id of group with lowest avg exposure
       grp_max_avg_exp = np.argmax(avg_exps)  # group id of group with lowest avg exposure
       grp_min_size = np.sum(consensus_group_ids == grp_min_avg_exp)
       Gmin_positions = np.argwhere(current_group_ids == grp_min_avg_exp).flatten()
       Gmax_positions = np.argwhere(current_group_ids == grp_max_avg_exp).flatten()

       indx_highest_grp_min_item = np.min(Gmin_positions)
       valid_Gmax_items = Gmax_positions < indx_highest_grp_min_item

       if np.sum(valid_Gmax_items) == 0:
           Gmin_counter = 1
           while np.sum(valid_Gmax_items) == 0:
               next_highest_ranked_Gmin = np.min(Gmin_positions[Gmin_counter:, ])
               valid_Gmax_items = Gmax_positions < next_highest_ranked_Gmin
               Gmin_counter += 1
           indx_highest_grp_min_item = next_highest_ranked_Gmin
       if swapped[indx_highest_grp_min_item] == True: #swapping same item
           #valid_grp_min = np.argwhere(~swapped & current_group_ids == grp_min_avg_exp).flatten()
           valid_grp_min = np.intersect1d(np.argwhere(~swapped).flatten(),np.argwhere(current_group_ids == grp_min_avg_exp).flatten())
           if len(valid_grp_min) != 0: indx_highest_grp_min_item = np.min(valid_grp_min)  # index of highest ranked item that was not swapped
       highest_item_exp = exp_at_position[indx_highest_grp_min_item]
       exp_grp_min_without_highest = (np.min(avg_exps) * grp_min_size) - highest_item_exp

       boost = (grp_min_size*max_avg_exp*bnd) - exp_grp_min_without_highest

       exp = np.copy(exp_at_position) #deep copy
       exp[np.argwhere(current_group_ids == grp_min_avg_exp).flatten()] = np.Inf
       exp[indx_highest_grp_min_item] = np.Inf #added 11/21
       indx = (np.abs(exp - boost)).argmin() #find position with closest exposure to boost
       if swapped[indx] == True: #swapping same item
           if indx >= len(swapped):
               break
           while(swapped[indx] != False):
               if indx < len(swapped) - 2:
                   indx += 1
               else:
                   break
       min_grp_item = current_ranking[indx_highest_grp_min_item]
       print("min_grp_item",min_grp_item)
       swapping_item = current_ranking[indx]
       print("swapping_item", swapping_item)
       #put swapping item in min_grp_item position
       current_ranking[indx_highest_grp_min_item] = swapping_item
       #put min_group_item at indx
       current_ranking[indx] = min_grp_item
       repositions += 1
       swapped[indx_highest_grp_min_item] = True
       swapped[indx] = True
       #update group ids
       current_group_ids = [item_group_dict[i] for i in current_ranking]
       current_group_ids = [unique_grp_strings.index(v) for v in current_group_ids]
       #set up next loop
       prev_exp = cur_exp
       cur_exp, avg_exps = calc_exposure_ratio(current_ranking, current_group_ids)
       print("exposure after swap:", cur_exp)
       if prev_exp == cur_exp:
           break


   if grporder == True: #Reorder to preserve consensus
       consensus = np.asarray(consensus)
       current_ranking = np.copy(consensus)
       current_group_ids = np.asarray(current_group_ids)
       consensus_group_ids = np.asarray(consensus_group_ids)
       for g in np.unique(current_group_ids).tolist():
           where_to_put_g = np.argwhere(current_group_ids == g).flatten()
           g_ordered = consensus[np.argwhere(consensus_group_ids == g).flatten()] #order in copeland
           current_ranking[where_to_put_g] = g_ordered
       return current_ranking.tolist()
   return current_ranking.tolist()


def epira_break(rating_df, item_col, rating_col, item_group_dict, epira_bnd, rand_seed):
    """
    Baseline from Cachel et al. FAccT'23, applied to tied bucket orders
    :param rating_df:
    :param item_col:
    :param rating_col:
    :param item_group_dict:
    :param epira_bnd:
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
            new_order = epiRA(tied_items_list, item_group_dict, epira_bnd, True)
            fair_ranking_list = fair_ranking_list + new_order
        else:
            fair_ranking_list = fair_ranking_list + tied_items_list  # no need to break since 1 item or same group

    return pd.DataFrame(fair_ranking_list), pd.DataFrame(scores_np)

def __bordascoring(profile_df, candidate_ids):
    """
    BORDA preference aggregation.
    :param profile_df: Dataframe of preference profile
    :param considered_candidates:  Numpy array of canidates ids
    :param k_cnt: length of consensus ranking
    :return:Dataframe of consensus ranking
    """
    num_rankings = len(profile_df.columns)
    borda_scores = {key: 0 for key in candidate_ids}
    num_items = len(candidate_ids) # use for borda count with same scores per ranking
    for r in range(0, num_rankings):
        single_ranking = profile_df.iloc[:, r] # isolate ranking
        single_ranking = np.array(
            single_ranking[~pd.isnull(single_ranking)]
        )  # drop any NaNs
        # num_items = len(single_ranking) # use for borda count with different scores per ranking
        points_at_pos = list(range(num_items - 1, -1, -1))
        for item_pos in range(0, len(single_ranking)):
            item = single_ranking[item_pos]
            borda_scores[item] +=points_at_pos[item_pos]

    ids = list(borda_scores.keys())
    new_scores = [borda_scores[cand] for cand in ids]
    scores, ordered_candidate_ids = zip(*sorted(zip(new_scores, ids), reverse=True))
    return ordered_candidate_ids


def epira_full(rating_df, item_col, rating_col, item_group_dict, epira_bnd, rand_seed, rater_col):
    """
    Baseline from Cachel et al. FAccT'23
    """


    #make profile
    profile_df = pd.DataFrame()
    for rater in tqdm(np.unique(rating_df[rater_col])):
        sub_df = rating_df[rating_df[rater_col] == rater]
        if len(sub_df) > 1:
            sorted_df = sub_df.sort_values(by=[rating_col], ascending=False)
            candidates = sorted_df[item_col].reset_index(drop=True)
        else:
            candidates = sub_df[item_col].reset_index(drop=True)

        profile_df = pd.concat([profile_df, candidates], axis=1)

    candidate_ids = np.asarray(list(item_group_dict.keys()))
    consensus = __bordascoring(profile_df, candidate_ids)
    # Fairness of Exposure Post-Process
    new_order = epiRA(consensus, item_group_dict, epira_bnd, True)
    items, scores = src.avg_rating(rating_df, item_col, rating_col, rand_seed)
    items = items.to_list()
    scores = scores.to_list()
    result_scores = [scores[items.index(i)] for i in new_order]
    return pd.DataFrame(new_order), pd.DataFrame(result_scores)