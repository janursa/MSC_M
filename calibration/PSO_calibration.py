import os
import pyswarms as ps
from pyswarms.utils.functions import single_obj as fx
import numpy as np
import json
import sys
# import matplotlib.pyplot as plt
import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')
sys.path.insert(0,dir_to_dirs)
from dirs import dir_to_MSC_osteogenesis
sys.path.insert(0,dir_to_MSC_osteogenesis)
from MSC_osteogenesis import *



# Set-up hyperparameters
class SETTINGS:
	options = {'c1': 0.6571, 'c2': 1.6, 'w':0.6}
	dimensions = len(free_params.keys())
	bounds = ([item[0] for item in free_params.values()],[item[1] for item in free_params.values()])
	n_particles = 100
	iters = 1000


def cost_function(calib_params):
	# print(len(calib_params))
	costs = [] # cost values for each particle
	for j in range(SETTINGS.n_particles):
		# run the model
		# calculate the error for each target by comparing the results to the original model
		calib_params_values = calib_params[j]
		calib_params_set = {}
		for key,value in zip(free_params.keys(),calib_params_values):
			calib_params_set[key] = value
		obj = MSC_model(fixed_params = fixed_params,free_params = calib_params_set)
		error = obj.run()
		costs.append(error)
	# print('finished')
	return costs

def optimize(n_proc):
	# Call instance of PSO
	optimizer = ps.single.GlobalBestPSO(n_particles=SETTINGS.n_particles, 
		dimensions=SETTINGS.dimensions, options=SETTINGS.options, bounds=SETTINGS.bounds)
	# Perform optimization
	cost, pos = optimizer.optimize(cost_function,iters=SETTINGS.iters,n_processes=n_proc)

	return cost,pos

if __name__ == '__main__':
	##/ calibrate
	n_proc = int(sys.argv[1])
	cost,pos = optimize(n_proc)

	inferred_params = {}
	for key,value in zip(free_params.keys(),pos):
		inferred_params[key] = value
	with open('inferred_params.json','w') as file:
		file.write(json.dumps(inferred_params, indent = 4))
