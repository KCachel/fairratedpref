import pandas as pd
import numpy as np
import src as src
from tqdm import tqdm
import comparedmethods as cm

def make_metadata(rating_df, item_col):
    """
    Get number of items and their mapping
    :param rating_df: Dataframe of rated data
    :param item_col: Column for item names
    :return: number of items, dictionary where values are ints representing each item
    """
    item_key = rating_df[item_col].unique().tolist()#drop any nans
    num_items = len(item_key)
    int_vals = list(range(num_items))
    item_key_dict = dict(zip(item_key, int_vals))
    return num_items, item_key_dict


def ones_transition_matrix(rating_df, num_items, item_key_dict, item_col, rating_col):
    """
    Vanilla MC approach to transition matrix of rated preferences
    :param rating_df:
    :param num_items:
    :param item_key:
    :return:
    """
    matrix = np.zeros((num_items, num_items))
    items = list(item_key_dict.keys())
    mean_ratings = rating_df.groupby(by=[item_col]).mean().reset_index()[rating_col].to_numpy()
    for a in tqdm(items):
        avg_a = np.mean(rating_df[rating_df[item_col] == a][rating_col])
        items_np = np.asarray(items)
        bs_less_avg_a = items_np[mean_ratings <= avg_a]
        matrix[[item_key_dict[i] for i in bs_less_avg_a], item_key_dict[a]] = 1
        matrix[item_key_dict[a], item_key_dict[a]] = 0
        # for b in items:
        #     if a != b:
        #         avg_a = np.mean(rating_df[rating_df[item_col] == a][rating_col])
        #         avg_b = np.mean(rating_df[rating_df[item_col] == b][rating_col])
        #         if avg_a >= avg_b: #a is "higher" so will transition
        #             matrix[item_key_dict[b], item_key_dict[a]] = avg_b / avg_a #note the col corresponds to the transition probs of the item
        #         else:
        #             matrix[item_key_dict[b], item_key_dict[a]] = 0
    return matrix


def get_normalized_transition_matrix(partial_mat, items):
    """
    Calculate the normalized transition matrix from the partial transition matrix
    :param partial_mat: partial transition matrix
    :param items: number of items
    :return: normalized transition matrix
    """
    matrix = partial_mat/items

    for a in range(items):
        matrix[a,a] = 1 - np.sum(matrix[a,:])


    return matrix

def ergodic_transition(norm_matrix, alpha, num_items):
    """
    Make transition ergodic
    :param norm_matrix: Transition matrix
    :param alpha: float
    :param num_items: int
    :return: ergodic matrix
    """
    return (norm_matrix * (1 - alpha)) + (alpha / num_items)

def get_initial_distribution_matrix(items):
    return np.repeat((1 / items), items)

def fair_transition(matrix, item_group_dict, item_key_dict, num_items):


    current_matrix = np.copy(matrix)
    grp_np = np.asarray(list(item_group_dict.values()))
    item_np = np.asarray(list(item_group_dict.keys()))
    num_groups = len(np.unique(list(item_group_dict.values())))

    for item in tqdm(item_np):
        row = item_key_dict[item]
        item_group = item_group_dict[item]
        for group in np.unique(list(item_group_dict.values())):
            if group != item_group:
                prev_probabilities_per_group = current_matrix[row,
                    [item_key_dict[item] for item in item_np[grp_np == group]]]  # original transition prob
                scaling = [(len(prev_probabilities_per_group)**i) for i in range(len(prev_probabilities_per_group))]
                #new_transitions_for_group = scaling/np.sum(scaling) *(1/ (num_groups - 1))
                new_transitions_for_group = np.asarray([i/np.sum(scaling) for i in scaling]) *(1/ (num_groups - 1))
                correct_order_transitions = align_magnitude(prev_probabilities_per_group, new_transitions_for_group, row)
                current_matrix[row, [item_key_dict[item] for item in item_np[grp_np == group]]] = correct_order_transitions
            if group == item_group:
                current_matrix[row, [item_key_dict[item] for item in item_np[grp_np == group]]] = np.nextafter(0,1)

    return current_matrix

def align_magnitude(prev_probabilities_per_group, new_transitions_for_group, seed):
    ind_list = list(range(0, len(prev_probabilities_per_group)))
    prev_sorted, corresponding_ind = zip(*sorted(zip(prev_probabilities_per_group, ind_list)))
    prev_sorted_np = np.asarray(prev_sorted)
    corresponding_ind_np = np.asarray(corresponding_ind)

    np.random.seed(1)
    #above is a stable sort, we would like to random shuffle
    for uni in np.unique(prev_sorted):
        corresponding_ind_np[prev_sorted_np == uni] = np.random.permutation(
            corresponding_ind_np[prev_sorted_np == uni])


    updated_transitions = np.zeros_like(ind_list, dtype=float)
    for i in range(len(corresponding_ind)):
        ith_smallest_new = new_transitions_for_group[i]
        index_for_ith_smallest_new = corresponding_ind_np[i]
        updated_transitions[index_for_ith_smallest_new] = ith_smallest_new

    return updated_transitions.tolist()


