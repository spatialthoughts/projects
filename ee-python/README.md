## Google Earth Engine Python API Code

This folder contains Scripts and Jupyter notebooks that demonstrate the working of Google Earth Engine API.

### Notebooks

- [`python_api_syntax.ipynb`](https://github.com/spatialthoughts/projects/blob/master/ee-python/python_api_syntax.ipynb): Getting started with Python API
- [`export_a_collection.ipynb`](https://github.com/spatialthoughts/projects/blob/master/ee-python/export_a_collection.ipynb): How to export all images in a collection using `ee.Task`
- [`large_gridded_exports.ipynb`](https://github.com/spatialthoughts/projects/blob/master/ee-python/large_gridded_exports.ipynb): How to created tiled exports from large images.
- [`export_image_bands.ipynb`](https://github.com/spatialthoughts/projects/blob/master/ee-python/export_image_bands.ipynb): How to export all bands of an image as separate image using `ee.Task`
- [`manage_tasks.ipynb`](https://github.com/spatialthoughts/projects/blob/master/ee-python/manage_tasks.ipynb): How to list and cancel running tasks
- [`delete_gee_assets.ipynb`](https://github.com/spatialthoughts/projects/blob/master/ee-python/delete_gee_assets.ipynb): How to delete multiple assets, including all assets within a folder/collection
- [`dynamic_visualization_parameters.ipynb`](https://github.com/spatialthoughts/projects/blob/master/ee-python/dynamic_visualization_parameters.ipynb): How to compute image statistics and use them in visualization parameters

### Scripts
- [`rename_collection.py`](https://github.com/spatialthoughts/projects/blob/master/ee-python/rename_collection.py): Renames a collection by copying the child assets to a new collection and deleting old collection recursively.
- [`download_data.py`](https://github.com/spatialthoughts/projects/blob/master/ee-python/download_data.py): How to automate downloading of data using Google Earth Engine API.
- [`asset_size.py`](https://github.com/spatialthoughts/projects/blob/master/ee-python/asset_size.py): Recursively calculate size of all assets in a folder
