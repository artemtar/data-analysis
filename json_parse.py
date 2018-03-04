import json
import os
import pandas as pd
from math import pi

def angle(x):
    return 180 / (pi * x)

directory_path = os.getcwd()
path = os.path.join(directory_path, 'wading-pools.json')


with open(path, 'r') as f:
    json_data = json.load(f)


pools_list = json_data['features']

print('raw data:  ', pools_list)

pools_list_refined = []

for p in pools_list:
    pool = p['properties']
    pool_location = p['geometry']
    pool_coord = pool_location['coordinates']
    pool_coord = [angle(pool_coord[0]), angle(pool_coord[1])] # remove if needed values in degree
    pools_list_refined.append({'name': pool['NAME'],
                               'coordinates': pool_coord})

print('unsorted: ' , pools_list_refined)

#sorting by coordinates, second is longitude, the most western is smallest(I think)
pools_list_refined.sort(key=lambda pool: pool['coordinates'][1], reverse=False)


print('sorted: ', pools_list_refined)

#look up data table can do exel staf on it
data_frame = pd.DataFrame(pools_list_refined)

csv_out = os.path.join(directory_path, 'csv.xls')
data_frame.to_csv(csv_out, encoding='utf-8', index=False)

#output
path_out = os.path.join(directory_path, 'output.pl')
with open(path_out, 'w') as f:
    for e in pools_list_refined:
        to_append = 'pool({0}, coordinates({1}, {2})).\n'.format(e['name'].split(' - ')[1], e['coordinates'][0], e['coordinates'][1])
        f.write(to_append)

