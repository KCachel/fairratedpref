import pandas as pd
from exp_workflow import *

url = 'https://raw.githubusercontent.com/MengtingWan/marketBias/master/data/df_electronics.csv'
rating_df = pd.read_csv(url)

#Data Preparation
rating_df = rating_df[rating_df['year'] == 2017]

item_col = 'item_id'
rating_col = 'rating'
group_col = 'model_attr'
dataset_name = 'Electronics'
csv_name = 'results/electronics/results_electronics.csv'
epira_bnd = .9 #highest observed exposure according to method
epsilon = 0.6
rand_seed = 1
num_rating = 5
#since the dataset is imbalanced (some items have 1000s of rating and others have a handful) take 5 reviews per item
drop_s = rating_df[item_col].value_counts() < num_rating #items with less than 5 reviews
drop = drop_s[drop_s].index.values
rating_df = rating_df[~rating_df[item_col].isin(drop)]
rating_df = rating_df.groupby(item_col).sample(n=num_rating, random_state=10)


print("There are ", len(rating_df[item_col].unique()), " items in the dataset.")
print("There are ", len(rating_df['user_id'].unique()), " raters in the dataset.")
print("There are ", len(rating_df), " ratings in the dataset.")
print("The groups are: ", rating_df[group_col].unique())
print("The profile GFR is: ", src.group_fair_rating(rating_df, item_col, rating_col, group_col, np.unique(rating_df[rating_col]), np.unique(rating_df[group_col])))
rater_col = 'user_id'
gfrs = []
for r in np.unique(rating_df[rater_col]):
    sub_df = rating_df[rating_df[rater_col] == r]
    gfrs.append(src.group_fair_rating(sub_df, item_col, rating_col, group_col, np.unique(rating_df[rating_col]), np.unique(rating_df[group_col])))
print("The average GFR is: ", np.mean(gfrs))
rating_df = rating_df[[item_col, rating_col, group_col, rater_col]]
run_exp(rating_df, item_col, rating_col, group_col, dataset_name, csv_name, epira_bnd, epsilon, rater_col)