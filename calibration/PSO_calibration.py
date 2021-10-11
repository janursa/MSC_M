import pyswarms as ps
from pyswarms.utils.functions import single_obj as fx
import numpy as np
import json
# import matplotlib.pyplot as plt
from MSC_osteogenesis import *



# Set-up hyperparameters
class SETTINGS:
	options = {'c1': 0.5, 'c2': 2, 'w':2}
	dimensions = len(free_params.keys())
	bounds = ([item[0] for item in free_params.values()],[item[1] for item in free_params.values()])
	n_particles = 100
	iters = 100


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
		obj = MSC_model(free_params = calib_params_set)
		error = obj.run()
		costs.append(error)
	# print('finished')
	return costs

def optimize():
	# Call instance of PSO
	optimizer = ps.single.GlobalBestPSO(n_particles=SETTINGS.n_particles, 
		dimensions=SETTINGS.dimensions, options=SETTINGS.options, bounds=SETTINGS.bounds)
	# Perform optimization
	cost, pos = optimizer.optimize(cost_function,iters=SETTINGS.iters)

	return cost,pos
cost,pos = optimize()
# print(cost)
# print(pos)
inferred_params = {}
for key,value in zip(free_params.keys(),pos):
	inferred_params[key] = value
with open('inferred_params.json','w') as file:
	file.write(json.dumps(inferred_params, indent = 4))
