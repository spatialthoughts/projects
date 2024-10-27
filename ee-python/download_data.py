"""This script is an example of automating a download
using Google Earth Engine API.

This script computes the average soil moisture for the
past 1-week over all districts in a state. The result 
is then downloaded as a JSON file and saved locally.

The Python environment needs to have earthengine-api
package installed. After install, a one-time authentication
needs to be completed using 'earthengine authenticate'
command.
"""
import ee
import json
import os

# Replace the cloud_project with your own project
cloud_project = 'spatialthoughts'

try:
    ee.Initialize(project=cloud_project)
except:
    ee.Authenticate()
    ee.Initialize(project=cloud_project)

# Get current date and convert to milliseconds 
end_date = ee.Date(datetime.datetime.now().timestamp()*1000)
start_date = end_date.advance(-1, 'week')

date_string = end_date.format('YYYY_MM_dd')
filename = 'ssm_{}.geojson'.format(date_string.getInfo())

# Saving to current directory. You can change the path to appropriate location
output_path = os.path.join(filename)

# Datasets
soilmoisture = ee.ImageCollection("NASA_USDA/HSL/SMAP10KM_soil_moisture")
admin2 = ee.FeatureCollection("FAO/GAUL_SIMPLIFIED_500m/2015/level2")

# Filter to a state
karnataka = admin2.filter(ee.Filter.eq('ADM1_NAME', 'Karnataka'))

# Select the ssm band
ssm  = soilmoisture.select('ssm')

filtered = ssm .filter(ee.Filter.date(start_date, end_date))

mean = filtered.mean()

stats = mean.reduceRegions(**{
  'collection': karnataka,
  'reducer': ee.Reducer.mean().setOutputs(['meanssm']),
  'scale': 10000,
  })

# Select columns to keep and remove geometry to make the result lightweight
# Change column names to match your uploaded shapefile
columns = ['ADM2_NAME', 'meanssm']
exportCollection = stats.select(**{
    'propertySelectors': columns,
    'retainGeometry': False})

# Get the result from the server
output = json.dumps(exportCollection.getInfo())

with open(output_path, 'w') as f:
    f.write(output)
    print('Success: File written at', output_path)
    
