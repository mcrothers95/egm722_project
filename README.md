# EGM722: Programming for GIS and Remote Sensing project
# Housing Stock Flood Analysis
# Marie-Claire Crothers B00666261

This code focuses on a basic flood risk analysis of housing stock based on each property’s distance from a river. When run, the code attributes each property with a distance from the river and groups the data into 4 risk categories from ‘High Risk’ to ‘No Risk’. This code outputs a stock map showing the housing stock flood data in PNG format, an updated CSV stock list with the newly attributed flood data and a summary bar graph image. 

The Housing Stock Flood Analysis script requires an organisation’s stock data in CSV format, which includes Longitude and Latitude columns in CRS EPSG:32629. The files required to run the analysis, as well as example stock data, are included in the Git repository - https://github.com/mcrothers95/egm722_project. 

# Dependencies
•	python 3.7 and above
•	geopandas
•	cartopy
•	rasterio
•	numpy
•	matplotlib
•	contextily

# Installation 
To install and run the Housing Stock Flood Analysis code, you are required to have Anaconda and git installed. This will allow you to fork the repository and clone it to your computer. If you do not already have one on your computer, an IDE should also be installed. This will allow you to view, run, and alter the code to interact with your datasets and create the outputs. The IDE used in the creation of the code was Microsoft Visual Studio.
Required software installation documentation can be found here – 
•	Git - https://git-scm.com/downloads
•	GitHub  - https://github.com/git-guides/install-git (Installing GitHub Desktop will also install the latest version of Git - https://desktop.github.com/.)
•	Anaconda - https://docs.anaconda.com/anaconda/install/index.html
•	Microsoft Visual Studio - https://visualstudio.microsoft.com/downloads/

# Forking the Repository
If not already present on your computer, install git and GitHub. The required files for the Housing Stock Flood Analysis code are hosted on GitHub, you will need to create an account if you do not already have one. Once complete, go to https://github.com/mcrothers95/egm722_project, which is the remote repository location for the Housing Stock Flood Analysis code files.
Fork the repository to your git account, take a note of the URL, and open GitHub Desktop. Here, log in to the account used to fork the repository. Use Ctrl+Shift+O to open the clone repository options. Click on the URL tab and enter the URL from earlier. Navigate to a local folder in which to save the data and click Clone.

# Setting up Anaconda
Open the Anaconda Navigator – follow the installation instructions if not already set up - and create a new environment. Click on the Import button and navigate to the ‘environment.yml’ file in the local folder in which you cloned the repository. Click Import and this will set up the environment by installing the packages and their additional dependencies required for the Housing Stock Flood Analysis code.

# Opening the Script in an IDE
In the home tab in Anaconda, set the ‘Applications on’ drop-down menu to the environment you created in the previous section – this will change the installed applications to those needed to run the Housing Stock Flood Analysis code. Launch the IDE of choice through Anaconda and open the ‘flood_map_script.py’ from the cloned folder on your local drive. 

# Getting the Script Ready to Run
The cloned repository on your local drive has the files required for the flood analysis, stored within the ‘data_files’ folder. Within this folder there are the following shapefiles:
•	NI Outline Polygon Layer
•	NI Towns Point Layer
•	NI Rivers Line Layer
•	NI Water Bodies Polygon Layer
•	NI Rivers Buffer Polygon Layer
These shapefiles are displayed in the output flood map and are used to run the analysis. The output map is set to A4 landscape size, but this part of the code can be altered to suit the user’s needs. 
In the cloned files on your local system, you will also find an example dataset called ‘housing_stock.csv’ – this is an example of housing stock data to demonstrate how the analysis works and to create example outputs. This file is read within the script and is plotted spatially using the Longitude and Latitude attributes present within the data. The existing housing stock example file can be replaced with the user’s data by placing the new housing stock data in this folder and renaming it to match the existing file – alternatively, the file name can be altered within the code to ensure the correct file is being called for analysis. The user’s data must be in CSV format and must have a Longitude and a Latitude column (called ylat and xlong respectively – again, the names within the code can also be altered to match that of the data in the CSV) with the correct spatial information present for each point. It is important to note that the spatial data must be in the Coordinate Reference System (CRS) EPSG:32629 to display properly on the output map and for the spatial analysis to run correctly. The user’s data may be required to be converted to the correct CRS before running the Housing Stock Flood Analysis code.
If the dataset is missing this spatial information, then the code will be unable to plot the data points and run the analysis. If the user does not have precise Longitude and Latitude information available to them, but still wishes to run the flood analysis on their housing stock data, an online postcode converter can be used to give the coordinates of the centre of a postcode area in which their property is located. The analysis will not be as accurate but may still offer an informative insight into the user’s housing stock. 
Once the user has prepared and replaced the housing stock data with their own, the Housing Stock Flood Analysis code is ready to run.
