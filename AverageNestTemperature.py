"""
The aim of this script is to compute the average nest temperature 
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

###

# Import the first csv file as a start
#V11 = pandas.read_csv('V11.csv', sep = ',', header = None, names = ['Timestamp', 'Unit', 'Integer', 'Fractional'], dtype = 'str', skiprows = 20, index_col = 0, parse_dates = True, dayfirst = True)
#print(pandas.DataFrame.head(V11))
#print(V11.dtypes)

# Merge the 'Integer' and 'Fractional' columns to a 'Temperature' column
#V11['Temperature'] = V11[['Integer', 'Fractional']].apply(lambda x: '.'.join(x.fillna('').map(str)), axis=1)
#V11['Temperature'] = V11['Temperature'].str.strip('.')
#print(pandas.DataFrame.head(V11))

# Delete the columns 'Unit', 'Integer', and 'Fractional'
#V11 = V11.drop(['Unit', 'Integer', 'Fractional'], axis=1)
#print(pandas.DataFrame.head(V11))

# Convert the data types to Date and Float
#V11['Temperature'] = V11.Temperature.astype(float)
#print(pandas.DataFrame.head(V11))

#print(V11.dtypes)

###

# Add a column 'DayOrNight'
#sun = ephem.Sun()
#observer = ephem.Observer()
# Define coordinates
#observer.lat, observer.lon, observer.elevation = '55.695', '13.447', 0

# Try on a single row
# Set the time (UTC)
#observer.date = ephem.Date(V11.index[0])
#sun.compute(observer)
#if sun.alt*180/math.pi < -6:
#	print('night')
#else:
#	print('day')
	
# Iterate over the dataframe
#V11['DayOrNight'] = ''
#for index, row in V11.iterrows():
	# Set the time (UTC)
#	observer.date = ephem.Date(index)
#	sun.compute(observer)
#	if sun.alt*180/math.pi < -6:
#		V11['DayOrNight'][index] = 'night'
#	else:
#		V11['DayOrNight'][index] = 'day'
#print(pandas.DataFrame.head(V11))

###

# Calculate the daily average temperature separately for civil days and civil nights
#TwilightAv = V11.groupby(['DayOrNight']).resample('D').mean()
#print(TwilightAv)
# Reset index 'day' or 'night' as a column
#TwilightAv.reset_index(level=0, inplace=True) 
#print(TwilightAv)

###

# Read multiple csv into multiple dataframes
NestNumbers = [11, 17, 28, 35, 37, 43, 85, 86, 87, 103, 110, 124, 136, 138, 141, 156, 162, 165, 191, 192, 216, 227, 306, 326, 330, 336, 340, 354, 371, 376, 385]
nests = {i: pandas.read_csv('/Users/jvddorpe/Desktop/PiedFlycatchers/NestTemperatureFiles/V{}.csv'.format(i), sep = ',', header = None, names = ['Timestamp', 'Unit', 'Integer', 'Fractional'], dtype = 'str', skiprows = 20, index_col = 0, parse_dates = True, dayfirst = True) for i in NestNumbers}
print(pandas.DataFrame.head(nests[11]))
print(nests[11].dtypes)

# Get the dataframes ready before adding a column 'DayOrNight'
def get_df_ready(NestNumber):
	# Merge the 'Integer' and 'Fractional' columns into a 'Temperature' column
	nests[NestNumber]['Temperature'] = nests[NestNumber][['Integer', 'Fractional']].apply(lambda x: '.'.join(x.fillna('').map(str)), axis=1)
	nests[NestNumber]['Temperature'] = nests[NestNumber]['Temperature'].str.strip('.')
	# Delete the columns 'Unit', 'Integer', and 'Fractional'
	nests[NestNumber] = nests[NestNumber].drop(['Unit', 'Integer', 'Fractional'], axis=1)
	# Convert the data types to Date and Float
	nests[NestNumber]['Temperature'] = nests[NestNumber].Temperature.astype(float)
	return(nests[NestNumber])

for NestNumber in NestNumbers:
	get_df_ready(NestNumber)

print(nests[17])
print((nests[17]).describe())

# Add a column 'DayOrNight' to each dataframe
sun = ephem.Sun()
observer = ephem.Observer()
# Define coordinates
observer.lat, observer.lon, observer.elevation = '55.695', '13.447', 0

def day_or_night(NestNumber):
	nests[NestNumber]['DayOrNight'] = ''
	for index, row in nests[NestNumber].iterrows():
		# Set the time (UTC)
		observer.date = ephem.Date(index)
		sun.compute(observer)
		if sun.alt*180/math.pi < -6:
			nests[NestNumber]['DayOrNight'][index] = 'night'
		else:
			nests[NestNumber]['DayOrNight'][index] = 'day'
	return(nests[NestNumber])

for NestNumber in NestNumbers:
	day_or_night(NestNumber)

print(pandas.DataFrame.head(nests[28]))

# Compute the daily average temperature separately for civil days and civil nights
def twilight_av(NestNumber):
	nests[NestNumber] = nests[NestNumber].groupby(['DayOrNight']).resample('D').mean()
	nests[NestNumber].reset_index(level=0, inplace=True)
	return(nests[NestNumber])

for NestNumber in NestNumbers:
	twilight_av(NestNumber)

print(pandas.DataFrame.head(nests[35]))

# Round temperature to 3 decimals
for NestNumber in NestNumbers:
	nests[NestNumber].Temperature = nests[NestNumber].Temperature.round(3)

# Export dataframes as csv to import them more easily afterwards
nests = {i: nests[i].to_csv('/Users/jvddorpe/Desktop/PiedFlycatchers/NestTemperatureFiles/nestV{}.csv'.format(i), sep = ',', encoding='utf-8') for i in NestNumbers}