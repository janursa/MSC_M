import os
import sys
import json
import numpy as np
import json
import pathlib

current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')

sys.path.insert(0,dir_to_dirs)


results_file = os.path.join(dir_to_dirs,'results','batch_calibration')

def file_func(n1,n2):
	files = []
	for i in range(n1,n2):
		file = 'inferred_params_%d.json'%i
		files.append(file)
	return files

files = file_func(n1 = 0, n2 = 100)
inferred_params_lists = [] # stores data based on study tag
for file in files:
	with open(os.path.join(results_file,file)) as ff:
		params = json.load(ff)
	inferred_params_lists.append(params)

inferred_params_accumulated = {}
for key in inferred_params_lists[0].keys():
	inferred_params_accumulated[key] = []
	for item in inferred_params_lists:
		inferred_params_accumulated[key].append(item[key])

inferred_params_mean = {}
for key,value in inferred_params_accumulated.items():
	inferred_params_mean[key]=np.mean(value)

with open('inferred_params_mean_1.json','w') as file:
	file.write(json.dumps(inferred_params_mean, indent = 4))
with open('inferred_params_accumulated.json','w') as file:
	file.write(json.dumps(inferred_params_accumulated, indent = 4))
