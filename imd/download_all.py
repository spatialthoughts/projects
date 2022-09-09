'''
Script to download GeoTIFF files of yearly rainfall
from IMD Gridded Rainfall Data.
'''
import os
import imdlib as imd
import rioxarray as xr

data_folder = r'C:\Users\ujava\Downloads\imd\data'
output_folder = r'C:\Users\ujava\Downloads\imd\geotiff'

if not os.path.exists(data_folder):
    os.makedirs(data_folder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    
start_year = 1901
end_year = 2021
variable = 'rain' # other options are ('tmin'/ 'tmax')
data = imd.get_data(variable, start_year, end_year, fn_format='yearwise', file_dir=data_folder)

for year in range(start_year, end_year+1):
    data = imd.open_data(variable, year, year,'yearwise', data_folder)
    ds = data.get_xarray()
    ds = ds.where(ds['rain'] != -999.)
    total = ds.sum('time')
    output_file = '{}.tif'.format(year)
    output_path = os.path.join(output_folder, output_file)
    total.rio.to_raster(output_path)
    print('Successfully created GeoTIFF file', output_path)