# import required modules. 
import os
import pandas as pd
import re

filename = 'meta.csv'
df = pd.read_csv(filename)

def get_date_from_name(row):
    name = row['id_no']
    # Extract the year and doy from name 
    # Date is a substring in YYYY_jjj format
    matches = re.search(r'(\d{4})_(\d{3})', name)
    year = int(matches.group(1))
    doy = int(matches.group(2))
    date = pd.to_datetime(year * 1000 + doy, format='%Y%j')
    # GEE expects dates in timestamp format
    return date.timestamp()

df['system:time_start'] = df.apply(get_date_from_name, axis=1)
df.to_csv(filename, index=False)