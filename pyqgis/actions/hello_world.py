from qgis.utils import iface

fid = [% $id %]
layer = QgsProject.instance().mapLayer('[% @layer_id %]')
new_layer = layer.materialize(QgsFeatureRequest().setFilterFids([fid]))
new_layer.setName('[%NAME%]')
QgsProject.instance().addMapLayer(new_layer)
iface.setActiveLayer(layer)
