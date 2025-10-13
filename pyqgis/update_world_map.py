import geopandas as gpd
from qgis.core import QgsPathResolver

# Get the path to bundled the world_map.gpkg file
world_map_gpkg_path = QgsPathResolver().readPath('inbuilt:/data/world_map.gpkg')
world_map_gdf = gpd.read_file(world_map_gpkg_path, layer='countries')

# Download Countries Point-of-Views shapefile 

# Choose your country code
country_code = 'ind'

# See all the available countries POV files at
# https://www.naturalearthdata.com/blog/admin-0-countries-point-of-views/

ne_pov_base_url = 'https://naciscdn.org/naturalearth/10m/cultural/'
ne_pov_filename = f'ne_10m_admin_0_countries_{country_code}.zip'
ne_pov_file_url = ne_pov_base_url + ne_pov_filename
pov_map_gdf = gpd.read_file(ne_pov_file_url)

columns = ['NAME' ,'FIPS_10', 'ISO_A3', 'WB_A2', 'WB_A3', 'ISO_A2', 'geometry']

# Select a subset of columns and rename to match the bundled layer
pov_map_gdf_output = pov_map_gdf[columns].rename(
    columns={'FIPS_10': 'FIPS_10_', 'ISO_A2': 'iso_a2'})

# Overwrite the bundled geopackage layer
pov_map_gdf_output.to_file(world_map_gpkg_path, 
    layer='countries', driver='GPKG', mode='w')
