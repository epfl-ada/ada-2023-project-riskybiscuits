import pandas as pd
import numpy as np


def get_reviews_df(review_path: str) -> pd.DataFrame:
    """Returns dataframe of reviews from the given txt file

    Args:
        review_path (str): path to the txt file containing the reviews

    Returns:
        pd.DataFrame: DataFrame of the reviews
    """
    with open(review_path, "r", encoding="utf8") as f:
        lines = f.readlines()

    # remove line breaks
    lines_without_breaks = [line[:-1] for line in lines if line != "\n"]

    # remove name of the feature and keep only the feature values
    data = [line[line.find(": ") + 2 :] for line in lines_without_breaks]
    data = np.array(data, dtype="object")

    # get features names
    features = [line[0 : line.find(": ")] for line in lines_without_breaks]
    n_features = np.unique(features).shape[0]
    features = features[:n_features]
    if len(lines_without_breaks) % n_features != 0:
        raise ValueError("There are missing features for at least one review")

    # create df
    reviews = data.reshape((-1, n_features))
    reviews_df = pd.DataFrame(reviews, columns=features)
    return reviews_df


def get_breweries_df(breweries_path: str) -> pd.DataFrame:
    """Returns dataframe of breweries

    Args:
        breweries_path (str): path to the csv file of the dataset

    Returns:
        pd.DataFrame: dataframe of breweries
    """

    # Get useful columns from csv file
    breweries_df = pd.read_csv(
        breweries_path,
        skiprows=1,
        usecols=[
            "id",
            "location",
            "name",
            "nbr_beers",
            "id.1",
            "nbr_beers.1",
        ],
    )

    # rename columns to distinguish between the features coming from
    # BeerAdvocate (we use the suffix "_ba"), and RateBeer (suffix "_rb")
    breweries_df = breweries_df.rename(
        {
            "id": "brewery_id_ba",
            "location": "brewery_location_ba",
            "name": "brewery_name_ba",
            "nbr_beers": "brewery_nbr_beers_ba",
            "id.1": "brewery_id_rb",
            "nbr_beers.1": "brewery_nbr_beers_rb",
        },
        axis=1,
        errors="raise",
    )
    return breweries_df


def get_beers_df(beers_path: str) -> pd.DataFrame:
    """Returns dataframe of beers

    Args:
        beers_path (str): path to the csv file of the beers data

    Returns:
        pd.DataFrame: dataframe containing beer data
    """

    # Get useful columns:
    beers_df = pd.read_csv(
        beers_path,
        skiprows=1,  # first row is used to indicate what feature comes from BeerAdvocate and what feature comes from RateBeer
        usecols=[
            "beer_id",
            "beer_name",
            "brewery_id",
            "nbr_ratings",
            "style",
            "abv",
            "avg_computed",
            "beer_id.1",
            "brewery_id.1",
            "nbr_ratings.1",
            "avg_computed.1",
        ],
    )

    # rename columns to distinguish between the same features coming from BeerAdvocate and RateBeer
    # (They are going to be useful to make joins and merges between Dataframes)
    beers_df = beers_df.rename(
        columns=lambda col: col.replace(".1", "_rb")
        if col.endswith(".1")
        else col + "_ba",
        errors="raise",
    )

    # rename column name to more explicit names
    beers_df = beers_df.rename(
        {
            "avg_computed_ba": "beer_avg_rating_ba",
            "avg_computed_rb": "beer_avg_rating_rb",
        },
        axis=1,
        errors="raise",
    )

    # Compute the weighted average beer scores using data from both BA and RB
    beers_df["beer_avg_rating_ba_rb"] = (
        beers_df["beer_avg_rating_ba"] * beers_df["nbr_ratings_ba"]
        + beers_df["beer_avg_rating_rb"] * beers_df["nbr_ratings_rb"]
    ) / (beers_df["nbr_ratings_rb"] + beers_df["nbr_ratings_ba"])

    return beers_df


def join_breweries_on_beers(
    beers_df: pd.DataFrame, breweries_df: pd.DataFrame
) -> pd.DataFrame:
    """Performs join between breweries and beers.
    This is necessary to add important features to the beer dataset,
    such as the country where the beer comes from, the number of other
    beers produced by the same brewery, ...

    We keep the features present in both datasets on purpose, so as to be able
    to perform joins on the review dataset for reviews coming from both
    website.

    Args:
        beers_df (pd.DataFrame): dataframe of the beers
        breweries_df (pd.DataFrame): dataframe of the breweries

    Returns:
        pd.DataFrame: Left join between the beers and the breweries dataframes
    """
    return beers_df.merge(
        breweries_df,
        left_on=["brewery_id_ba", "brewery_id_rb"],
        right_on=["brewery_id_ba", "brewery_id_rb"],
        how="left",
    )


