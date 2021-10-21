# Scripts for geeup Workflow

This scripts were written for uploading some eMODIS NDVI files to GEE via the [geeup](https://github.com/samapriya/geeup) tool.

The scripts assume the following directory structureThe scripts can be modified to suit any other dataset.

```
Desktop
│ 
└───eModis
    │   rename_files.py
    │   update_metadata.py
    └─── data
             | US_eMAH_NDVI_2020.287-293.1KM.VI_NDVI.006.2020300170330.tif
             | US_eMAH_NDVI_2020.294-300.1KM_VI_NDVI.006_2020303221006.tif
             | US_eMAH_NDVI_2020.294-307.1KM_VI_NDVI.006_2020311150401.tif
             | US_eMAH_NDVI_2020.301-307.1KM_VI_NDVI.006_2020311141002.tif
```

1. If the filenames have a `.`, the `geeup` tool can't extract the filename correctly. So we run the `rename_files.py` script.

```
python rename_files.py
```
The new filenames now look like below

```
US_eMAH_NDVI_2020_287-293_1KM_VI_NDVI_006_2020300170330.tif
US_eMAH_NDVI_2020_294-300_1KM_VI_NDVI_006_2020303221006.tif
US_eMAH_NDVI_2020_294-307_1KM_VI_NDVI_006_2020311150401.tif
US_eMAH_NDVI_2020_301-307_1KM_VI_NDVI_006_2020311141002.tif
```

2. Run `geeup getmeta` to extract metadata. 

> Note: geeup needs full paths to the folders

```
geeup getmeta \
    --input /Users/ujavalgandhi/Desktop/eModis/data/ \
    --metadata /Users/ujavalgandhi/Desktop/eModis/meta.csv
```

4. 
5. Upload the data using cookies.
```
geeup upload \
    --source /Users/ujavalgandhi/Desktop/eModis/data/ \
    --dest users/ujavalgandhi/temp/eModis \
    -m /Users/ujavalgandhi/Desktop/eModis/meta.csv \
    -u ujaval@spatialthoughts.com \
    --method cookies
```
