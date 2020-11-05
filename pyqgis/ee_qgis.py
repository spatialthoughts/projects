# imports and constants
import ee
from ee_plugin import Map
import json

ee.Initialize()
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA').filterDate('2019-01-01', '2019-12-31');
composite = collection.median();

composite_ndvi = composite.normalizedDifference(['B5','B4']);

palette = [
  'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718',
  '74A901', '66A000', '529400', '3E8601', '207401', '056201',
  '004C00', '023B01', '012E01', '011D01', '011301']

# Replace the Layer Name 'layer' with the actual layer name
layer = QgsProject.instance().mapLayersByName('layer')[0]
geometry = json.loads(layer.getFeatures().__next__().geometry().asJson())
polygon = ee.Geometry.MultiPolygon(geometry['coordinates'])
Map.addLayer(composite.clip(polygon), {'bands': ['B4', 'B3', 'B2'], 'min':0, 'max': 0.4, 'gamma': 1.2}, 'Image')

Map.addLayer(composite_ndvi.clip(polygon), {'min': 0, 'max': 1, 'palette': palette}, 'Clipped NDVI');
