import cdsapi
import argparse
from datetime import datetime
parser = argparse.ArgumentParser()
parser.add_argument('--year',type=int,
                    help='year for download')

args = parser.parse_args()

c = cdsapi.Client()

def get_era(var=str, pres_levels=list, year=int, months=list):
    #year=int(date[:4])
    #month=int(date[4:6])
    #day=int(date[6:8])

    c.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
         {
        'product_type': 'monthly_averaged_reanalysis',
        'variable': var,
        'year': str(year),
        'month': months
        ,
        'time': '00:00',
        'grid': [0.5, 0.5],
#        'area': [
#            90, -180, -90,
#                 180,
#        ],
        'format': 'netcdf',
    },
    f'era5_sst_monthly_{year}_0p5.nc')

year=args.year

print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
months=[]
for YY in range(year,year+1):
    print("Download year: ", YY,'\n')
    months = [f"{ff:02d}" for ff in range(1,13)]
    get_era('sea_surface_temperature', None, year=YY, months=months)
    print()

print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


