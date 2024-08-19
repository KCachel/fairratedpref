import pandas as pd
from exp_workflow import *

file = 'datasets/xwines/XWines_Slim_150K_ratings.csv'
rating_df = pd.read_csv(file)

meta_file = 'datasets/xwines/XWines_Slim_1K_wines.csv'
metadata_df = pd.read_csv(meta_file)
metadata_df = metadata_df[["WineID", "Type"]]


rating_df = rating_df.merge(metadata_df, on = "WineID") #merge in groups
#Data Preparation
item_col = 'WineID'
rating_col = 'Rating'
group_col = 'Type'
dataset_name = 'XWines'
csv_name = 'results/xwines/results_xwines.csv'
epira_bnd = .9 #highest observed exposure according to method
epsilon = 0.6
rand_seed = 1
num_rating = 6
#since the dataset is imbalanced (some items have hundreds of rating and others have a handful) take 5 reviews per item
drop_s = rating_df[item_col].value_counts() < num_rating #items with less than 5 reviews
drop = drop_s[drop_s].index.values
rating_df = rating_df[~rating_df[item_col].isin(drop)]
rating_df = rating_df.groupby(item_col).sample(n=num_rating, random_state=10)


print("There are ", len(rating_df[item_col].unique()), " items in the dataset.")
print("There are ", len(rating_df['UserID'].unique()), " raters in the dataset.")
print("There are ", len(rating_df), " ratings in the dataset.")
print("The groups are: ", rating_df[group_col].unique())
print("The profile GFR is: ", src.group_fair_rating(rating_df, item_col, rating_col, group_col, np.unique(rating_df[rating_col]), np.unique(rating_df[group_col])))
rater_col = 'UserID'
gfrs = []
for r in np.unique(rating_df[rater_col]):
    sub_df = rating_df[rating_df[rater_col] == r]
    gfrs.append(src.group_fair_rating(sub_df, item_col, rating_col, group_col, np.unique(rating_df[rating_col]), np.unique(rating_df[group_col])))
print("The average GFR is: ", np.mean(gfrs))
rating_df = rating_df[[item_col, rating_col, group_col, rater_col]]
run_exp(rating_df, item_col, rating_col, group_col, dataset_name, csv_name, epira_bnd, epsilon, rater_col)