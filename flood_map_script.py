#import modules needed for script
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np
import pandas as pd
from shapely.geometry import Point


# ---------------------------------------------------------------------------------------------------------------------
#This section contains code to create the base map which will be used to run analysis on input data 
# ---------------------------------------------------------------------------------------------------------------------

# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles


# create a scale bar of length 20 km in the upper right corner of the map
# adapted this question: https://stackoverflow.com/q/32333870
# answered by SO user Siyh: https://stackoverflow.com/a/35705477
def scale_bar(ax, location=(0.92, 0.95)):
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]

    tmc = ccrs.TransverseMercator(sbllx, sblly)
    x0, x1, y0, y1 = ax.get_extent(tmc)
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    plt.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=tmc)
    plt.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=tmc)
    plt.plot([sbx-10000, sbx - 20000], [sby, sby], color='w', linewidth=6, transform=tmc)

    plt.text(sbx, sby-4500, '20 km', transform=tmc, fontsize=8)
    plt.text(sbx-12500, sby-4500, '10 km', transform=tmc, fontsize=8)
    plt.text(sbx-24500, sby-4500, '0 km', transform=tmc, fontsize=8)


# load the datasets
outline = gpd.read_file('data_files/NI_outline.shp')
towns = gpd.read_file('data_files/Towns.shp')
water = gpd.read_file('data_files/Water.shp')
rivers = gpd.read_file('data_files/Rivers.shp')

# create a figure of size 10x10 (representing the page size in inches)
myFig = plt.figure(figsize=(10, 10))

myCRS = ccrs.UTM(29)  # create a Universal Transverse Mercator reference system to transform our data.

ax = plt.axes(projection=ccrs.Mercator())  # finally, create an axes object in the figure, using a Mercator projection, where we can actually plot our data.

# add the outline of Northern Ireland using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='w')
#xmin, ymin, xmax, ymax = outline.total_bounds
ax.add_feature(outline_feature)

#ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)

# setting the edge colour and the face color.
water_feat = ShapelyFeature(water['geometry'], myCRS,
                            edgecolor='mediumblue',
                            facecolor='mediumblue',
                            linewidth=1)
ax.add_feature(water_feat)

river_feat = ShapelyFeature(rivers['geometry'], myCRS,
                            edgecolor='royalblue',
                            linewidth=0.2)

ax.add_feature(river_feat)

# ---------------------------------------------------------------------------------------------------------------------
#This section contains code to add users housing stock data to the base map  
# ---------------------------------------------------------------------------------------------------------------------

stock_data = pd.read_csv('pointer-sample-data-2011.csv') #user to input file path to their stock data csv

stock_data['geometry']=list(zip(stock_data['xlong'], stock_data['ylat']))
#print(stock_data)
stock_data['geometry'] = stock_data['geometry'].apply(Point)

housing_stock = gpd.GeoDataFrame(stock_data, crs="EPSG:32629")

stock_bounds=housing_stock.geometry.total_bounds
#print(stock_bounds)

housing_stock_handle = ax.plot(housing_stock.xlong, housing_stock.ylat,'s', color='0.5', ms=4, transform=myCRS)


xmin, ymin, xmax, ymax = stock_bounds


ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS) 

# ---------------------------------------------------------------------------------------------------------------------
#Script to build rest of map
# ---------------------------------------------------------------------------------------------------------------------

water_handle = generate_handles(['Lakes'], ['mediumblue'])

river_handle = [mlines.Line2D([], [], color='royalblue')] 

# ax.legend() takes a list of handles and a list of labels corresponding to the objects you want to add to the legend
handles = water_handle + river_handle + housing_stock_handle
labels = ['Lakes', 'Rivers', 'Property'] 

leg = ax.legend(handles, labels, title='Legend', title_fontsize=14,
                 fontsize=12, loc='upper left', frameon=True, framealpha=1)

gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-8, -7.5, -7, -6.5, -6, -5.5],
                         ylocs=[54, 54.5, 55, 55.5])

gridlines.left_labels = False
gridlines.bottom_labels = False

# add the text labels for the towns
for i, row in towns.iterrows():
    x, y = row.geometry.x, row.geometry.y
    plt.text(x, y, row['TOWN_NAME'].title(), fontsize=7, transform=myCRS) # use plt.text to place a label at x,y

scale_bar(ax)

myFig.suptitle('Housing Stock Flood Map', fontsize=12)
ax.set_xlabel('Longitude', fontsize=10)
ax.set_ylabel('Latitude', fontsize='medium')
myFig.savefig('map.png')