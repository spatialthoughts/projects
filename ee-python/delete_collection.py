""" A python script to delete Earth Engine Collections

GEE collections cannot be delete directly, so this script
provides a simple way to get all assets in a collection
and delete them


Sample usage:
python delete_collection.py --collection <collection> 

Add a --delete option to actually delete the assets
python delete_collection.py --collection <collection> --delete
"""
import argparse
import ee

parser = argparse.ArgumentParser(usage='python delete_collection.py <collection>')
parser.add_argument('--collection', help='collection to delete')
parser.add_argument('--delete', help='delete old collection', action=argparse.BooleanOptionalAction)

args = parser.parse_args()

# Replace the cloud_project with your own project
cloud_project = 'spatialthoughts'

try:
    ee.Initialize(project=cloud_project)
except:
    ee.Authenticate()
    ee.Initialize(project=cloud_project)

collection = args.collection

# Check if new collection exists
try:
    ee.ImageCollection(collection).getInfo()
except:
    print('Collection {} does not exist'.format(collection))
    

assets = ee.data.listAssets({'parent': collection})['assets']

if not args.delete:
    print('The command will just list asset. Add --delete to actually delete them.')


for asset in assets:
    asset_name = asset['name']
    print(f'Found child asset {asset_name}')
    if args.delete:
        print('Deleting <{}>'.format(asset_name))
        ee.data.deleteAsset(asset_name)

if args.delete:
    print('Deleting Collection <{}>'.format(collection))
    ee.data.deleteAsset(collection)