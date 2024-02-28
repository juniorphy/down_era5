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
#        'pressure_level': [
#             '10', ' 50', '70',
#            '100', '125', '150',
#            '175', '200', '225',
#            '250', '300', '350',
#            '400', '450', '500',
#            '550', '600', '650',
#            '700', '750', '775',
#            '800', '825', '850',
#            '875', '900', '925',
#            '950', '975','1000',
#        ],
        'year': str(year),
        'month':
            months
        ,
        'time': '00:00',
#        'area': [
#            90, -180, -90,
#                 180,
#        ],
        'format': 'netcdf',
    },
    f'era5_sst_monthly_sep-oct-nov_{year}.nc')

year=args.year

print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

for YY in range(year,year+1):
    print("Download year: ", YY,'\n')

    get_era('sea_surface_temperature', None, year=YY, months=['09','10','11'])
    print()

print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

