import numpy as np

import os
import sys
import json
import json
import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')


class PARAMS:
	# study = 'Qiao_2021_Mg'
	# study = 'Ber_2016'
	# study = 'All'
	# study = 'Valles_2020'
	study = 'Chen_2018'
	results_folder = os.path.join(dir_to_dirs,'raw_results',study)
	results_file = os.path.join(results_folder,'batch_calibration_selected')
	n_start = 0
	n_end = 100
	inferred_params_mean_file = os.path.join(results_folder,'inferred_params_%d_%d.json'%(n_start,n_end))
	inferred_params_accumulated_file = os.path.join(results_folder,'inferred_params_accumulated.json')

print('Merging files {} to {} from folder {}'.format(PARAMS.n_start,PARAMS.n_end,PARAMS.results_file))

def file_func(n1,n2):
	files = []
	for i in range(n1,n2):
		file = 'inferred_params_%d.json'%i
		files.append(file)
	return files

files = file_func(n1 = PARAMS.n_start, n2 = PARAMS.n_end)
inferred_params_lists = [] # stores data based on study tag
for file in files:
	with open(os.path.join(PARAMS.results_file,file)) as ff:
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

with open(PARAMS.inferred_params_mean_file,'w') as file:
	file.write(json.dumps(inferred_params_mean, indent = 4))
with open(PARAMS.inferred_params_accumulated_file,'w') as file:
	file.write(json.dumps(inferred_params_accumulated, indent = 4))
