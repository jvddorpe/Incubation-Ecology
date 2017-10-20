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
V011 = pandas.read_csv('V011.csv', sep = ',', skiprows = 19)
# How to tell there are only 3 columns?
V011.dtypes
print(pandas.DataFrame.head(V011))