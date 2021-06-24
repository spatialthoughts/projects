from qgis.utils import iface

layer_id = '[%@layer_id%]'
qa_field_name = 'checked'
layer = QgsProject().instance().mapLayer(layer_id)
field = layer.fields().lookupField(qa_field_name)

with edit(layer):
    layer.changeAttributeValue([%$id%], field, 'Y')
    iface.messageBar().pushInfo('Success', 'Field Value Updated')