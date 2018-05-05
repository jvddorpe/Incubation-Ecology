
import os
import pandas
import numpy	

# Set the working directory
os.chdir('/Users/jvddorpe/Desktop/PiedFlycatchers/TemperatureFiles')

# Import the first .txt file
nestV11 = pandas.read_csv('001_Stensoffa 2013_V11_FD10041.csv', sep = ';', header = (0))
print(pandas.DataFrame.head(nestV11))
print(nestV11.dtypes)

# Delete 'Absolute Time' column
del nestV11['Absolute Time']
print(pandas.DataFrame.head(nestV11))

# Convert the column 'Begin Date Time' from object to datetime
nestV11['Begin Date Time'] =  pandas.to_datetime(nestV11['Begin Date Time'])
print(pandas.DataFrame.head(nestV11))

# Sort the data according 'Begin Time'
nestV11 = nestV11.sort_values(by = ['Begin Time (s)'])
print(pandas.DataFrame.head(nestV11))
# Reset the index
nestV11 = nestV11.reset_index(drop=True)
print(pandas.DataFrame.head(nestV11))

# Add a 'DayOrNight' column: 'Day' is the day where the first egg was laid, and the days include the sunrises, whereas the nights include the sunsets
nestV11['DayOrNight'] = 'Day'
print(pandas.DataFrame.head(nestV11))

# Get the index of all the cells in the column 'Event' as integer
events = nestV11.index.tolist()
print(events)
# Get the index of the cells 'Sunset' in the column 'Event'
sunsets = nestV11.index[nestV11['Event'] == 'Sunset'].tolist()
print(sunsets)
# Get the index of the cells 'Sunrise' in the column 'Event'
sunrises = nestV11.index[nestV11['Event'] == 'Sunrise'].tolist()
print(sunrises)

# Change 'DayOrNight' to 'Night' between sunsets (included) and sunrises (not included)
for event in events:
	for i in range(len(sunsets)):
		if sunsets[i] <= event and event < sunrises[i]:
			nestV11.at[event, 'DayOrNight'] = 'Night'
print(nestV11)

# Add a column 'DayAfterFirstEggWasLaid'
nestV11['DayAfterFirstEggWasLaid'] = len(sunrises) + 1
print(pandas.DataFrame.head(nestV11))

for event in events:
	for i in range(len(sunrises)):
		if event < sunrises[0]:
			nestV11.at[event, 'DayAfterFirstEggWasLaid'] = 1 # First day must be the day the first egg was laid
		if sunrises[i-1] <= event and event < sunrises[i]:
			nestV11.at[event, 'DayAfterFirstEggWasLaid'] = nestV11['DayAfterFirstEggWasLaid'][0] + i
print(nestV11)
print(nestV11.dtypes)

# Merge column 'DayOrNight' and 'DayAfterFirstEggWasLaid'
nestV11['DayOrNight'] = nestV11['DayOrNight'].astype('str') 
nestV11['DayAfterFirstEggWasLaid'] = nestV11['DayAfterFirstEggWasLaid'].apply(str)
print(pandas.DataFrame.head(nestV11))
print(nestV11.dtypes)
nestV11['DaysAndNights'] = nestV11['DayOrNight'].map(str) + nestV11['DayAfterFirstEggWasLaid']
print(nestV11)

# Delete columns 'DayOrNight' and 'DayAfterFirstEggWasLaid'
del nestV11['DayOrNight']
del nestV11['DayAfterFirstEggWasLaid']	
print(pandas.DataFrame.head(nestV11))
print(nestV11)


###
# Total time of a day (min)
# Total time of a night (min)
# Total off-bout duration (min)
# Total time spent actively incubating (min)
# Incubation constancy (%)
# Number of off-bouts
# Average off-bout duration (min)
# Average on-bout duration (min)
# Average Max/Min Amp (temperature) (degrees)