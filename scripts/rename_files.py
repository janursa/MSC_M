import os
import sys
import json
import numpy as np
import json
import pathlib

current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')

sys.path.insert(0,dir_to_dirs)


results_file = os.path.join(dir_to_dirs,'results','batch_calibration_2')

def file_func(n1,n2):
	files = []
	for i in range(n1,n2):
		file = 'inferred_params_%d.json'%i
		files.append(file)
	return files

files = file_func(n1 = 0, n2 = 100)
range_of_new_names = range(100,200)
dest_folder = os.path.join(dir_to_dirs,'results','batch_calibration_22')
for i in range(len(files)):
	file = files[i]
	new_name = 'inferred_params_%d.json'%range_of_new_names[i]
	with open(os.path.join(results_file,file)) as ff:
		params = json.load(ff)
	with open(os.path.join(dest_folder,new_name),'w') as ff:
		ff.write(json.dumps(params, indent = 4))
