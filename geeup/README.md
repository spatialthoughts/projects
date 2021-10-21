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

3. Extract image date from the filename and update the `meta.csv` file.

```
python update_metadata.py
```

4. Generate cookies using `geeup cookie_setup`. On Mac, need to switch to Bash and disble canonical mode.

> Note: Make sure you grab cookies from the main Code Editor application at https://code.earthengine.google.com. Cookies from subdomains such as https://code.earthengine.google.co.in/ will not work.

```
/bin/sh
stty -icanon
geeup cookie_setup
<paste cookies using the Chrome Extension>
stty icanon
/bin/zsh
```

5. It's a good idea to create a collection for the data first. You can use the `earthengine` command-line tool.

```
earthengine create collection users/ujavalgandhi/eModis
```

7. Upload the data to the new collection using cookies.
```
geeup upload \
    --source /Users/ujavalgandhi/Desktop/eModis/data/ \
    --dest users/ujavalgandhi/eModis \
    -m /Users/ujavalgandhi/Desktop/eModis/meta.csv \
    -u ujaval@spatialthoughts.com \
    --method cookies
```
