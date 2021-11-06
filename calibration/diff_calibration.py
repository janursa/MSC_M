from scipy.optimize import differential_evolution
import numpy as np
import json
import sys
import pathlib
import os
current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')
sys.path.insert(0,dir_to_dirs)
from dirs import dir_to_MSC_osteogenesis
sys.path.insert(0,dir_to_MSC_osteogenesis)
from MSC_osteogenesis import MSC_model
from parameters import specifications, fixed_params	

##// optimize //##
class Calibrate:
	def __init__(self,fixed_params,free_params,observations):
		self.max_iters = 300
		self.free_params = free_params
		self.fixed_params = fixed_params
		self.obs = observations
	def cost_function(self,calib_params_values):
		# calculate the error for each target by comparing the results to the original model
		calib_params = {}
		for key,value in zip(self.free_params.keys(),calib_params_values):
			calib_params[key] = value
		obj = MSC_model(fixed_params = self.fixed_params,free_params=calib_params,observations = self.obs)
		error = obj.run()
		return error

	def optimize(self,n_proc,disp=True):
		# Call instance of PSO
		# results = differential_evolution(self.cost_function,bounds=list(self.free_params.values()),disp=True,maxiter=self.max_iters,workers=-1)
		results = differential_evolution(self.cost_function,bounds=list(self.free_params.values()),maxiter=self.max_iters,workers=n_proc,disp=disp)
		# results = differential_evolution(self.cost_function,bounds=list(self.free_params.values()),disp=True,maxiter=self.max_iters)
		inferred_params = {}
		for key,value in zip(self.free_params.keys(),results.x):
			inferred_params[key] = value
		with open('inferred_params.json','w') as file:
			file.write(json.dumps(inferred_params, indent = 4))
		return inferred_params,results.fun

def calibrate(fixed_params,free_params,observations, n_proc=1,disp=True):
	# print('fixed_params',fixed_params)
	# print('free_params',free_params)
	calib_obj = Calibrate(fixed_params,free_params,observations)
	inferred_params,error = calib_obj.optimize(n_proc,disp=disp)
	return inferred_params


if __name__ == '__main__':
	##/ calibrate
	n_proc = sys.argv[1]
	# study = 'Chen_2018'
	study = 'All'
	print('number of assigned processers:',n_proc)
	obs,free_params = specifications(study = study)
	calibrate(fixed_params = fixed_params,free_params=free_params,observations=obs,n_proc=n_proc)

