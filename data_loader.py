import pandas as pd
import numpy as np


def get_reviews(file, n_features):
    """
    Returns dataframe of beet reviews from txt file
    """
    with open(file, "r", encoding="utf8") as f:
        lines = f.readlines()
    lines_without_breaks = [line[:-1] for line in lines if line != "\n"]
    data = [line[line.find(": ") + 2 :] for line in lines_without_breaks]
    data = np.array(data, dtype="object")
    features = [line[0 : line.find(": ")] for line in lines[:n_features]]
    reviews = data.reshape((-1, n_features))
    reviews_df = pd.DataFrame(reviews, columns=features)
    return reviews_df
