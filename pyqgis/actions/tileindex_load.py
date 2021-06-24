from qgis.utils import iface

path = '[%location%]'
iface.addRasterLayer(path)

index_layer_name = 'index'
index_layer = QgsProject.instance().mapLayersByName(index_layer_name)[0]
iface.setActiveLayer(index_layer)