def get_users_df(users_path: str) -> pd.DataFrame:
    """Returns user dataframe from csv file of the dataset

    Args:
        users_path (str): path to csv file containing the data

    Returns:
        pd.DataFrame: dataframe of the users
    """
    users = pd.read_csv(users_path)
    return users.drop_duplicates(subset="user_id", keep="first")


def merge_reviews(
    ba_df: pd.DataFrame,
    rb_df: pd.DataFrame,
    beers_df: pd.DataFrame,
    users_df_ba: pd.DataFrame,
    users_df_rb: pd.DataFrame,
) -> pd.DataFrame:
    """Merges the reviews from BeerAdvocate and RateBeer with the users and beers dataframes
    - Merging with the users dataframe allow us to add insightful features to the reviews,
    such as the number of reviews of the user, its location, ...
    - Merging with the beers dataframe adds features like the average rating of the beer,
    the country where the beer comes from, the number of ratings it has received on both websites, ...
    - A few features are available for both websites: This is the case of the number of reviews received
    by the beer on each website, or its average rating.

    Args:
        ba_df (pd.DataFrame): dataframe of the reviews from BeerAdvocate
        rb_df (pd.DataFrame):dataframe of the reviews from RateBeer
        beers_df (pd.DataFrame): dataframe of the beers
        users_df_ba (pd.DataFrame): dataframe of the users of BeerAdvocate
        users_df_rb (pd.DataFrame): dataframe of the users of RateBeer

    Raises:
        ValueError: If the resulting dataframe length is not equal to the sum of length
        of the ba_df and rb_df dataframes

    Returns:
        pd.DataFrame: complete dataframe of the reviews
    """
    n_reviews_ba = ba_df.shape[0]
    n_reviews_rb = rb_df.shape[0]

    # We drop the features that are going to be obtained when merging with the brewery dataset
    ba_df = ba_df.drop(["brewery_name", "abv"], axis=1)
    rb_df = rb_df.drop(["brewery_name", "abv"], axis=1)

    users_df_ba = users_df_ba[["user_id", "location", "nbr_ratings"]]
    users_df_rb = users_df_rb[["user_id", "location", "nbr_ratings"]]

    # this is necessary to perform a join on the "user_id" between the review and the user datasets
    ba_df.user_id = ba_df.user_id.astype(str)
    rb_df.user_id = rb_df.user_id.astype(str)

    users_df_ba.loc[:, "user_id"] = users_df_ba.user_id.astype(str)
    users_df_rb.loc[:, "user_id"] = users_df_rb.user_id.astype(str)

    ba_df.beer_id = ba_df.beer_id.astype(int)
    rb_df.beer_id = rb_df.beer_id.astype(int)

    # Merge each reviews dataframe with the beer dataframe. We do it separately because the
    # column name on which the review dataset is merged on the beer dataset depends on the
    # provenance of the data (beers have different ID on RateBeer and BeerAdvocate)
    ba_df = pd.merge(
        ba_df,
        beers_df,
        left_on="beer_id",
        right_on="beer_id_ba",
        how="left",
    )

    rb_df = pd.merge(
        rb_df,
        beers_df,
        left_on="beer_id",
        right_on="beer_id_rb",
        how="left",
    )

    # Merge each reviews dataframe with the user dataset that corresponds to the right website.
    # We use the unmatched user datasets because the matched one (that only contains the users that
    # are active on both websites) only contains 3000 users, while there are more than 90000 unique
    # users in total in the final dataset. Merging each review dataframe with its user dataframe
    # allows to get all the data for the users.
    ba_df = pd.merge(
        ba_df,
        users_df_ba,
        left_on="user_id",
        right_on="user_id",
        how="left",
    )

    rb_df = pd.merge(
        rb_df,
        users_df_rb,
        left_on="user_id",
        right_on="user_id",
        how="left",
    )

    # Concatenate the reviews dataframe
    reviews_df = pd.concat([ba_df, rb_df])
    reviews_df.drop(["brewery_id"], axis=1, inplace=True)

    if (n_reviews_ba + n_reviews_rb) != reviews_df.shape[0]:
        raise ValueError("There are missing breweries or duplicate entries in beers")
    
    #remove the duplicate beer_name_ba column
    reviews_df = reviews_df.drop(['beer_name_ba'], axis=1)


    # rename the columns to give them more explicit names
    reviews_df = reviews_df.rename(
        {
            "brewery_name_ba": "brewery_name",
            "brewery_location_ba": "brewery_location",
            "style_ba": "style",
            #"beer_name_ba": "beer_name",
            "abv_ba": "abv",
            "location": "user_location",
            "nbr_ratings": "user_nbr_ratings",
        },
        axis=1,
        errors="raise",
    )
   

    return reviews_df
