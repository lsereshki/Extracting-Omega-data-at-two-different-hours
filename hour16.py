#getting omega values from a netCDF file for a special domain with definit latitudes and longitudes for 30 days of months April to December 2021 and showing them in csv format.
#Data got from ERA5 at 1 hpa

from netCDF4 import num2date
import cftime
import netCDF4
import numpy as np
import pandas as pd
from netCDF4 import Dataset

f = Dataset ('/home/lida/Desktop/11Day/omeganew/hour16.nc')

omega = f.variables['w']

time = f.variables ['time']
latitudes = f.variables ['latitude']
longitudes = f.variables ['longitude']

time = num2date (time[:], units=time.units)

def domain_bounderies(year, month, day, lat1, lon1):
    

    latitude = latitudes[:] == lat1
    l = len(time)
    
    #cftime.DatetimeGregorian just gives the data @ hour 0 so in order to get data for other hours:
     
    times = [] 

    for i in range(l):
       if ((time[i].year == year and time[i].month == month) and time[i].day == day):
            times.append(True)
            
       else:
            times.append(False)

    longitude = longitudes[:] == lon1

    times_grid, latitudes_grid, longitudes_grid = [x.flatten() for x in np.meshgrid(time[times], latitudes[latitude], longitudes[longitude], indexing='ij')]

   
    df = pd.DataFrame({'time':times_grid, 'omega': omega[times,latitude,longitude].flatten()})
     
    return df

for month in range (4,12):    
    latlon_value = domain_bounderies(2021,month,1, 35.7, 51.3)    
    for day in range(2,29):
        
        daily = domain_bounderies(2021,month,day,35.7, 51.3)        
        latlon_value = latlon_value.append(daily)

    
    latlon_value.to_csv('/home/lida/Desktop/atan/'+ str(month) + '.csv', index=False)
 



