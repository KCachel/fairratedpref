import comparedmethods as cm
import src as src
import pandas as pd
import numpy as np
#Note: WULOSS (wieghted utility loss) is called (average rating utility loss) in the paper
def get_groups(rating_df, item_col, group_col):
    grouped_df = rating_df.groupby(by=[item_col, group_col], observed = True).size().reset_index()
    items = grouped_df[item_col].to_list()
    groups = grouped_df[group_col].to_list()
    item_group_dict = dict(zip(items, groups))
    return item_group_dict


def run_exp(rating_df, item_col, rating_col, group_col, dataset_name, csv_name, epira_bnd, epsilon, rater_col):
    item_group_dict = get_groups(rating_df, item_col, group_col)
    rand_seed = 1
    print("Starting iteration 1...")
    iteration_results_df1 = core(rating_df, item_col, rating_col, rand_seed, dataset_name, item_group_dict, epira_bnd, epsilon, rater_col)


    rand_seed = 2
    print("Starting iteration 2...")
    iteration_results_df2 = core(rating_df, item_col, rating_col, rand_seed, dataset_name, item_group_dict, epira_bnd,
                                epsilon, rater_col)
    rand_seed = 3
    print("Starting iteration 3...")
    iteration_results_df3 = core(rating_df, item_col, rating_col, rand_seed, dataset_name, item_group_dict, epira_bnd,
                                epsilon, rater_col)

    rand_seed = 4
    print("Starting iteration 4...")
    iteration_results_df4 = core(rating_df, item_col, rating_col, rand_seed, dataset_name, item_group_dict, epira_bnd,
                                epsilon, rater_col)

    rand_seed = 5
    print("Starting iteration 5...")
    iteration_results_df5 = core(rating_df, item_col, rating_col, rand_seed, dataset_name, item_group_dict, epira_bnd,
                                epsilon, rater_col)



    frames = [iteration_results_df1, iteration_results_df2, iteration_results_df3, iteration_results_df4, iteration_results_df5]
    results = pd.concat(frames)

    result = results.groupby(by=['method', 'dataset']).mean().reset_index()
    result.to_csv(csv_name, index=False)

def core(rating_df, item_col, rating_col, rand_seed, dataset_name, item_group_dict, epira_bnd, epsilon, rater_col):

    #initialize data collectors
    method = []
    dataset = []
    NDKL_Value = []
    ULOSS_Value = []
    WULOSS_Value = []



    avg_res, avg_scores = cm.avg_rating_consensus(rating_df, item_col, rating_col, rand_seed)
    avg_item_col = 'item'
    avg_rating_col = 'rating'
    avg_group_col = 'group'
    avg_rating_df = pd.DataFrame({'rating': avg_scores.iloc[:, 0].to_list(), 'item': avg_res.iloc[:, 0].to_list(),
                              'group': [item_group_dict[i] for i in avg_res.iloc[:, 0].to_numpy()]})
    avg_grf = src.group_fair_rating(avg_rating_df, avg_item_col, avg_rating_col, avg_group_col, np.unique(avg_rating_df[avg_rating_col]),
                          np.unique(avg_rating_df[avg_group_col]))
    print("The GRF of the average rating preference list is: ", avg_grf)

    method.append('AVG')
    dataset.append(dataset_name)
    NDKL_Value.append(src.NDKL(avg_res, item_group_dict, 'EQUAL'))
    ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, avg_res))
    WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, avg_res))
    print('Avg done.')

    worst, worst_score = cm.worst_case_break(rating_df, item_col, rating_col, item_group_dict, rand_seed)
    method.append('Worst')
    dataset.append(dataset_name)
    NDKL_Value.append(src.NDKL(worst, item_group_dict, 'EQUAL'))
    print("NDKL WORST ---- ", src.NDKL(worst, item_group_dict, 'EQUAL'))
    ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, worst))
    WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, worst))
    print('Worst done.')

    fairbreak, fairbreak_score = src.fairbreak(rating_df, item_col, rating_col, item_group_dict, rand_seed)
    method.append('Fair-Break')
    dataset.append(dataset_name)
    NDKL_Value.append(src.NDKL(fairbreak, item_group_dict, 'EQUAL'))
    ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, fairbreak))
    WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, fairbreak))
    print('Fair break done.')

    vanillamc, vanillamc_score, fairfull, fairfull_score, fairmc, fairmc_score = src.fairfull(rating_df, item_col, rating_col, item_group_dict, rand_seed)
    method.append('Fair-Full')
    dataset.append(dataset_name)
    NDKL_Value.append(src.NDKL(fairfull, item_group_dict, 'EQUAL'))
    ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, fairfull))
    WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, fairfull))


    method.append('VanillaMC')
    dataset.append(dataset_name)
    NDKL_Value.append(src.NDKL(vanillamc, item_group_dict, 'EQUAL'))
    ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, vanillamc))
    WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, vanillamc))


    method.append('FairMC')
    dataset.append(dataset_name)
    NDKL_Value.append(src.NDKL(fairmc, item_group_dict, 'EQUAL'))
    ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, fairmc))
    WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, fairmc))
    print('Markov Methods done.')


    epibreak, epibreak_score = cm.epira_break(rating_df, item_col, rating_col, item_group_dict, epira_bnd, rand_seed)
    method.append('EPIRA-Break')
    dataset.append(dataset_name)
    NDKL_Value.append(src.NDKL(epibreak, item_group_dict, 'EQUAL'))
    ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, epibreak))
    WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, epibreak))
    print('EPIRA break done.')

    epifull, epifull_score = cm.epira_full(rating_df, item_col, rating_col, item_group_dict, epira_bnd, rand_seed, rater_col)
    method.append('EPIRA-Full')
    dataset.append(dataset_name)
    NDKL_Value.append(src.NDKL(epifull, item_group_dict, 'EQUAL'))
    ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, epifull))
    WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, epifull))
    print('EPIRA full done.')

    epsilonbreak, epsilonbreak_score = cm.epsilon_greedy_break(rating_df, item_col, rating_col, item_group_dict, epsilon, rand_seed)
    method.append('Epsilon-Break')
    dataset.append(dataset_name)
    NDKL_Value.append(src.NDKL(epsilonbreak, item_group_dict, 'EQUAL'))
    ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, epsilonbreak))
    WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, epsilonbreak))
    print('Epsilon break done.')

    epsilonfull, epsilonfull_score = cm.epsilon_greedy_full(rating_df, item_col, rating_col, item_group_dict, epsilon, rand_seed)
    method.append('Epsilon-Full')
    dataset.append(dataset_name)
    NDKL_Value.append(src.NDKL(epsilonfull, item_group_dict, 'EQUAL'))
    ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, epsilonfull))
    WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, epsilonfull))
    print('Epsilon full done.')
    print("iteration complete.")
    # Save results
    dic = {'method': method,
           'dataset': dataset,
           'NDKL_Value': NDKL_Value,
           'ULOSS_Value': ULOSS_Value,
           'WULOSS_Value': WULOSS_Value}


    iteration_results_df = pd.DataFrame(dic)
    return iteration_results_df




