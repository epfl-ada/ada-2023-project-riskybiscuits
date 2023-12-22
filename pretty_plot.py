"""
pretty_plot.py

This file contains functions for making pretty plots.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd
import seaborn as sns

import matplotlib.cm as cm
from matplotlib.colors import Normalize

from PIL import Image


def plot_climate_one_stat(
    df, column, title, column_ticks=None, cmap_name="YlOrRd"
):  # RdBu_r
    """
    This function plots on a map of the United States the mean of the column passed as an argument for each state depending on its climate.
    df should have a column "climate" and a column str(column) with the values to plot. Requires to call plt.show() after the function call.

    Args:
        df (pd.DataFrame): DataFrame containing the data to plot
        column (str): Column to plot
        title (str): Title of the plot
        column_ticks (list, optional): List of strings to use as ticks on the colorbar. Defaults to None.
        cmap_name (str, optional): Name of the colormap to use. Defaults to "YlOrRd".
    """

    us_map = gpd.read_file("data/Maps/US/cb_2018_us_state_500k.shp")
    states_climate = pd.read_csv("data/states_climate.csv")

    # Add climate column to us_map and the df
    us_map = us_map.merge(states_climate, left_on="NAME", right_on="State")
    us_map = us_map.merge(df, left_on="Climate", right_on="climate")

    # For display purposes, move Alaska and Hawaii to the East
    alaska = us_map[us_map["NAME"] == "Alaska"].geometry
    hawaii = us_map[us_map["NAME"] == "Hawaii"].geometry

    alaska = alaska.translate(xoff=40)
    hawaii = hawaii.translate(xoff=40)

    us_map_shifted = us_map.copy()
    us_map_shifted.loc[us_map_shifted["NAME"] == "Alaska", "geometry"] = alaska
    us_map_shifted.loc[us_map_shifted["NAME"] == "Hawaii", "geometry"] = hawaii

    fig, ax = plt.subplots(figsize=(8, 7))
    us_map_shifted.boundary.plot(ax=ax, linewidth=1, color="black")

    # Plot on the colorbar only the unique values associated to the each climate type
    values = df[column].unique()
    # Sort the dictionary by descending values
    norm = Normalize(vmin=values.min(), vmax=values.max())
    sm = cm.ScalarMappable(cmap=cmap_name, norm=norm)
    sm.set_array([])

    us_map_shifted.plot(
        column=column,
        cmap=cmap_name,
        ax=ax,
        legend=False,
        missing_kwds={"color": "lightgrey", "label": "Missing values"},
    )

    cbar = fig.colorbar(sm, ax=ax, orientation="vertical", ticks=values)
    cbar.set_ticks(values)

    ticks_labels_dict = zip(values, df[column_ticks].unique())

    cbar.set_ticklabels(
        [label + ": {:.2f}".format(value) for value, label in ticks_labels_dict]
    )
    ax.set_title(title)
    # change the size of the title
    ax.title.set_size(13)
    ax.set_axis_off()
    ax.set_xlim(-140, -60)

    plt.show()


def plot_climate_multiple_stats(
    df,
    columns,
    titles,
    column_ticks=None,
    cmap_name="YlOrRd",
    figsize=(8, 7),
    separate_colorbars=False,
):
    """
    This function plots on a map of the United States the mean of the column passed as an argument for each state depending on its climate.
    df should have a column "climate" and a column str(column) with the values to plot. Requires to call plt.show() after the function call.

    Args:
        df (pd.DataFrame): DataFrame containing the data to plot
        column (str): Column to plot
        title (str): Title of the plot
        column_ticks (str, optional): Column to use for the ticks of the colorbar. If None, the column passed as argument is used.
        cmap_name (str, optional): Name of the colormap to use. Defaults to "YlOrRd".
        figsize (tuple, optional): Size of the figure. Defaults to (8, 7). It is to be noted that if mutiple plots are displayed, the figsize is multiplied by the number of plots along the x-axis.
        separate_colorbars (bool, optional): If True, each plot has its own colorbar. If False, all the plots share the same colorbar. Defaults to False.
    """

    us_map = gpd.read_file("data/Maps/US/cb_2018_us_state_500k.shp")
    states_climate = pd.read_csv("data/states_climate.csv")

    # Add climate column to us_map and the df
    us_map = us_map.merge(states_climate, left_on="NAME", right_on="State")
    us_map = us_map.merge(df, left_on="Climate", right_on="climate")

    # For display purposes, move Alaska and Hawaii to the East
    alaska = us_map[us_map["NAME"] == "Alaska"].geometry
    hawaii = us_map[us_map["NAME"] == "Hawaii"].geometry

    alaska = alaska.translate(xoff=40)
    hawaii = hawaii.translate(xoff=40)

    us_map_shifted = us_map.copy()
    us_map_shifted.loc[us_map_shifted["NAME"] == "Alaska", "geometry"] = alaska
    us_map_shifted.loc[us_map_shifted["NAME"] == "Hawaii", "geometry"] = hawaii

    num_plots = len(columns)
    figsize = (figsize[0] * num_plots, figsize[1])
    fig, axes = plt.subplots(1, num_plots, figsize=figsize)

    if not separate_colorbars:
        # Get the min and max values of the columns to plot
        vmin = df[columns].min().min()
        vmax = df[columns].max().max()

    for i in range(num_plots):
        us_map_shifted.boundary.plot(ax=axes[i], linewidth=1, color="black")

        # Plot on the colorbar only the unique values associated to the each climate type
        values = df[columns[i]].unique()

        if separate_colorbars:
            vmin = values.min()
            vmax = values.max()

        # Sort the dictionary by descending values
        norm = Normalize(vmin=vmin, vmax=vmax)
        sm = cm.ScalarMappable(cmap=cmap_name, norm=norm)
        sm.set_array([])

        us_map_shifted.plot(
            column=columns[i],
            cmap=cmap_name,
            ax=axes[i],
            legend=False,
            missing_kwds={"color": "lightgrey", "label": "Missing values"},
            vmin=vmin,
            vmax=vmax,
        )

        cbar = fig.colorbar(sm, ax=axes[i], orientation="vertical", ticks=values)
        cbar.set_ticks(values)
        cbar.set_ticklabels(
            [
                label + ": {:.2f}".format(value)
                for value, label in zip(values, df[column_ticks[i]].unique())
            ]
        )

        axes[i].set_title(titles[i])
        # change the size of the title
        axes[i].title.set_size(13)

        axes[i].set_axis_off()
        axes[i].set_xlim(-140, -60)

    plt.tight_layout()
    plt.show()


def spider_plot(
    scores_around, scores_averages, list_categories, figsize=(8, 8), title=None
):
    """
    This function plots a spider plot of the columns passed as argument.
    Requires to call plt.show() after the function call.

    Args:
        scores_around (list): List of columns to plot as the corners
        scores_averages (list): List of values to plot as the lines
        list_categories (list): List of categories to plot
        figsize (tuple, optional): Size of the figure. Defaults to (8, 8).
        title (str, optional): Title of the plot. Defaults to None.
    """

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, polar=True)

    # Set the angle of the ticks
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Set the ticks
    ticks = np.linspace(0, 2 * np.pi, len(scores_around), endpoint=False)
    ticks = np.append(ticks, ticks[0])

    ax.set_xticks(ticks[:-1])
    ax.set_xticklabels(
        [score for score in scores_around], fontsize=14
    )  # Increase ticks label size

    for climate_t in list_categories:
        # Get the average score for each climate
        average_score = [scores_averages[(climate_t, score)] for score in scores_around]
        average_score.append(average_score[0])

        # Plot the average score for each climate
        ax.plot(ticks, average_score, label=climate_t, linewidth=2)

    # Get the minimum and maximum average score
    min_average_score = min([mean for mean in scores_averages.values()])
    max_average_score = max([mean for mean in scores_averages.values()])
    diff_average_score = max_average_score - min_average_score
    ax.set_ylim(
        min_average_score - 0.1 * diff_average_score,
        max_average_score + 0.1 * diff_average_score,
    )

    # Set the title
    ax.set_title(title, y=1.1, fontsize=20)  # Increase title size
    ax.legend(
        loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=12
    )  # Increase legend size

    plt.show()


def plot_on_beers(
    df,
    column,
    column_ticks=None,
    title=None,
    figsize=(20, 10),
):
    """
    This function plots the column passed as argument different beers.
    The values are showed by how much the beer is filled.

    Args:
        df (pd.DataFrame): DataFrame containing the data to plot
        column (str): Column to plot
        column_ticks (str, optional): Column to use for the ticks of the colorbar. If None, the column passed as argument is used.
        title (str, optional): Title of the plot. Defaults to None.
        figsize (tuple, optional): Size of the figure. Defaults to (20, 10).
    """

    img = plt.imread("data/images/beer2.png")

    mask = np.array(Image.open("data/images/beer2.png").convert("L")) > 1
    mask = ~mask

    num_rows = df.shape[0]
    fig, axs = plt.subplots(1, num_rows, figsize=figsize)

    i = 0
    for row in df.iterrows():
        # Create an image with the same shape as the mask
        img_plot = np.zeros_like(img)

        # in this image put red pixels
        x_center = 145
        width = 116
        height_max = 350
        y_max = 450

        fill_percentage = 1 - row[1][column] / 10

        img_plot[
            int(y_max - fill_percentage * height_max) : y_max,
            x_center - width : x_center + width,
            ...,
        ] = (1, 0.6, 0, 1)

        # Mask the img_plot with the mask
        img_masked = img_plot * mask[..., None]

        img_masked = img_masked + img

        axs[i].imshow(img_masked)
        axs[i].set_title(row[1][column_ticks])
        axs[i].text(
            0.43,
            0.13,
            str(row[1][column]),
            fontsize=15,
            color="black",
            horizontalalignment="center",
            verticalalignment="center",
            transform=axs[i].transAxes,
        )
        axs[i].axis("off")
        i += 1

    plt.suptitle(title, y=0.65)
    plt.show()
