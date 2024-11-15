import pandas as pd
import src as src
import numpy as np
import FairRankTune as frt

unique_real_ratings = np.asarray(list(range(1,6)))
item_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
rating_list = [5, 5, 5, 5, 1, 1, 1, 1]
group_list = ["G1", "G1", "G1", "G1", "G2", "G2", "G2", "G2"]
item_group_dict = dict(zip(item_list, group_list))
unique_groups = np.unique(group_list)
# dictionary of lists
dic = {'items': item_list, 'rating': rating_list, 'groups': group_list}
rating_df_a = pd.DataFrame(dic)
item_col = 'items'
rating_col = 'rating'
group_col = 'groups'
ranking_a = pd.DataFrame(item_list)

gfr = src.group_fair_rating(rating_df_a, item_col, rating_col, group_col, unique_real_ratings, unique_groups)
ndkl = src.NDKL(ranking_a, item_group_dict, 'EQUAL')
print("GRF of rating A is: ", gfr)
print("NDKL of rating A is: ", ndkl)
scores_a = pd.DataFrame([1, 1, 1, 1, 0, 0, 0, 0])
expu, _ = frt.EXPU(ranking_a, item_group_dict, scores_a, 'MinMaxRatio')
print("EXPU of rating A is: ", expu)



print("++++++++++")
item_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
rating_list = [5, 5, 5, 5, 4, 4, 4, 4]
group_list = ["G1", "G1", "G1", "G1", "G2", "G2", "G2", "G2"]
item_group_dict = dict(zip(item_list, group_list))

# dictionary of lists
dic = {'items': item_list, 'rating': rating_list, 'groups': group_list}
rating_df_b = pd.DataFrame(dic)
item_col = 'items'
rating_col = 'rating'
group_col = 'groups'
ranking_b = pd.DataFrame(item_list)
gfr = src.group_fair_rating(rating_df_b, item_col, rating_col, group_col, unique_real_ratings, unique_groups)
ndkl = src.NDKL(ranking_b, item_group_dict, 'EQUAL')
print("GRF of rating B is: ", gfr)
print("NDKL of rating B is: ", ndkl)

scores_b = pd.DataFrame([1, 1, 1, 1, .75, .75, .75, .75])
expu, _ = frt.EXPU(ranking_b, item_group_dict, scores_b, 'MinMaxRatio')
print("EXPU of rating B is: ", expu)

print("++++++++++")
item_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
rating_list = [5, 5, 5, 5, 4, 4, 3, 3]
group_list = ["G1", "G2", "G1", "G2", "G1", "G2", "G1", "G2"]
item_group_dict = dict(zip(item_list, group_list))

# dictionary of lists
dic = {'items': item_list, 'rating': rating_list, 'groups': group_list}
rating_df_c = pd.DataFrame(dic)
item_col = 'items'
rating_col = 'rating'
group_col = 'groups'
ranking_c = pd.DataFrame(item_list)
gfr = src.group_fair_rating(rating_df_c, item_col, rating_col, group_col, unique_real_ratings, unique_groups)
ndkl = src.NDKL(ranking_c, item_group_dict, 'EQUAL')
print("GRF of rating C is: ", gfr)
print("NDKL of rating C is: ", ndkl)

scores_c = pd.DataFrame([1, 1, 1, 1, .75, .75, .5, .5])
expu, _ = frt.EXPU(ranking_c, item_group_dict, scores_c, 'MinMaxRatio')
print("EXPU of rating C is: ", expu)

print("++++++++++")
item_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
rating_list = [5, 5, 3, 3, 3, 1, 1, 1]
group_list = ["G1", "G2", "G1", "G1", "G1", "G2", "G2", "G2"]
item_group_dict = dict(zip(item_list, group_list))

# dictionary of lists
dic = {'items': item_list, 'rating': rating_list, 'groups': group_list}
rating_df_d = pd.DataFrame(dic)
item_col = 'items'
rating_col = 'rating'
group_col = 'groups'
ranking_d = pd.DataFrame(item_list)
gfr = src.group_fair_rating(rating_df_d, item_col, rating_col, group_col, unique_real_ratings, unique_groups)
ndkl = src.NDKL(ranking_d, item_group_dict, 'EQUAL')
print("GRF of rating D is: ", gfr)
print("NDKL of rating D is: ", ndkl)

scores_d = pd.DataFrame([1, 1, .5, .5, .5, 0, 0, 0])
expu, _ = frt.EXPU(ranking_d, item_group_dict, scores_d, 'MinMaxRatio')
print("EXPU of rating D is: ", expu)

print("++++++++++")
item_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
rating_list = [5, 5, 2, 2, 2, 2, 2, 2]
group_list = ["G1", "G2", "G1", "G1", "G1", "G2", "G2", "G2"]
item_group_dict = dict(zip(item_list, group_list))

# dictionary of lists
dic = {'items': item_list, 'rating': rating_list, 'groups': group_list}
rating_df_e = pd.DataFrame(dic)
item_col = 'items'
rating_col = 'rating'
group_col = 'groups'
ranking_e = pd.DataFrame(item_list)
gfr = src.group_fair_rating(rating_df_e, item_col, rating_col, group_col, unique_real_ratings, unique_groups)
ndkl = src.NDKL(ranking_e, item_group_dict, 'EQUAL')
print("GRF of rating E is: ", gfr)
print("NDKL of rating E is: ", ndkl)
scores_e = pd.DataFrame([1, 1, .25, .25, .25, .25, .25, .25])
expu, _ = frt.EXPU(ranking_e, item_group_dict, scores_e, 'MinMaxRatio')
print("EXPU of rating E is: ", expu)