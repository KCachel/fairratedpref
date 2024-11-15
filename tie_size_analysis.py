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


def run_exp():
    csv_name = 'results/tie_analysis/tie_analysis_results.csv'
    rand_seed = 1
    print("Starting iteration 1...")
    iteration_results_df1 = core(rand_seed)

    rand_seed = 2
    print("Starting iteration 2...")
    iteration_results_df2 = core(rand_seed)

    rand_seed = 3
    print("Starting iteration 3...")
    iteration_results_df3 = core(rand_seed)

    rand_seed = 4
    print("Starting iteration 4...")
    iteration_results_df4 = core(rand_seed)

    rand_seed = 5
    print("Starting iteration 5...")
    iteration_results_df5 = core(rand_seed)



    frames = [iteration_results_df1, iteration_results_df2, iteration_results_df3, iteration_results_df4, iteration_results_df5]
    results = pd.concat(frames)
    #results.to_csv('results/tie_analysis/tie_analysis_verbose_results.csv', index=False)
    result = results.groupby(by=['method', 'dataset', 'TIE_PROP', 'NOT_TIE_PROP', 'GFR']).mean().reset_index()
    result.to_csv(csv_name, index=False)

def core(rand_seed):

    #initialize data collectors
    method = []
    dataset = []
    NDKL_Value = []
    ULOSS_Value = []
    WULOSS_Value = []
    TIE_PROP = []
    NOT_TIE_PROP = []
    GFR = []

    num_items = 100
    skewed_groups = np.hstack((np.tile('G1', 50), np.tile('G2', 50)))
    alternating_groups = np.tile(np.hstack((np.tile('G1', 10), np.tile('G2', 10))), 5)
    epira_bnd = .9
    epsilon = .6
    for g in ['skewed_groups', 'alternating_groups']:
        if g == 'skewed_groups':
            groups = skewed_groups
        if g == 'alternating_groups':
            groups = alternating_groups
        for tied_proportion in [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]:
            print("Working on ....", g)
            print("Working on tied_proportion....", tied_proportion)
            unique_ratings = num_items - num_items * tied_proportion
            not_tied_ratings = np.arange(0, unique_ratings)[::-1]
            tied_ratings = np.tile(unique_ratings, int(tied_proportion * num_items))
            ratings = np.hstack((tied_ratings, not_tied_ratings))
            items = np.arange(0, 100)
            item_col = 'ItemID'
            group_col = 'Group'
            rating_col = 'Rating'
            data = {item_col: items.tolist(),
                    rating_col: ratings.tolist(),
                    group_col: groups.tolist()}
            rating_df = pd.DataFrame(data)
            rating_df = pd.concat([rating_df] * 10, ignore_index=True)
            raters_np = np.tile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 100)
            raters_np.sort()
            rating_df['rater'] = raters_np
            dataset_name = g
            not_tied_proportion = 1 - tied_proportion
            item_group_dict = get_groups(rating_df, item_col, group_col)
            gfr_value = src.group_fair_rating(rating_df, item_col, rating_col, group_col, np.unique(rating_df[rating_col]), np.unique(rating_df[group_col]))

            avg_res, avg_scores = cm.avg_rating_consensus(rating_df, item_col, rating_col, rand_seed)
            method.append('AVG')
            dataset.append(dataset_name)
            NDKL_Value.append(src.NDKL(avg_res, item_group_dict, 'EQUAL'))
            ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, avg_res))
            WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, avg_res))
            TIE_PROP.append(tied_proportion)
            NOT_TIE_PROP.append(not_tied_proportion)
            GFR.append(gfr_value)
            print('Avg done.')
            #
            worst, worst_score = cm.worst_case_break(rating_df, item_col, rating_col, item_group_dict, rand_seed)
            method.append('Worst')
            dataset.append(dataset_name)
            NDKL_Value.append(src.NDKL(worst, item_group_dict, 'EQUAL'))
            print("NDKL WORST ---- ", src.NDKL(worst, item_group_dict, 'EQUAL'))
            ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, worst))
            WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, worst))
            TIE_PROP.append(tied_proportion)
            NOT_TIE_PROP.append(not_tied_proportion)
            GFR.append(gfr_value)
            print('Worst done.')

            fairbreak, fairbreak_score = src.fairbreak(rating_df, item_col, rating_col, item_group_dict, rand_seed)
            method.append('Fair-Break')
            dataset.append(dataset_name)
            NDKL_Value.append(src.NDKL(fairbreak, item_group_dict, 'EQUAL'))
            ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, fairbreak))
            WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, fairbreak))
            TIE_PROP.append(tied_proportion)
            NOT_TIE_PROP.append(not_tied_proportion)
            GFR.append(gfr_value)
            print('Fair break done.')

            vanillamc, vanillamc_score,  fairfull, fairfull_score, fairmc, fairmc_score = src.fairfull(rating_df, item_col, rating_col, item_group_dict, rand_seed)
            method.append('Fair-Full')
            dataset.append(dataset_name)
            NDKL_Value.append(src.NDKL(fairfull, item_group_dict, 'EQUAL'))
            ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, fairfull))
            WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, fairfull))
            TIE_PROP.append(tied_proportion)
            NOT_TIE_PROP.append(not_tied_proportion)
            GFR.append(gfr_value)

            method.append('VanillaMC')
            dataset.append(dataset_name)
            NDKL_Value.append(src.NDKL(vanillamc, item_group_dict, 'EQUAL'))
            ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, vanillamc))
            WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, vanillamc))
            TIE_PROP.append(tied_proportion)
            NOT_TIE_PROP.append(not_tied_proportion)
            GFR.append(gfr_value)


            method.append('FairMC')
            dataset.append(dataset_name)
            NDKL_Value.append(src.NDKL(fairmc, item_group_dict, 'EQUAL'))
            ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, fairmc))
            WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, fairmc))
            print('Markov Methods done.')
            TIE_PROP.append(tied_proportion)
            NOT_TIE_PROP.append(not_tied_proportion)
            GFR.append(gfr_value)


            epibreak, epibreak_score = cm.epira_break(rating_df, item_col, rating_col, item_group_dict, epira_bnd, rand_seed)
            method.append('EPIRA-Break')
            dataset.append(dataset_name)
            NDKL_Value.append(src.NDKL(epibreak, item_group_dict, 'EQUAL'))
            ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, epibreak))
            WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, epibreak))
            TIE_PROP.append(tied_proportion)
            NOT_TIE_PROP.append(not_tied_proportion)
            GFR.append(gfr_value)
            print('EPIRA break done.')

            epifull, epifull_score = cm.epira_full(rating_df, item_col, rating_col, item_group_dict, epira_bnd, rand_seed, 'rater')
            method.append('EPIRA-Full')
            dataset.append(dataset_name)
            NDKL_Value.append(src.NDKL(epifull, item_group_dict, 'EQUAL'))
            ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, epifull))
            WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, epifull))
            TIE_PROP.append(tied_proportion)
            NOT_TIE_PROP.append(not_tied_proportion)
            GFR.append(gfr_value)
            print('EPIRA full done.')

            epsilonbreak, epsilonbreak_score = cm.epsilon_greedy_break(rating_df, item_col, rating_col, item_group_dict, epsilon, rand_seed)
            method.append('Epsilon-Break')
            dataset.append(dataset_name)
            NDKL_Value.append(src.NDKL(epsilonbreak, item_group_dict, 'EQUAL'))
            ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, epsilonbreak))
            WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, epsilonbreak))
            TIE_PROP.append(tied_proportion)
            NOT_TIE_PROP.append(not_tied_proportion)
            GFR.append(gfr_value)
            print('Epsilon break done.')

            epsilonfull, epsilonfull_score = cm.epsilon_greedy_full(rating_df, item_col, rating_col, item_group_dict, epsilon, rand_seed)
            method.append('Epsilon-Full')
            dataset.append(dataset_name)
            NDKL_Value.append(src.NDKL(epsilonfull, item_group_dict, 'EQUAL'))
            ULOSS_Value.append(src.utility_loss(avg_res, avg_scores, epsilonfull))
            WULOSS_Value.append(src.wutility_loss(avg_res, avg_scores, epsilonfull))
            TIE_PROP.append(tied_proportion)
            NOT_TIE_PROP.append(not_tied_proportion)
            GFR.append(gfr_value)
            print('Epsilon full done.')
            print("iteration complete.")

    # Save results
    dic = {'method': method,
           'dataset': dataset,
           'NDKL_Value': NDKL_Value,
           'ULOSS_Value': ULOSS_Value,
           'WULOSS_Value': WULOSS_Value,
           'TIE_PROP': TIE_PROP,
           'NOT_TIE_PROP': NOT_TIE_PROP,
           'GFR': GFR}


    iteration_results_df = pd.DataFrame(dic)
    return iteration_results_df



run_exp()
