from qgis.utils import iface
from PyQt5.QtCore import QFileInfo

path = r'[%location%]'
layer_name = QFileInfo(path).baseName()
layer_list = QgsProject.instance().mapLayersByName(layer_name)
if layer_list:
    QgsProject.instance().removeMapLayer(layer_list[0])
    iface.mapCanvas().refresh()
