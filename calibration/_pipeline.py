from SA import sensitivity_analysis,SA_settings
# from ABC_calibration import calibrate
from diff_calibration import calibrate

import pathlib
import os 
import sys
import copy
import json

current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')
sys.path.insert(0,dir_to_dirs)
from dirs import dir_to_MSC_osteogenesis
sys.path.insert(0,dir_to_MSC_osteogenesis)
from MSC_osteogenesis import free_params,fixed_params

class PARAMS:
	top_n = 7
	threshold = 0.01

def select(PTTS,n,free_params):
	values = list(PTTS.values())
	keys = list(PTTS.keys())
	top_values_indices = sorted(range(len(values)), key=lambda i: values[i])[-n:]
	selected_free_params_keys = []
	for i in top_values_indices:
		selected_free_params_keys.append(keys[i])

	selected_free_params = {}
	for key in selected_free_params_keys:
		selected_free_params.update({key:free_params[key]})
	return selected_free_params

if __name__ == '__main__':
	n = 0
	original_fixed_params = copy.deepcopy(fixed_params)
	original_free_params = copy.deepcopy(free_params)
	errors = []
	flag = True
	ii = 0
	inferred_params_combined = {}
	while flag:
		if free_params == {}:
			flag = False
		if len(free_params.keys())<5:
			selected_free_params = free_params
		else:
			SA_settings['args'] = {'fixed_params': fixed_params}
			PTTS = sensitivity_analysis(free_params,SA_settings) 
			selected_free_params = select(PTTS,PARAMS.top_n,free_params)
		inferred_params,error = calibrate(fixed_params=fixed_params,free_params = selected_free_params,n_proc=2)
		inferred_params_combined = {**inferred_params_combined,**inferred_params}
		with open('inferred_params_%d.json'%ii,'w') as file:
			file.write(json.dumps(inferred_params, indent = 4))
		# print('inferred_params',inferred_params)
		for key,value in inferred_params.items():
			fixed_params[key] = value
			del free_params[key]

		errors.append(error)
		if ii > 2:
			if (errors[-1]-errors[-2]) < PARAMS.threshold:
				flag = False
		ii+=1
	with open('inferred_params.json','w') as file:
		file.write(json.dumps(inferred_params_combined, indent = 4))



