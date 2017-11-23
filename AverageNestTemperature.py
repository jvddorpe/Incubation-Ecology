"""
The aim of this script is to calculate the average nest temperature 
for each day and night,
day and night being delimited by sunrise and sunset times.
"""
import os
import pandas
import ephem
import math
import datetime

# Set the working directory
os.chdir('/Users/jvddorpe/Desktop/PiedFlycatchers/NestTemperatureFiles')

# Import the first csv file as a start
V011 = pandas.read_csv('V011.csv', sep = ',', skiprows = 20, header = None, names = ['Timestamp', 'Unit', 'Integer', 'Fractional'], index_col=0, parse_dates=True, dayfirst = True)
print(pandas.DataFrame.head(V011))
print(V011.dtypes)

# Merge the 'Integer' and 'Fractional' columns to a 'Temperature' column
V011['Temperature'] = V011[['Integer', 'Fractional']].apply(lambda x: '.'.join(x.fillna('').map(str)), axis=1)
V011['Temperature'] = V011['Temperature'].str.strip('.')

# Delete the columns 'Unit', 'Integer', and 'Fractional'
V011 = V011.drop(['Unit', 'Integer', 'Fractional'], axis=1)
print(pandas.DataFrame.head(V011))

# Convert the data types to Date and Float
V011['Temperature'] = V011.Temperature.astype(float)
print(V011.dtypes)

# Add a column 'DayOrNight'
sun = ephem.Sun()
observer = ephem.Observer()
# Define coordinates
observer.lat, observer.lon, observer.elevation = '55.695', '13.447', 0

# Try on a single row
# Set the time (UTC)
observer.date = ephem.Date(V011.index[0])
sun.compute(observer)
if sun.alt*180/math.pi < -6:
	print('night')
else:
	print('day')
	
# Iterate over the dataframe
V011['DayOrNight'] = ''
for index, row in V011.iterrows():
	# Set the time (UTC)
	observer.date = ephem.Date(index)
	sun.compute(observer)
	if sun.alt*180/math.pi < -6:
		V011['DayOrNight'][index] = 'night'
	else:
		V011['DayOrNight'][index] = 'day'
print(pandas.DataFrame.head(V011))

# Calculate the daily average temperature separately for civil day and civil night
TwilightAv = V011.groupby(['DayOrNight']).resample('D').mean()
print(TwilightAv)
# Reset index 'day' or 'night' as a column
TwilightAv.reset_index(level=0, inplace=True) 
print(TwilightAv)