import os
data_dir = 'data'
files = os.listdir(data_dir)
for old_name in files:
    filename, extension = os.path.splitext(old_name)
    new_name = filename.replace('.', '_') + extension
    old_path = os.path.join(data_dir, old_name)
    new_path = os.path.join(data_dir, new_name)
    os.rename(old_path, new_path)
    print('Renamed: {} to {}'.format(old_path, new_path))