# Pints and Patterns: How Climate Shapes U.S. Beer Ratings

# Our Website

You can find the data story of the project [here!](https://albanpuech.github.io/risky-biscuits-project/)


## Goal

After exploring, in a preliminary analysis, a possible correlation between beers and climate around the world, we have ultimately decided to focus the final part of our project exclusively on the United States of America. The choice of the U.S. allowed us to integrate information on different climates in a more homogeneous manner, given the high number of reviews released from the U.S. and the more consistent distribution of various climates across the states. Starting from this point, our interest focused on exploring the correlation between the ten different climates characterizing the various states in the U.S. and the general types of beers most liked in each state, the grades of these beers, the evolution of the overall grades, and the most reviewed beers. We also dove deeper in the climate analysis by grouping the climates in bigger categories based on three levels of Köppen climate classification: scheme, precipitation and heat level. To complete our analysis we also conducted a textual analysis and observed a possible logic correlation between the adjectives used to describe beer and the climate location.

## Research questions

**Our three main questions are**: 
1) Is there a correlation between climates and the average beer scores (overall, taste, appearance, palate and aroma)?
2) Do users from a certain climate thrive on certain styles of beers?
3) Do people living in different climates prefer beers with different levels of alcohol?

## Additional datasets

In addition to the **BeerAdvocate** and **RateBeer** datasets, we will use the following datasets:

- [Climate data](https://weatherandclimate.com/countries): this dataset is composed of the Köppen climate classification and average temperature for countries worldwide. We will use it to find out if there is a correlation between the climate zone and the beer ratings.

- [SpaCy](https://spacy.io/usage/models): a Python library for advanced Natural Language Processing. We will use their model `en_core_web_sm` to find adjectives in the text reviews in order to see how users qualitatively perceive beers from country to country.

- [United States Census Bureau](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html): this dataset contains a cartographic boundary files of the 50 states of the United States plus 6 territories. We use the file `cb_2018_us_state_500k` to plot the map of the United States using the `geopandas` library. We kept only the states as we do not have any data for the territories.

## Methods

In order to answer the research questions, we work with the following pipeline:

1) Making the dataframe (`us_users_rating`) usable by filtering and cleaning it:
- Merge the provided datasets to get each reviews in a row
- Keep only reviews from users from US
Remove all the beers that have less than 10 reviews

2) **Climate**: 
- Using the previously mentioned dataset for the climate we added the climate corresponding to the each state in the US (`states_climate`)
- To each review we also added separately the three levels of the Köppen climate classification (`climate_classified`)

3) **General styles**:
- Map each specific type of beer to ten general style according to an article by [EHL](https://hospitalityinsights.ehl.edu/beer-types): Lager, Pale Ale, Blonde Ale, Brown Ale, IPA, Wheat beer, Porter, Stout, Sour Ale, Scottish Ale

4) **U.S. Maps**:
- We add to a geopandas dataset (`cb_2018_us_state_500k`) the values we want to plot, they are added to each state depending on which climate it belongs to
- Use geopandas to plot the resulting map of the U.S.

5) Make sure that the columns of interest used in each different section doest have NaN.

6) **Analysis of the scores**:
- We group the dataframe per climate and we compute the mean of the different scores (overall, taste, appearance, palate and aroma). We compare the plots. 
- We repeat the analysis for the three others climates classification and, in order to increase the interpretability, we use radar charts where we visualize the scores per category. 
	
7) **Analysis of the styles of beers**:
- We look at the distribution of the general style of beers in each climate and we plot it on a world cloud.
- For each climate we sort the beer styles in two different ways: 
    - The most popular beer styles: based on the number of reviews
    - The preferred beer styles: based on the mean overall score
- We plot the results to compare
- For each general type we look at the overall mean across the climates and we visualize them on a line plot to investigate for potential patterns.
- We repeat the analysis for the three others climates classification 
- We check the variability of the abv within each general type and we focused on the interval between the 25th and 75th quantile for each case.

8) **Analysis of the abv**:
- In order to remove the outliers, which highly impact the means of the abv, we only keep beers which are between the 5th and the 95th quantile. 
- For each climate we sort the three best general type of beers, based on the score given by the users, and the three most reviewed beer, based on the number of reviews per each style of beer.
- We then plot the two categories in the U.S. map
- We repeat the analysis for the three others climates classification

**Note**: for each comparison between different datasets we computed in parallel statistical tests (one-way ANOVA tests) to account for statistically significance of the results. 
 

## Proposed timeline

**Step 1**: 20/11/2023: Finish the pre-processing.<br>
**Step 2**: 04/12/2023: Finish the parts of the scores, styles of beers and abv. To be done on parallel, at the end see what could be improved.<br>
**Step 3**: 11/12/2023: Finish the text analysis. On the side, redo what is needed.<br>
**Step 4**: 18/12/2023: Finish the analysis. Start working on the data story and add needed plots.<br>
**Step 5**: 22/12/2023: Submit the work.


## Organization within the team

| Member   | Task |
| -------- | ------- |
| **Alban**  | data cleaning, time analysis, data story   |
| **Barbara**| textual analysis, data story    |
| **Marin** | scores analysis, review and formatting the code |
| **Emilie** | abv analysis, README |
| **Meline** | general type analysis, data story |