#import modules needed for script
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib_scalebar.scalebar import ScaleBar
import numpy as np
import pandas as pd
from shapely.geometry import Point
import contextily as ctx
#import csv  #remove '#' to activate this if needed for csv output

plt.ion() # make the plotting interactive

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

# load the datasets
outline = gpd.read_file('data_files/NI_outline.shp')
towns = gpd.read_file('data_files/Towns.shp')
water = gpd.read_file('data_files/Water.shp')
rivers = gpd.read_file('data_files/Rivers.shp')
rivers_buffer = gpd.read_file('data_files/Rivers_buffer.shp')

# create a figure of size 11.69, 8.27(representing the page size in inches - size of A4 landscape) 
# can be changed to suit needs of user
myFig = plt.figure(figsize=(11.69, 8.27)) 

myCRS = ccrs.UTM(29)  # create a Universal Transverse Mercator reference system to transform our data.
ax = plt.axes(projection=ccrs.Mercator())  #create an axes object in the figure, using a Mercator projection.

# add the outline of Northern Ireland using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor="None")
ax.add_feature(outline_feature)

# setting the edge colour and the face color.
water_feat = ShapelyFeature(water['geometry'], myCRS,
                            edgecolor='blue',
                            facecolor='blue',
                            linewidth=1)
ax.add_feature(water_feat)

river_feat = ShapelyFeature(rivers['geometry'], myCRS,
                            edgecolor='darkblue',
                            facecolor='None',
                            linewidth=0.7)

ax.add_feature(river_feat)

# ---------------------------------------------------------------------------------------------------------------------
#This section contains code to add users housing stock data to the base map  
# ---------------------------------------------------------------------------------------------------------------------

stock_data = pd.read_csv('housing_stock.csv') #user to input file path to their stock data csv

stock_data['geometry']=list(zip(stock_data['xlong'], stock_data['ylat'])) #user to change attribute name according to csv
#print(stock_data) #remove '#' to check attributes of stock_data
stock_data['geometry'] = stock_data['geometry'].apply(Point)

housing_stock = gpd.GeoDataFrame(stock_data, crs="EPSG:32629")

stock_bounds=housing_stock.geometry.total_bounds
#print(stock_bounds) #remove '#' to check attributes of stock_bounds

xmin, ymin, xmax, ymax = stock_bounds

# ---------------------------------------------------------------------------------------------------------------------
#Analysis of input stock data
# ---------------------------------------------------------------------------------------------------------------------
#print(rivers_buffer.crs == housing_stock.crs) #remove '#' to check same crs, True means same CRS
housing_stock_flood = gpd.sjoin(housing_stock, rivers_buffer, how='inner', lsuffix='left', rsuffix='right')
#print(housing_stock_flood) #remove '#' to check join data

#split layer by flood value
house_50=housing_stock_flood[housing_stock_flood.buff == 50]
house_100=housing_stock_flood[housing_stock_flood.buff == 100]
house_250=housing_stock_flood[housing_stock_flood.buff == 250]
house_null=housing_stock_flood[housing_stock_flood.buff == 0]

#Plot each flood risk bracket
housing_stock_high = ax.plot(house_50.xlong, house_50.ylat,'o', markerfacecolor='red', markeredgecolor='black', markeredgewidth=0.4, ms=2, transform=myCRS)
housing_stock_med = ax.plot(house_100.xlong, house_100.ylat,'o', markerfacecolor='orange', markeredgecolor='black', markeredgewidth=0.4, ms=2, transform=myCRS)
housing_stock_low = ax.plot(house_250.xlong, house_250.ylat,'o', markerfacecolor='yellow', markeredgecolor='black', markeredgewidth=0.4, ms=2, transform=myCRS)
housing_stock_none = ax.plot(house_null.xlong, house_null.ylat,'o', markerfacecolor='green', markeredgecolor='black', markeredgewidth=0.4, ms=2, transform=myCRS)

# ---------------------------------------------------------------------------------------------------------------------
#Script to build rest of map
# ---------------------------------------------------------------------------------------------------------------------

water_handle = generate_handles(['Lakes'], ['blue'])

river_handle = [mlines.Line2D([], [], color='darkblue')] 

# ax.legend() takes a list of handles and a list of labels corresponding to the objects to add to the legend
handles = water_handle + river_handle + housing_stock_high + housing_stock_med + housing_stock_low +housing_stock_none
labels = ['Lakes', 'Rivers', 'High Risk Property', 'Medium Risk Property', 'Low Risk Property', 'No Risk Property'] 

leg = ax.legend(handles, labels, title='Legend', title_fontsize=14,
                 fontsize=12, bbox_to_anchor=(1.04,1), borderaxespad=0, frameon=True, framealpha=1)



# add the text labels for the towns
inds = towns.to_crs(epsg="32629").cx[xmin:xmax, ymin:ymax].index
for i, row in towns.loc[inds].iterrows():
    x, y = row.geometry.x, row.geometry.y
    plt.text(x, y, row['TOWN_NAME'].title(), fontsize=7, transform=myCRS,clip_on=True) # use plt.text to place a label at x,y

#add scalebar
ax.add_artist(ScaleBar(1))

#set axes extent to full extent of data layer
ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS) 

#use contextily to add basemap 
ctx.add_basemap(ax)

# ---------------------------------------------------------------------------------------------------------------------
#Map Output image
# ---------------------------------------------------------------------------------------------------------------------

myFig.suptitle('Housing Stock Flood Map', fontsize=12)
ax.set_xlabel('Longitude', fontsize=10)
ax.set_ylabel('Latitude', fontsize='medium')
myFig.savefig('Housing Stock Flood Risk Map.png', bbox_inches="tight", dpi=500)
#close map plot
plt.close(myFig)

# ---------------------------------------------------------------------------------------------------------------------
#Stock data csv output
# ---------------------------------------------------------------------------------------------------------------------

#work in progress csv output
#print(housing_stock_flood.columns.values)
#fields = [housing_stock_flood.columns]
#rows =[housing_stock_flood]
#filename = "housing_stock_flood_data.csv"
#print(rows)

#with open(filename, 'w') as csvfile: 
   # csvwriter = csv.writer(csvfile) 
    #csvwriter.writerow(fields)
    #csvwriter.writerows(rows, delimiter=",", fmt="%s") 

#working CSV output
np.savetxt('housing_stock_flood_data.csv', housing_stock_flood, delimiter=",", fmt="%s")

# ---------------------------------------------------------------------------------------------------------------------
#Stock data bar graph output
# ---------------------------------------------------------------------------------------------------------------------
Data = gpd.sjoin(housing_stock, rivers_buffer, how='inner', lsuffix='left', rsuffix='right')
df1 = pd.DataFrame(Data,columns=['risk'])
# Count number of each risk element in df
N1, N2, N3, N4 = len(df1[df1['risk'] == 'High Risk']), len(df1[df1['risk'] == 'Medium Risk']), len(df1[df1['risk'] == 'Low Risk']), len(df1[df1['risk'] == 'No Risk'])
width = 0.125
New_Colors = ['red','orange','yellow','green']

# Plot the dataframe on axes
plt.bar(['High Risk', 'Medium Risk', 'Low Risk', 'No Risk'], [N1, N2, N3, N4], width, color=New_Colors)
plt.title('Flood Risk Summary', fontsize=14)
plt.xlabel('Flood Risk', fontsize=14)
plt.ylabel('Number of Properties', fontsize=14)
plt.grid(True)
plt.savefig('Flood Risk Summary Graph.png')
