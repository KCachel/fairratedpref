import src as src
import pandas as pd
import numpy as np

def fair_mc_routine(matrix, item_group_dict, item_key_dict):

    current_matrix = np.copy(matrix)
    grp_np = np.asarray(list(item_group_dict.values()))
    item_np = np.asarray(list(item_group_dict.keys()))
    num_groups = len(np.unique(list(item_group_dict.values())))
    for item in item_np:
        row = item_key_dict[item]
        item_group = item_group_dict[item]
        for group in np.unique(list(item_group_dict.values())):
            prev_probabilities_per_group = current_matrix[row,
                [item_key_dict[item] for item in item_np[grp_np == group]]]  # original transition prob
            sum_probability_per_group = np.sum(
                prev_probabilities_per_group)  # total transition probability assigned to this group
            new_transitions_for_group = prev_probabilities_per_group * (
                        (1 / num_groups) / sum_probability_per_group)
            current_matrix[row, [item_key_dict[item] for item in item_np[grp_np == group]]] = new_transitions_for_group
            # if group != item_group:
            #     prev_probabilities_per_group = current_matrix[row,
            #         [item_key_dict[item] for item in item_np[grp_np == group]]]  # original transition prob
            #     sum_probability_per_group = np.sum(
            #         prev_probabilities_per_group)  # total transition probability assigned to this group
            #     new_transitions_for_group = prev_probabilities_per_group * (
            #                 (1 / num_groups) / sum_probability_per_group)
            #     current_matrix[row, [item_key_dict[item] for item in item_np[grp_np == group]]] = new_transitions_for_group
            # if group == item_group:
            #     current_matrix[row, [item_key_dict[item] for item in item_np[grp_np == group]]] = 0

    return current_matrix



def fairmc(rating_df, item_col, rating_col, item_group_dict, rand_seed):
    alpha = 1 / 7
    precision = 0.0000001,
    iterations = 500
    num_items, item_key_dict = src.make_metadata(rating_df, item_col)
    partial_transition_matrix = src.fill_transition_matrix(rating_df, num_items, item_key_dict, item_col, rating_col)


    normalized_transition_matrix = src.get_normalized_transition_matrix(partial_transition_matrix, num_items)
    ergodic_transition_matrix = src.ergodic_transition(normalized_transition_matrix, alpha, num_items)
    transition_matrix = fair_mc_routine(ergodic_transition_matrix, item_group_dict, item_key_dict)
    initial_distribution_matrix = src.get_initial_distribution_matrix(num_items)

    stationary_distribution_matrix = src.solve_stationary_distribution_matrix(initial_distribution_matrix,
                                                                          transition_matrix, precision,
                                                                          iterations)
    result_ranking = src.extract_ranks(stationary_distribution_matrix, item_key_dict, rand_seed)
    items, scores = src.avg_rating(rating_df, item_col, rating_col, rand_seed)
    items = items.to_list()
    scores = scores.to_list()
    result_scores = [scores[items.index(i)] for i in result_ranking]
    unique_probs = src.unique_vals(stationary_distribution_matrix)
    return pd.DataFrame(result_ranking), pd.DataFrame(result_scores), unique_probs
