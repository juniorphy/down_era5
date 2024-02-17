import cdsapi

c = cdsapi.Client()

def get_era(var=str, pres_levels=list, year=int, month=int):
    #if len(date) :
       
    #year=int(date[:4])
    #month=int(date[4:6])
    #day=int(date[6:8])
    c.retrieve(
    'reanalysis-era5-pressure-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': [
            'vertical_velocity',
        ],
        'pressure_level': [
             '3','10', '50'
            '100', '125', '150',
            '175', '200', '225',
            '250', '300', '350',
            '400', '450', '500',
            '550', '600', '650',
            '700', '750', '775',
            '800', '825', '850',
            '875', '900', '925',
            '950', '975', '1000',
        ],
        'year': f'{year}',
        'month': f'{month:02d}',
        'day': [f'{day:02d}'
        ],
        'time': [
            '00:00', '03:00' 
            '06:00', '09:00', 
            '12:00', '15:00', 
            '18:00', '21:00', 
        ],
        'area': [
            -80, -20, -60,
            -20,
        ],
    },
    'download.nc')

get_era('temperature',[1000],'20230101')


