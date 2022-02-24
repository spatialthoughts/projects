import argparse
import ee
import sys
import csv

ee.Initialize()

parser = argparse.ArgumentParser(usage='python asset_size.py <path to asset folder> <output_file>')
parser.add_argument('--asset_folder', help='full path to the asset folder')
parser.add_argument('--output_file', help='output file to write')

args = parser.parse_args()

parent = args.asset_folder

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
            asset_list.extend(get_asset_list(child_id))
        else:
            asset_list.append(child_id)
    return asset_list
    
all_assets = get_asset_list(parent)

print('Found {} assets'.format(len(all_assets)))

data = []

for asset in all_assets:
    size = ee.data.getAsset(asset)['sizeBytes']
    size_mb = round(int(size)/1e6, 2)
    data.append({'asset': asset, 'size_mb': size_mb})
    

fieldnames = ['asset', 'size_mb']
with open(args.output_file, mode='w') as output_file:
    csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    for row in data:
        csv_writer.writerow(row)
        
print('Successfully written output file at {}'.format(args.output_file))
