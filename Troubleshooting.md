# Troubleshooting
# Error - 
Traceback (most recent call last):
  File "c:/Users/marie/Documents/EGM722/egm722_project/flood_map_script.py", line 66, in <module>
    stock_data = pd.read_csv('housing_stock.csv') #user to input file path to their stock data csv
  File "C:\Users\marie\anaconda3\envs\EGM722\lib\site-packages\pandas\util\_decorators.py", line 311, in wrapper
    return func(*args, **kwargs)
  File "C:\Users\marie\anaconda3\envs\EGM722\lib\site-packages\pandas\io\parsers\readers.py", line 680, in read_csv
    return _read(filepath_or_buffer, kwds)
  File "C:\Users\marie\anaconda3\envs\EGM722\lib\site-packages\pandas\io\parsers\readers.py", line 575, in _read
    parser = TextFileReader(filepath_or_buffer, **kwds)
  File "C:\Users\marie\anaconda3\envs\EGM722\lib\site-packages\pandas\io\parsers\readers.py", line 933, in __init__
    self._engine = self._make_engine(f, self.engine)
  File "C:\Users\marie\anaconda3\envs\EGM722\lib\site-packages\pandas\io\parsers\readers.py", line 1217, in _make_engine
    self.handles = get_handle(  # type: ignore[call-overload]
  File "C:\Users\marie\anaconda3\envs\EGM722\lib\site-packages\pandas\io\common.py", line 789, in get_handle
    handle = open(
FileNotFoundError: [Errno 2] No such file or directory: 'housing_stock.csv'
# Reason - 
This error has occurred because the housing stock CSV in the local folder has a different name than the file being called in the code. 
# Solution – 
Try renaming the housing stock CSV to ‘housing_stock.csv’. Alternatively, change line 66 in the code to match the CSV file in your local folder. Double-check that the file is in CSV format, if not, go to file, save as, and change the file type to CSV. NB: If you are changing an excel workbook to CSV which has multiple sheets, only the current sheet will save as CSV.

# Error-
Traceback (most recent call last):
  File "c:/Users/marie/Documents/EGM722/egm722_project/flood_map_script.py", line 68, in <module>
    stock_data['geometry']=list(zip(stock_data['xlong'], stock_data['ylat'])) #user to change attribute name according to csv
  File "C:\Users\marie\anaconda3\envs\EGM722\lib\site-packages\pandas\core\frame.py", line 3505, in __getitem__
    indexer = self.columns.get_loc(key)
  File "C:\Users\marie\anaconda3\envs\EGM722\lib\site-packages\pandas\core\indexes\base.py", line 3623, in get_loc
    raise KeyError(key) from err
KeyError: 'xlong'
# Reason - 
This error has occurred because the Longitude and Latitude columns in the housing stock CSV file have different names than those defined in the code (xlong, ylat).
# Solution – 
Identify Longitude and Latitude columns in the housing stock CSV file and replace the column names with those in the code - xlong, ylat. Alternatively, change line 68 in the code to match the column names in your CSV file.

# Error - 
The code ran correctly, but the output map image doesn’t quite look right.
# Solution – 
Check that you have correctly identified the Longitude and Latitude columns. In this case, the columns were labelled the wrong way around, resulting in a map error. Another possible cause of an error like this is that the Longitude and Latitude values are not in the correct projection/format, i.e., Easting and Northing. Try using an online converter such as http://www.nearby.org.uk/.

# Error - 
Traceback (most recent call last):
  File "c:/Users/marie/Documents/EGM722/egm722_project/flood_map_script.py", line 159, in <module>    np.savetxt('housing_stock_flood_data.csv', housing_stock_flood, delimiter=",", fmt="%s")
  File "<__array_function__ internals>", line 180, in savetxt
  File "C:\Users\marie\anaconda3\envs\EGM722\lib\site-packages\numpy\lib\npyio.py", line 1383, in savetxt
    open(fname, 'wt').close()
PermissionError: [Errno 13] Permission denied: 'housing_stock_flood_data.csv'
# Reason - 
The Map image was successfully created but the code has produced an error when creating the output CSV file. This has occurred because the file is open or running elsewhere and the code cannot overwrite the file.
# Solution – 
Ensure that the CSV file is not open on your desktop or being used in another program. 
