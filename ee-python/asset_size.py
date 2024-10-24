"""This script queries your Asset folder and generates a CSV file
with the size and type of each asset.

Usage:

python asset_size.py --asset_folder <path to any asset folder> --output_file output.csv

Example
python asset_size.py \
    --asset_folder projects/earthengine-legacy/assets/users/ujavalgandhi/temp \
    --output_file output.csv
"""
import argparse
import ee
import csv

parser = argparse.ArgumentParser(usage='python asset_size.py <path to asset folder> <output_file>')
parser.add_argument('--asset_folder', help='full path to the asset folder')
parser.add_argument('--output_file', help='output file to write')

args = parser.parse_args()
parent = args.asset_folder

# Replace the cloud_project with your own project
cloud_project = 'spatialthoughts'

try:
    ee.Initialize(project=cloud_project)
except:
    ee.Authenticate()
    ee.Initialize(project=cloud_project)

def get_asset_list(parent):
    parent_asset = ee.data.getAsset(parent)
    parent_id = parent_asset['name']
    parent_type = parent_asset['type']
    asset_list = []
    child_assets = ee.data.listAssets({'parent': parent_id})['assets']
    for child_asset in child_assets:
        child_id = child_asset['name']
        child_type = child_asset['type']
        if child_type in ['FOLDER','IMAGE_COLLECTION']:
            # Recursively call the function to get child assets
            asset_list.extend(get_asset_list(child_id))
        else:
            asset_list.append(child_id)
    return asset_list
    
all_assets = get_asset_list(parent)

print('Found {} assets'.format(len(all_assets)))

data = []

for asset in all_assets:
    print('Processing {}'.format(asset))
    info = ee.data.getAsset(asset)
    asset_type = info['type']
    size = info['sizeBytes']
    size_mb = round(int(size)/1e6, 2)
    data.append({
        'asset': asset, 
        'type': asset_type,
        'size_mb': size_mb
    })
    

# Sort the assets by size
sorted_data = sorted(data, key=lambda d: d['size_mb'], reverse=True)

# Write the data to a file
fieldnames = ['asset', 'type', 'size_mb']
with open(args.output_file, mode='w') as output_file:
    csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    for row in sorted_data:
        csv_writer.writerow(row)
        
print('Successfully written output file at {}'.format(args.output_file))
