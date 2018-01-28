
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[1]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd


def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[2]:

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')

df['M_D'] = df['Date'].apply(lambda x:  x[5:])
df = df[df['M_D'] != '02-29'].copy()
df.set_index("M_D",inplace=True)


# In[3]:

df['Date'] = df ['Date'].apply(pd.to_datetime)
df['dayofyear'] = df ['Date'].apply(lambda x: x.dayofyear)


# In[4]:

import numpy as np
get_ipython().magic('matplotlib notebook')


print(df[df["Data_Value"]==np.min(df["Data_Value"])])
doymin = df[(df['Element'] == 'TMIN')&(df['Date'] >= '2005-01-01') & (df['Date'] <= '2014-12-31')].groupby(level=0).aggregate({'Data_Value':np.min,'dayofyear':np.min})
doymax = df[(df['Element'] == 'TMAX')&(df['Date'] >= '2005-01-01') & (df['Date'] <= '2014-12-31')].groupby(level=0).aggregate({'Data_Value':np.max,'dayofyear':np.min})

doymin2015 = df[(df['Element'] == 'TMIN')&(df['Date'] >= '2015-01-01')&(df['Date'] <= '2015-12-31')].groupby(level=0).aggregate({'Data_Value':np.min,'dayofyear':np.min})
doymax2015 = df[(df['Element'] == 'TMAX')&(df['Date'] >= '2015-01-01')&(df['Date'] <= '2015-12-31')].groupby(level=0).aggregate({'Data_Value':np.max,'dayofyear':np.min})


recbreakmin = doymin2015[doymin2015["Data_Value"] < doymin["Data_Value"]]
recbreakmax = doymax2015[doymax2015["Data_Value"] > doymax["Data_Value"]]



# In[21]:

plt.plot(doymin.dayofyear,doymin.Data_Value,"skyblue",doymax.dayofyear,doymax.Data_Value,"goldenrod",alpha=0.8)
plt.scatter(recbreakmin.dayofyear,recbreakmin.Data_Value,c="b",marker='v',s=40,alpha=0.5)
plt.scatter(recbreakmax.dayofyear,recbreakmax.Data_Value,c="r",marker='^',s=40,alpha=0.5)
plt.gca().fill_between(range(len(doymin)), doymin['Data_Value'], doymax['Data_Value'], facecolor = 'gray', alpha = 0.2)
plt.xlabel('Day of the Year')
plt.ylabel('Temperature (Tenths of Degrees C)')
plt.title('Temperature Summary plot')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.legend(['2005-2014 Rec Low', '2005-2014 Rec High', '2015 Rec Low','2015 Rec High'])
plt.savefig()


# 

# In[ ]:




# In[ ]:



