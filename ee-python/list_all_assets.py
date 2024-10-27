import argparse
import ee

parser = argparse.ArgumentParser()
parser.add_argument('--asset_folder', help='full path to the asset folder')
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

for asset in all_assets:
	print(asset)