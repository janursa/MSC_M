from SA import sensitivity_analysis
from ABC_calibration import calibrate

import pathlib
import os 
import sys

current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')
sys.path.insert(0,dir_to_dirs)
from dirs import dir_to_MSC_osteogenesis
sys.path.insert(0,dir_to_MSC_osteogenesis)
from MSC_osteogenesis import free_params

class PARAMS:
	cycle_n = 3
	top_n = 5


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
	PTTS = sensitivity_analysis(free_params) 
	selected_free_params = select(PTTS,PARAMS.top_n,free_params)
	inferred_params = calibrate(selected_free_params)
	print(inferred_params)
	# with open('inferred_params_{}.json'.format(n),'w') as file:
	# 	file.write(json.dumps(inferred_params, indent = 4))


