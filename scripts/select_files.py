import os
import sys
import json
import numpy as np
import json
import pathlib

current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')
sys.path.insert(0,dir_to_dirs)
from dirs import dir_to_MSC_osteogenesis
sys.path.insert(0,dir_to_MSC_osteogenesis)
from MSC_osteogenesis import single_run,fixed_params,MSC_model

class PARAMS:
	results_folder = os.path.join(dir_to_dirs,'results','Chen')
	results_file = os.path.join(results_folder,'batch_calibration')
	dest_folder = os.path.join(results_folder,'batch_calibration_selected')
	error_cut_off_value = 0.1
	n_start = 0
	n_end = 200

try:
    os.makedirs(PARAMS.dest_folder)
except OSError:
    print("Creation of the directory %s failed" % PARAMS.dest_folder)



## run the simulation for the obtain parameters and calculate error values
def file_func(n1,n2):
	files = []
	for i in range(n1,n2):
		file = 'inferred_params_%d.json'%i
		files.append(file)
	return files

files = file_func(n1 = PARAMS.n_start, n2 = PARAMS.n_end)
ii = 0 
errors = {}
for file in files:
	with open(os.path.join(PARAMS.results_file,file)) as ff:
		inferred_params = json.load(ff)
	# obj = MSC_model(fixed_params = fixed_params,free_params=inferred_params)
	# error = obj.run()
	error = single_run(fixed_params = fixed_params,free_params=inferred_params)
	if error > PARAMS.error_cut_off_value:
		continue
	print(ii,error)
	with open(os.path.join(PARAMS.dest_folder,'inferred_params_%d.json'%ii),'w') as ff:
		ff.write(json.dumps(inferred_params))
	errors[ii]=error
	ii+=1

with open(os.path.join(PARAMS.dest_folder,'errors.json'),'w') as ff:
	ff.write(json.dumps(errors))
