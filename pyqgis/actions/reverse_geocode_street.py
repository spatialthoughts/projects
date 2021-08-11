"""
PyQGIS Code to be used in a QGIS Python Action for 
Reverse Geocoding a point layer using a street network

This action to be defined on the point layer
"""
import math
from qgis.utils import iface
from qgis.core import QgsSpatialIndex, QgsVectorLayer
from PyQt5.QtCore import QVariant

street_layer = 'Street'
street_layer_name_attr = 'NAME'
left_from_field = 'L_F_ADD'
left_to_field = 'L_T_ADD'
right_from_field = 'R_F_ADD'
right_to_field = 'R_T_ADD'
address_attribute_name = 'ADDRESS'

# Point layer to reverse geocode
point_layer = QgsProject.instance().mapLayer('[% @layer_id %]')
fid = [% $id %]
feature = point_layer.getFeature(fid)
geometry = feature.geometry()

# Street layer
street_layer = QgsProject.instance().mapLayersByName(street_layer)[0]

# Use Spatial Index to find nearest features 
index = QgsSpatialIndex(street_layer.getFeatures())
# Get 5 nearest features based on the spatial index
nearestids = index.nearestNeighbor(geometry, 5)
nearest_distance = 9999
# Iterate over candidate features and find the nearest one
for f in street_layer.getFeatures(QgsFeatureRequest(nearestids)):
    distance = geometry.distance(f.geometry())
    if distance < nearest_distance:
        nearest_feature = f

# Now we have the nearest line
# Determine which side of the street is the address point
point = geometry.asPoint()
point_in_line = nearest_feature.geometry().closestSegmentWithContext(point)[1]

out = nearest_feature.geometry().closestSegmentWithContext(point)
# out is a tuple. Last item indicates relative direction of the point
direction = out[-1]

if direction < 0:
    side = 'Left'
else:
    side = 'Right'
print('Address is on the {}'.format(side))    

# Locate the nearest point on the line segment
street_name = nearest_feature[street_layer_name_attr]
nearest_geometry = nearest_feature.geometry()
nearest_point = nearest_geometry.nearestPoint(geometry)

# Measure how far along is the nearest point from start of geometry
distance = nearest_geometry.lineLocatePoint(nearest_point)
length = nearest_geometry.length()

print('Point is at {:.0%} from start'.format(distance/length))
attributes = nearest_feature.attributes()

# Find min and max range of addresses
if side == 'Left':
    from_add = int(nearest_feature[left_from_field])
    to_add = int(nearest_feature[left_to_field])
else:
    from_add = int(nearest_feature[right_from_field])
    to_add = int(nearest_feature[right_to_field])
print('from', from_add, 'to', to_add)

# Interpolate the address and round up to nearest integer
interpolated = from_add + ((to_add - from_add)*distance)/length

rounded = math.ceil(interpolated)

if side == 'Left' and rounded % 2 == 0:
    streetnum = rounded + 1
elif side == 'Left' and rounded % 2 !=0:
    streetnum = rounded
elif side == 'Right' and rounded % 2 == 0:
    streetnum = rounded
elif side == 'Right' and rounded % 2 != 0:
    streetnum = rounded + 1

address = '{:.0f}, {}'.format(streetnum, street_name)
side = '{} side of street'.format(side)
message = '{}, ({})'.format(address, side)
iface.messageBar().pushMessage(message)

# Create a point layer showing the nearest point whose address we determined
vlayer = QgsVectorLayer('Point?crs=EPSG:2274', 'point', 'memory')
provider = vlayer.dataProvider()
provider.addAttributes([QgsField(address_attribute_name, QVariant.String)])
vlayer.updateFields() 

f = QgsFeature()
f.setGeometry(nearest_point)
f.setAttributes([address])
provider = vlayer.dataProvider()
provider.addFeature(f)
vlayer.updateExtents() 
QgsProject.instance().addMapLayer(vlayer)
iface.setActiveLayer(point_layer)
