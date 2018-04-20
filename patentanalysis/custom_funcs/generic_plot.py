import seaborn as sns
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# dataset = pd.read_excel("C:\Users\U783495\Documents\BYN\DSR\AA\excel2017-08-03-10-04-26.xlsx", sheetname="Sheet1", header=0)
dataset = pd.read_excel("C:\Users\U582788\Desktop\OTC\Analytics\APAC\excel2017-08-02-16-48-47.xlsx", sheetname="Sheet1", header=0)
#sns.plt.show()

# Publication year vs. Count of records
def PubYearPlot(dataset):
    sns.set_style("whitegrid")
    palette = mpl.colors.hex2color('#feb24c')
    plot = sns.factorplot(x="Publication Year", data=dataset, kind="count", color=palette,
                    size=6, aspect=1.5)
    ax = plt.gca()
    for p in ax.patches:
        ax.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()),
                fontsize=10, color='black', ha='center', va='bottom')
    plot.set_axis_labels("Publication Year", "Number of Records")
    # .set_xticklabels(step=2))
    return plot



# Other attributes vs. Count of records
# Regroup to top10 & others
def BarPlot(dataset, field):
    counts = pd.DataFrame(dataset[field].value_counts())
    counts["Field"] = counts.index
    counts.index = range(len(counts))
    counts.rename(columns={field:"Count", "Field":field}, inplace=True)
    if len(counts) > 10:
        counts_grp = counts.head(10)
        counts_grp.loc[11] = [sum(counts[10:]["Count"]), "Other"]
    else:
        counts_grp = counts
    palette = mpl.colors.hex2color('#feb24c')
    plot = sns.factorplot(x="Count", y=field, data=counts_grp,
                        kind="bar", color=palette)
    plot.set_axis_labels("Number of Records", field)
    return plot

# BarPlot(dataset, "Application Country")
# BarPlot(dataset, "Assignee - Current US")


# 3D Selected Field vs. Time vs. Count of records
def ThreeDPlot(dataset, field):
    top_10_cnt = dataset[field].value_counts()[:10].index
    cnt_3d = dataset.groupby([field, "Publication Year"]).size().reset_index(name="Frq")
    cnt_3d = cnt_3d[cnt_3d[field].isin(top_10_cnt)]

    cnt_pivot = cnt_3d.pivot_table("Frq", "Publication Year", field, fill_value=0)
    cnt_pivot = cnt_pivot[top_10_cnt]
    cnt_array = np.array(cnt_pivot)

    years = cnt_pivot.index
    cnts = cnt_pivot.columns

    fig = plt.figure()
    ax = Axes3D(fig)

    lx = len(cnt_array[0])            # Work out matrix dimensions
    ly = len(cnt_array[:,0])
    xpos = np.arange(0,lx,1)    # Set up a mesh of positions
    ypos = np.arange(0,ly,1)
    xpos, ypos = np.meshgrid(xpos+0.25, ypos+0.25)

    xpos = xpos.flatten()   # Convert positions to 1D array
    ypos = ypos.flatten()
    zpos = np.zeros(lx*ly)

    dx = 0.5 * np.ones_like(zpos)
    dy = dx.copy()
    dz = cnt_array.flatten()

    cs = ["#9e0142", "#d53e4f", "#f46d43", "#fdae61", "#fee08b", "#e6f598", "#abdda4", "#66c2a5", "#3288bd", "#5e4fa2"] * ly
    ax.bar3d(xpos,ypos,zpos, dx, dy, dz, color=cs)

    ax.set_xticks(range(0, len(cnts)))
    ax.set_yticks(range(0, len(years)))
    ax.w_xaxis.set_ticklabels(cnts)
    ax.w_yaxis.set_ticklabels(years)
    ax.set_xlabel(field, linespacing=3.2)
    ax.set_ylabel('', linespacing=3.2)
    ax.set_zlabel('Number of Records')
    ax.dist = 10

    return plt

# ThreeDPlot(dataset, "Application Country")


PubYearPlot(dataset)