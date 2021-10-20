import os
import sys
import json
import numpy as np
import json
import pathlib

current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')

sys.path.insert(0,dir_to_dirs)

class PARAMS:
	results_file = os.path.join(dir_to_dirs,'results','batch_calibration')
	errors_file = os.path.join(results_file,'error_list.json')
	dest_folder = os.path.join(dir_to_dirs,'results','batch_calibration_selected')
	error_cut_off_value = 0.01

try:
    os.makedirs(PARAMS.dest_folder)
except OSError:
    print("Creation of the directory %s failed" % PARAMS.dest_folder)


with open(PARAMS.errors_file) as ff:
	error_list = json.load(ff) 

def file_func(n1,n2):
	files = []
	for i in range(n1,n2):
		if error_list[str(i)]>PARAMS.error_cut_off_value:
			continue
		file = 'inferred_params_%d.json'%i
		files.append(file)
	return files

files = file_func(n1 = 0, n2 = 10)

for file in files:
	with open(os.path.join(PARAMS.results_file,file)) as ff:
		params = json.load(ff)
	with open(os.path.join(PARAMS.dest_folder,file),'w') as ff:
		ff.write(json.dumps(params))

sys.exit(2)