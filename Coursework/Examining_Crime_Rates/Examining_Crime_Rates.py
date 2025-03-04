# -*- coding: utf-8 -*-
"""Week3DataAssignment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Yu_DV4CVQpfz_pC1I54WORdbEmfY1KKP

**Week 3 - Data Assignment**

Gabrielle Young

Questions:
- Where are different kinds of crime occurring?
- In which areas crime is growing fastest (or dropping fastest)?
- Are certain crimes more common in certain areas?


Group data by location (zip code or type of location) and examine trends within the data.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
pd.set_option('display.max_rows', None)
import datetime
from plotly.subplots import make_subplots

nRowsRead = 1000
crimedata = pd.read_csv('/content/crimestat (1) - crimestat (1).csv', delimiter=',', nrows = nRowsRead, index_col='INC NUMBER')
crimedata.dataframeName = 'crimestat (1).csv'


# I pulled this code and the pandas packages from Kaggle. https://kaggle.com/code/cassel/module-3-basics

# Preview of the data
crimedata.head(10)

"""# **Making Sense of the Data**

**Crimes by Zip Code**
"""

# renaming columns for simplicity
crimedata.rename(columns={'UCR CRIME CATEGORY': 'category', 'PREMISE TYPE': 'TYPE'}, inplace=True)

# I wanted to calucate the proportion of ALL crimes that occur within a single zip code.
zip_counts = crimedata.ZIP.value_counts()

zip_proportions = zip_counts / len(crimedata)

crimedata['zip_proportion'] = crimedata['ZIP'].map(zip_proportions)
crimedata.head(10)

"""One example this output shows is that 3.1% of all crimes within the Phoenix area occur in the 85029 zip code."""

# Grouping by ZIP code
grouped = crimedata.groupby(["ZIP"])
type(grouped)
crimedata['ZIP'] = crimedata["ZIP"].astype(str)
crimedata['ZIP'] = crimedata["ZIP"].str.strip()

# Originally I was getting an error becasue of the ZIP code's formatting issues.

# An example of a single zipcode and all crimes recorded there within this dataset.
# The 85027 zipcode represents 2.1% of all crime within the Phoenix area.
grouped.get_group('85027')

crimetype_by_Zip = grouped.category.value_counts(normalize=True)
crimetype_by_Zip.head(15)

"""I have created a dataset displaying where different types of crime are occurring. Crimes are organized by zip code (location) and category (either larceny-theft, drug offense, motor vehicle theft, aggravated assault, etc.). I have also illustrated the proportion of each crime type per zip code.

According to this data, we can see that larceny-theft crimes are most common within the 85003 zip code area.

**Crimes by Location Type**
"""

# Grouping by location TYPE
locationgrouped = crimedata.groupby(["TYPE"])
type(locationgrouped)
crimedata['TYPE'] = crimedata["TYPE"].astype(str)
crimedata['TYPE'] = crimedata["TYPE"].str.strip()

crimetype_by_Type = locationgrouped.category.value_counts(normalize=True)
crimetype_by_Type.head(20)

"""Here, I have created a dataset displaying location type where different types of crime are occurring. Crimes are organized by loation type (airport, bus station, apartment, etc.) and category (either larceny-theft, drug offense, motor vehicle theft, aggravated assault, etc.). I have also illustrated the proportion of each crime type per location type.

This displays where certain crimes are most common depending on area. For example, we can see that larceny-theft crimes are the most common type of crimes in airports.

**Crime Growth/Shrinking Rates**
"""

# Dropping NaN values to prevent errors in furture calcuations
cleancrimedata = crimedata.dropna()
cleancrimedata.head(10)
cleancrimedata['OCCURRED ON'] = pd.to_datetime(cleancrimedata['OCCURRED ON'])

# Here, I calculated the day to day change rate for crimes by location
cleancrimedata['day'] = cleancrimedata['OCCURRED ON'].dt.day

crime_trend = cleancrimedata.groupby(['ZIP', 'day']).size().reset_index(name='crime_count')

crime_trend['crime_rate_change'] = crime_trend.groupby('ZIP')['crime_count'].pct_change()

"""Crime Growing Areas"""

# Calculate crime growing areas by sorting from largest rate of change to smallest
crime_growing_areas = crime_trend.sort_values(by='crime_rate_change', ascending=False)
print(crime_growing_areas.head())

"""Here, we can see that crime rates are increasing day-to-day within the 85031 zip code.

Crime Shrinking Areas
"""

# Calculate crime shrinking areas by sorting from smallest rate of change to largest
crime_shrinking_areas = crime_trend.sort_values(by='crime_rate_change', ascending=True)
print(crime_shrinking_areas.head())

"""Here, we can see that crime rates are decreasing day-to-day within the 85043 zip code.

"""