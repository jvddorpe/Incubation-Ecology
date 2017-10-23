# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 16:20:31 2017

@author: jvddorpe

The aim of this script is to calculate the average nest temperature 
for each day and night,
day and night being delimited by sunrise and sunset times.
"""
# Set the working directory
import os
os.chdir('/Users/jvddorpe/Desktop/PiedFlycatchers/NestTemperatureFiles')

# Import the first csv file as a start
import pandas
V011 = pandas.read_csv('V011.csv', sep = ',', skiprows = 20, header = None, names = ['Date/Time', 'Unit', 'Integer', 'Fractional'], dayfirst = True)

# Merging the 'Integer' and 'Fractional' columns to a 'Temperature' column
V011['Temperature'] = V011[['Integer', 'Fractional']].apply(lambda x: '.'.join(x.fillna('').map(str)), axis=1)
V011['Temperature'] = V011['Temperature'].str.strip('.')

# Deleting the columns 'Unit', 'Integer', and 'Fractional'
V011 = V011.drop(['Unit', 'Integer', 'Fractional'], axis=1)

# Convert the data types to Date and Float
V011['Date/Time'] = pandas.to_datetime(V011['Date/Time'])
V011['Temperature'] = pandas.to_numeric(V011['Temperature'])

# Calculate daily average temperature - WIP
V011 = V011.set_index(['Date/Time'])
V011.index = pandas.to_datetime(V011.index, unit='s')
DailyAv = V011.resample('D', how = 'mean')


print(pandas.DataFrame.head(V011))
V011.dtypes
