import ee
from ee_plugin import Map
import json

ee.Initialize()

bounds = iface.mapCanvas().extent()
xMin = bounds.xMinimum()
yMin = bounds.yMinimum()
xMax = bounds.xMaximum()
yMax = bounds.yMaximum()
geometry = ee.Geometry.Rectangle([xMin, yMin, xMax, yMax])

dataset = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
    .filter(ee.Filter.date('2021-01-01', '2022-01-01')) \
    .filter(ee.Filter.bounds(geometry))

image = dataset.median()

visParams = {
    'min':0,
    'max':10000,
    'bands': ['SR_B4', 'SR_B3', 'SR_B2']
}
Map.addLayer(image, visParams, 'Image')
