import pandas as pd
from exp_workflow import *

file = 'datasets/hr/IBMHRAnalytics.csv'
rating_df = pd.read_csv(file)

#Bin the ages of employees for groups
bins = [17, 20, 30, 40, 50, 60]
labels = ['10s','20s','30s','40s','50+']
rating_df['BinnedAge'] = pd.cut(rating_df['Age'], bins=bins, labels=labels)

rating_df = rating_df[['EmployeeNumber','BinnedAge', 'EnvironmentSatisfaction', 'JobInvolvement', 'JobSatisfaction', 'PerformanceRating']]

#Format like ratings
rating_df = rating_df.melt(id_vars=['EmployeeNumber','BinnedAge'])

#Data Preparation
item_col = 'EmployeeNumber'
rating_col = 'value'
group_col = 'BinnedAge'
dataset_name = 'HR'
csv_name = 'results/hr/results_hr.csv'
epira_bnd = .9 #highest observed exposure according to method
epsilon = 0.6



print("There are ", len(rating_df[item_col].unique()), " items in the dataset.")
print("There are ", len(rating_df)/len(rating_df[item_col].unique()), " raters in the dataset.")
print("There are ", len(rating_df), " ratings in the dataset.")
print("The groups are: ", rating_df[group_col].unique())
print("The profile GFR is: ", src.group_fair_rating(rating_df, item_col, rating_col, group_col, np.unique(rating_df[rating_col]), np.unique(rating_df[group_col])))
rater_col = 'variable'
gfrs = []
for r in np.unique(rating_df[rater_col]):
    sub_df = rating_df[rating_df[rater_col] == r]
    gfrs.append(src.group_fair_rating(sub_df, item_col, rating_col, group_col, np.unique(rating_df[rating_col]), np.unique(rating_df[group_col])))
print("The average GFR is: ", np.mean(gfrs))
rating_df = rating_df[[item_col, rating_col, group_col, rater_col]]
run_exp(rating_df, item_col, rating_col, group_col, dataset_name, csv_name, epira_bnd, epsilon, rater_col)