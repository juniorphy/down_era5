import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from netCDF4 import Dataset

mfs = xr.open_mfdataset('global/era5_omega_monthly_*.nc', combine='by_coords')
#mfs = xr.open_mfdataset('sst_era5/era5_sst_monthly_*.nc', combine='by_coords')

nlat=len(mfs.latitude.values) ; nlon=len(mfs.longitude.values) 
month=9

#reg = mfs.sel(latitude=slice(10,-10),level=slice(100,1000))
regclim = mfs.sel(time=slice('1991','2020'),level=slice(100,1000),latitude=slice(10,-10))
monclim = regclim.where(regclim['time.month']==month, drop=True).groupby('time.month').mean() #.where(regclim['month']==9)
#reg.coords['longitude'] = (reg.coords['longitude'] + 180) % 360 - 180
#reg = reg.sortby(reg.longitude)
#reg = reg.sortby(reg.level)
#reg = regclim.mean(dim='longitude')
monclim = monclim.mean(dim='latitude')

sst23 = mfs.sel(time=f'2023-{month}',level=slice(100,1000), latitude=slice(10,-10)).rename({'time':'month'})
sst23['month'] = sst23['month'].astype(int)
sst23['month']=monclim['month']
sst23 = sst23.mean(dim='latitude')

anom = sst23 - monclim
#anom.reindex(latitude=anom.latitude[::-1])
#anom.to_netcdf(f'anom_2023{month}_avg_10N-10S.nc',format='NETCDF4_CLASSIC' )
ncfile = Dataset(f'anom_omega_2023{month:02d}_walker.nc',mode='w', format='NETCDF4')

lat_dim = ncfile.createDimension('lat', 1)     # latitude axis
lon_dim = ncfile.createDimension('lon', nlon)    # longitude axis
lev_dim = ncfile.createDimension('lev', 27)
time_dim = ncfile.createDimension('time',1)

lat = ncfile.createVariable('lat', np.float32, ('lat',))
lat.units = 'degrees_north'
lat.long_name = 'latitude'
lon = ncfile.createVariable('lon', np.float32, ('lon',))
lon.units = 'degrees_east'
lon.long_name = 'longitude'
lev = ncfile.createVariable('lev', np.intc, ('lev',))
lev.units = 'millibars'
lev.long_name = 'pressure'
time = ncfile.createVariable('time', np.float64, ('time',))
time.units = 'months since 1989-12-01'
time.long_name = 'time'
# Define a 3D variable to hold the data
sst = ncfile.createVariable('omega',np.float64,('time','lev','lon')) 
sst.units = 'hPa/s' # degrees Kelvin
sst.standard_name = 'Omega'
nlats = len(lat_dim); nlons = len(lon_dim); ntimes = 1
# Write latitudes, longitudes.
# Note: the ":" is necessary in these "write" statements
lat[:] = 0 #anom['latitude'].values #-90. + (180./nlats)*np.arange(nlats) # south pole to north pole
#print(anom['latitude'].values)
lon[:] = anom['longitude'].values #(180./nlats)*np.arange(nlons) # Greenwich meridian eastward
lev[:] = anom['level'].values
#print(anom.level.values)
# create a 3D array of random numbers
time[:] = 0
#print(anom['w'].values.shape)
#var = np.expand_dims(anom['sst'].values,-1)
var=anom['w'].values
# Write the data.  This writes the whole 3D netCDF variable all at once.
sst[:,:,:] = var #np.squeeze(var)
ncfile.close()

exit()
lon, pressure = np.meshgrid(omega['longitude'], omega['level'])

levels = np.arange(-0.03,0.035,0.005)

# Plotting
plt.figure(figsize=(8, 6))
contour = plt.contourf(lon, pressure, anom, cmap='RdBu_r', levels=levels)
plt.colorbar(contour, label='Omega (hPa/s)', extend='both')
plt.xlabel('longitude')
plt.ylabel('Pressure (hPa)')
plt.title('Anomalia Omega Sep2023')
plt.gca().invert_yaxis()  # Invert y-axis to show pressure decreasing downwards
plt.grid(True)
plt.show()

