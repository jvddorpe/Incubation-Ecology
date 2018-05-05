"""
The aim of this script is to compute the average nest temperature 
for each day and night,
day and night being delimited by sunrise and sunset times.
"""

import os
import pandas
import numpy
import ephem
import math
import datetime

# Set the working directory
os.chdir('/Users/jvddorpe/Desktop/PiedFlycatchers/AmbientTemperatureFiles')

# Read multiple csv into multiple dataframes
IDs = ['13_13BDB141', '13_183DA241', '17_2445A841', '09-20170913h']
AmbientTempFiles = {i: pandas.read_csv('/Users/jvddorpe/Desktop/PiedFlycatchers/AmbientTemperatureFiles/20{}.csv'.format(i), sep = ',', header = None, names = ['Timestamp', 'Unit', 'Integer', 'Fractional'], dtype = 'str', skiprows = 20, index_col = 0, parse_dates = True, dayfirst = True) for i in IDs}
print(pandas.DataFrame.head(AmbientTempFiles['13_13BDB141']))
print(AmbientTempFiles['13_13BDB141'].dtypes)
print(AmbientTempFiles['13_13BDB141'])

AmbientTempFiles['09-20170913h'] = AmbientTempFiles['09-20170913h'].dropna(subset = ['Fractional', 'Integer'])
print(AmbientTempFiles['09-20170913h'])

# Get the dataframes ready before adding a column 'DayOrNight'
def get_df_ready(ID):
	# Merge the 'Integer' and 'Fractional' columns into a 'Temperature' column
	AmbientTempFiles[ID]['Temperature'] = AmbientTempFiles[ID][['Integer', 'Fractional']].apply(lambda x: '.'.join(x.fillna('').map(str)), axis=1)
	AmbientTempFiles[ID]['Temperature'] = AmbientTempFiles[ID]['Temperature'].str.strip('.')
	# Delete the columns 'Unit', 'Integer', and 'Fractional'
	AmbientTempFiles[ID] = AmbientTempFiles[ID].drop(['Unit', 'Integer', 'Fractional'], axis=1)
	# Convert the data types to Date and Float
	AmbientTempFiles[ID]['Temperature'] = AmbientTempFiles[ID].Temperature.astype(float)
	return(AmbientTempFiles[ID])

for ID in AmbientTempFiles:
	get_df_ready(ID)

print(AmbientTempFiles['13_183DA241'])
print((AmbientTempFiles['13_183DA241']).describe())

# Add a column 'DayOrNight' to each dataframe
sun = ephem.Sun()
observer = ephem.Observer()
# Define coordinates
observer.lat, observer.lon, observer.elevation = '55.695', '13.447', 0

def day_or_night(ID):
	AmbientTempFiles[ID]['DayOrNight'] = ''
	for index, row in AmbientTempFiles[ID].iterrows():
		# Set the time (UTC)
		observer.date = ephem.Date(index)
		sun.compute(observer)
		if sun.alt*180/math.pi < -6:
			AmbientTempFiles[ID]['DayOrNight'][index] = 'night'
		else:
			AmbientTempFiles[ID]['DayOrNight'][index] = 'day'
	return(AmbientTempFiles[ID])

for ID in AmbientTempFiles:
	day_or_night(ID)

print(pandas.DataFrame.head(AmbientTempFiles['17_2445A841']))

# Compute the daily average temperature separately for civil days and civil nights
def twilight_av(ID):
	AmbientTempFiles[ID] = AmbientTempFiles[ID].groupby(['DayOrNight']).resample('D').mean()
	AmbientTempFiles[ID].reset_index(level=0, inplace=True)
	return(AmbientTempFiles[ID])

for ID in AmbientTempFiles:
	twilight_av(ID)

print(pandas.DataFrame.head(AmbientTempFiles['13_13BDB141']))

# Round temperature to 3 decimals
for ID in AmbientTempFiles:
	AmbientTempFiles[ID].Temperature = AmbientTempFiles[ID].Temperature.round(3)

# Export dataframes as csv to import them more easily afterwards
AmbientTempFiles = {i: AmbientTempFiles[i].to_csv('/Users/jvddorpe/Desktop/PiedFlycatchers/AmbientTemperatureFiles/AmbientTemperatureFile_20{}.csv'.format(i), sep = ',', encoding='utf-8') for i in IDs}