def solve_stationary_distribution_matrix(state_matrix, transition_matrix, precision, iterations):
    """
    Update stationary distribution
    :param state_matrix: initial distribution matrix numpy array
    :param transition_matrix: transition matrix numpy array
    :param precision: error margin for convergence, default is 1e-07
    :param iterations: iterations to reach stationary distribution
    :return: numpy array of stationary distribution matrix
    """
    counter = 1
    #while counter <= iterations:
    for counter in range(0,iterations):

        current_state_matrix = state_matrix

        new_state_matrix = state_matrix.dot(transition_matrix)

        error = new_state_matrix - current_state_matrix

        if (np.abs(error) < precision).all():
            break

        state_matrix = new_state_matrix

        #counter += 1

    return state_matrix

def extract_ranks(matrix, item_key, rand_seed):
    """
    Get the item orders
    :param matrix: Stationary matrix
    :param item_key: Dictionary of item names an int mappings
    :return: array of items
    """
    np.random.seed(rand_seed)
    state_matrix = np.copy(matrix)
    if np.all(np.isnan(matrix)) == True: #special case in tie analysis experiments where all items get same score and thus are nans for tied
        state_matrix = np.zeros_like(state_matrix)
    ranking = []
    item_names = list(item_key.keys())
    item_indexers = list(item_key.values())
    for i in range(len(item_key)):
        #max_indx = np.argmax(state_matrix)
        indxs = np.argwhere(state_matrix == np.amax(state_matrix)).flatten()
        np.random.shuffle(indxs)
        max_indx = indxs[0]
        ranking.append(item_names[item_indexers.index(max_indx)])
        state_matrix[max_indx] = -np.Inf

    return np.asarray(ranking)

def unique_vals(stationary_distribution_matrix):
    return len(np.unique(stationary_distribution_matrix))/ len(stationary_distribution_matrix)

def faterate(rating_df, item_col, rating_col, item_group_dict, rand_seed):
    #Run all the markov chain methods to help with the ablation experiment
    alpha = 1 / 7
    precision = 0.0000001,
    iterations = 500
    num_items, item_key_dict = make_metadata(rating_df, item_col)
    partial_transition_matrix = ones_transition_matrix(rating_df, num_items, item_key_dict, item_col, rating_col)


    normalized_transition_matrix = get_normalized_transition_matrix(partial_transition_matrix, num_items)
    ergodic_transition_matrix = ergodic_transition(normalized_transition_matrix, alpha, num_items)


    #FateRate Version
    fair_transition_matrix = fair_transition(ergodic_transition_matrix, item_group_dict, item_key_dict, num_items)
    fairrate, fairrate_score = solve_markov(fair_transition_matrix, num_items, precision, iterations, item_key_dict, rating_df, item_col, rating_col,
                 rand_seed)


    return fairrate, fairrate_score

def fairfull(rating_df, item_col, rating_col, item_group_dict, rand_seed):
    #Run all the markov chain methods to help with the ablation experiment
    alpha = 1 / 7
    precision = 0.0000001,
    iterations = 500
    num_items, item_key_dict = make_metadata(rating_df, item_col)
    partial_transition_matrix = ones_transition_matrix(rating_df, num_items, item_key_dict, item_col, rating_col)


    normalized_transition_matrix = get_normalized_transition_matrix(partial_transition_matrix, num_items)
    ergodic_transition_matrix = ergodic_transition(normalized_transition_matrix, alpha, num_items)
    #ergodic_transition_matrix = partial_transition_matrix

    # Vanilla Version
    vanillamc, vanillamc_score = solve_markov(ergodic_transition_matrix, num_items, precision, iterations,
                                                         item_key_dict, rating_df, item_col, rating_col,
                                                         rand_seed)

    #FairFull Version
    fair_transition_matrix = fair_transition(ergodic_transition_matrix, item_group_dict, item_key_dict, num_items)
    fairfull, fairfull_score = solve_markov(fair_transition_matrix, num_items, precision, iterations, item_key_dict, rating_df, item_col, rating_col,
                 rand_seed)

    # FairMC Version
    fairmc_transition_matrix = cm.fair_mc_routine(ergodic_transition_matrix, item_group_dict, item_key_dict)
    fairmc, fairmc_score= solve_markov(fairmc_transition_matrix, num_items, precision, iterations,
                                                         item_key_dict, rating_df, item_col, rating_col,
                                                         rand_seed)

    return vanillamc, vanillamc_score, fairfull, fairfull_score, fairmc, fairmc_score

def solve_markov(transition_matrix, num_items, precision, iterations, item_key_dict, rating_df, item_col, rating_col, rand_seed):
    initial_distribution_matrix = get_initial_distribution_matrix(num_items)

    stationary_distribution_matrix = solve_stationary_distribution_matrix(initial_distribution_matrix,
                                                                          transition_matrix, precision,
                                                                          iterations)
    result_ranking = extract_ranks(stationary_distribution_matrix, item_key_dict, rand_seed)
    items, scores = src.avg_rating(rating_df, item_col, rating_col, rand_seed)
    items = items.to_list()
    scores = scores.to_list()
    result_scores = [scores[items.index(i)] for i in result_ranking]

    return pd.DataFrame(result_ranking), pd.DataFrame(result_scores)