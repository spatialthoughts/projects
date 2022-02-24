""" A python script to rename Earth Engine Collections

GEE collections cannot be renamed directly, so this script
provides a simple way to get all assets in a collection
and copies it to the new collection

Sample usage:
python rename_collection.py --old_collection <old_collection> --new_collection <new_collection>

Add a --delete option to delete old_collection
python rename_collection.py --old_collection <old_collection> --new_collection <new_collection> --delete
"""
import argparse
import ee

parser = argparse.ArgumentParser(usage='python rename_collection.py --old_collection <old collection> --new_collection <new collection>')
parser.add_argument('--old_collection', help='old collection')
parser.add_argument('--new_collection', help='new collection')
parser.add_argument('--delete', help='delete old collection', action=argparse.BooleanOptionalAction)

args = parser.parse_args()

old_collection = args.old_collection
new_collection = args.new_collection

ee.Initialize()

# Check if new collection exists
try:
    ee.ImageCollection(new_collection).getInfo()
except:
    print('Collection {} does not exist'.format(new_collection))
    ee.data.createAsset({'type': ee.data.ASSET_TYPE_IMAGE_COLL}, new_collection)
    print('Created a new empty collection {}.'.format(new_collection))
    

assets = ee.data.listAssets({'parent': old_collection})['assets']


for asset in assets:
    old_name = asset['name']
    new_name = old_name.replace(old_collection, new_collection)
    print('Copying {} to {}'.format(old_name, new_name))
    ee.data.copyAsset(old_name, new_name, True)
    if args.delete:
        print('Deleting <{}>'.format(old_name))
        ee.data.deleteAsset(old_name)

if args.delete:
    print('Deleting Collection <{}>'.format(old_collection))
    ee.data.deleteAsset(old_collection)