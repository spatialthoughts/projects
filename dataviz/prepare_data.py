"""Convert the course data to small web-ready files for the dashboard.

Usage: python prepare_data.py <download_dir>
"""
import sys
import geopandas as gpd
import pandas as pd

src = sys.argv[1]
gpkg = f'{src}/karnataka.gpkg'

districts = gpd.read_file(gpkg, layer='karnataka_districts').to_crs('EPSG:4326')
roads = gpd.read_file(gpkg, layer='karnataka_highways').to_crs('EPSG:4326')

# Simplify geometries (~10 m tolerance) to keep file sizes small for the web
districts['geometry'] = districts.simplify(0.0001)
roads['geometry'] = roads.simplify(0.0001)

lengths = pd.read_csv(f'{src}/highway_lengths_by_district.csv')

# Write everything as JavaScript variables so index.html can load it with a
# <script> tag. This works even when the page is opened directly from disk.
with open('data/data.js', 'w') as f:
    f.write(f'const DISTRICTS = {districts.to_json()};\n')
    f.write(f'const HIGHWAYS = {roads[["geometry"]].to_json()};\n')
    f.write(f'const LENGTHS = {lengths.to_json(orient="records")};\n')
