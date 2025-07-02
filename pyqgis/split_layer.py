# A PyQGIS script to split a layer into multiple GeoPackage files based on Admin2 and Admin3 fields.
# This script assumes that the active layer in QGIS has fields named 'Admin2' and 'Admin3'.
# It creates a folder structure based on Admin2 values and saves each Admin3 feature as a separate GeoPackage file.

# Script to be run from Python Console in QGIS
# Tested on dataset ka_admin_boundaries.gpkg
import os

layer = iface.activeLayer()
field_names = [field.name() for field in layer.fields()]

admin2_field = 'Admin2'
admin3_field = 'Admin3'

# Relative path to the root folder where GeoPackage files will be saved
root_folder = 'admin_boundaries'

for feature in layer.getFeatures():
    admin2 = feature[admin2_field]
    admin3 = feature[admin3_field]
    # Create Admin2 folder
    admin2_folder = os.path.join(root_folder, str(admin2))
    if not os.path.exists(admin2_folder):
        os.makedirs(admin2_folder)
        print(f"Created Admin2 folder: {admin2_folder}")
    # Create GeoPackage filename
    gpkg_filename = f"{admin3}.gpkg"
    gpkg_path = os.path.join(admin2_folder, gpkg_filename)
    print(gpkg_path)
    feature_id = feature.id()
    new_layer = layer.materialize(
        QgsFeatureRequest().setFilterFids([feature_id]))
    
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.layerName = f'{admin3}'
    QgsVectorFileWriter.writeAsVectorFormat(
        new_layer, 
        gpkg_path, 
        options
    )
    print(f'Created {gpkg_path}')
