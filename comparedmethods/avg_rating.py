import pandas as pd
import src as src

def avg_rating_consensus(rating_df, item_col, rating_col, rand_seed):

    ranking, scores = src.avg_rating(rating_df, item_col, rating_col, rand_seed)
    return pd.DataFrame(ranking), pd.DataFrame(scores)