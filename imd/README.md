# Working with IMD (Indian Meteorologoical Department) Gridded Rainfall data

The notebooks in this folder are for processing [IMD New High Spatial Resolution (0.25X0.25 degree) Long Period (1901-2021) Daily Gridded Rainfall Data Set](http://imdpune.gov.in/Clim_Pred_LRF_New/Grided_Data_Download.html) Over India.

- [imd_to_geotiff.ipynb](https://github.com/spatialthoughts/projects/blob/master/imd/imd_to_geotiff.ipynb) uses `imdlib` to convert binary grid files to georeferenced GeoTiff files suitable to be used in a GIS
- [download_all.py](https://github.com/spatialthoughts/projects/blob/master/imd/download_all.py) shows how to download, convert and create annual rainfall rasters from 2901-2021.
