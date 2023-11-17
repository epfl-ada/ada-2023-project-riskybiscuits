# Seeing the world through the lens of beer reviews

## Abstract

Beers are produced and consumed in every part of the world. One can thus wonder how beers around the world are perceived by different cultures. The interest of this project is to look into how beers from each country of production are judged and how specific countries judge others. As a side note, we will finally answer an age-old question : Are German beers actually good ?

On the one hand, we want to explore how a country’s beers are perceived both quantitatively and qualitatively. On the other hand, we will analyze the users’ ratings and look for significant patterns in how distinct countries rate other countries. For both of these analyses, we will dissect both the ratings and reviews to understand the feelings of the users. These findings will also be mapped to their climate to see if there is a correlation between a countries’ beer rating and the climate of said country. 

## Research questions

The goal of this project is to answer the following questions:

1) Which country has the best beers in the world?
2) Which beers have more ratings in each country? Which beers are the best rated in each country?
3) What adjectives are most commonly used in the reviews to describe beers in different countries? Are there some recurrent adjectives when looking at the totality of the considered countries?
4) What is the correlation between a country’s climate and the beer it produced? Is the climate influencing the taste and the look of the beer? 
5) Does the reviewer’s nationality influence the rating a beer will receive? How is a target country differently evaluated by people from other countries? 
6) What is the cross-correlation between the country of the reviewer and the country of the beer? Does the country of origin of a user have an influence on their taste in beer?

## Additional datasets

In addition to the BeerAdvocate and RateBeer datasets, we will use the following datasets:

- [Climate data](https://weatherandclimate.com/countries): this dataset is composed of the Köppen climate classification and average temperature for countries worldwide. We will use it to find out if there is a correlation between the climate zone and the beer ratings.

- [SpaCy](https://spacy.io/usage/models): a Python library for advanced Natural Language Processing. We will use their model `en_core_web_sm` to find adjectives in the text reviews in order to see how users qualitatively perceive beers from country to country.

- [United States Census Bureau](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html): this dataset contains a cartographic boundary files of the 50 states of the United States plus 6 territories. We use the file `cb_2018_us_state_500k` to plot the map of the United States using the `geopandas` library. We kept only the states as we do not have any data for the territories.

## Methods

In order to answer the research questions, we will use the following pipeline:

- Making of useable dataframes:

    - Remove the beers that have less than 10 reviews to have enough data points and make significant conclusions
    - Depending on the part of the analysis, remove all reviews for which the beer’s origin has less than 10 beers or if the user has rated less than 10 beers for validity 
    - If in the analysis 2, we first select one country as the source and keep only reviews from users of that country


- Compute the average ratings (according to the 5 different scores: Overall, Taste, Aroma, Palate and Appearance, or to the average of these) of the beers of each country kept in the analysis.
- For these results check their statistical significance and if they are, plot them on a world map for visual comparison
- Furthermore, for each country look at the most common adjectives used to describe their beers and use wordclouds to display them, can also compute an average positivity using Spacy to see if it matches with the average ratings
- If time allows it, we will also look at the climate of the country to look for a correlation between the climate and the ratings of a country’s beer. If so, check it’s statistical significance. 

## Proposed timeline

<ol>
<li> Data cleaning and making adequate dataframes for the different analyses. </li>
<li> Go through the beer rating dataset and make different visualizations of :
    <ol type="a">
    <li>The average ratings received per country (looking into the different sub-categories).</li>
    <li>The best rated beers of each country.</li>
    <li>Any correlations between the two previous findings.</li>
    </ol>
</li>
<li>
Find the most used adjectives from the textual reviews for each country. Make a word cloud visualization of these with a scale of writing to show the predominance of each used adjective in the ratings given to each country. Try to look at the positivity of these words and see if any correlation with the ratings appears.
</li>
<li>Group the countries per climate and make visualizations of:
    <ol type="a">
    <li>the average rating of beers per climate group</li>
    <li>the best rated beer per climate group</li>
    <li>the most used adjectives per climate group</li>
    <li>cross-correlation between the previous findings</li>
    </ol>
</li>
<li> Observe the reviews and ratings given by users of a certain nationality. Make visualizations of:
    <ol type="a">
    <li>the average rating given per country</li>
    <li>the best rated beers per users in a certain country</li>
    <li>any correlations between the two previous findings</li>
    </ol>
</li>
<li> For each country look at how users from the rest of the world rate its beers. This is done by aggregating the users in their respective country in order to be able again to plot on a map the results. Look for correlation between the ratings of the beers of the users’ origin country by comparison with the ones of the target and how they rate the beers of the target country. </li>
<li> Create an interactive map to visualize our findings. </li>
</ol>

## Organization within the team

We intend to separate the work as follows:

- Alban: How to be able to select a target country with interactive maps. Will also work on building the website.
- Barbara: Climate analysis and qualitative analysis of the textual reviews
- Marin: Analysis of the ratings of the beers of each country, help with the textual analysis.
- Emilie: Analysis of the reviews from users of the same country. Compute correlations with the ratings of the beers of their country.
- Meline: Analysis of the reviews from users of different countries and how they rate the beers of the target country. Look at which are the best beers after selecting one country or group of users.
