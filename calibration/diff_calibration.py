from scipy.optimize import differential_evolution
import numpy as np
import json
import sys
from MSC_osteogenesis import *

##// optimize //##
class Calibrate:
	def __init__(self,free_params):
		self.max_iters = 500
		self.free_params = free_params
	def cost_function(self,calib_params_values):
		# calculate the error for each target by comparing the results to the original model
		calib_params = {}
		for key,value in zip(self.free_params.keys(),calib_params_values):
			calib_params[key] = value
		obj = MSC_model(free_params = calib_params)
		error = obj.run()
		return error

	def optimize(self,n_proc):
		# Call instance of PSO
		# results = differential_evolution(self.cost_function,bounds=list(self.free_params.values()),disp=True,maxiter=self.max_iters,workers=-1)
		results = differential_evolution(self.cost_function,bounds=list(self.free_params.values()),disp=True,maxiter=self.max_iters,workers=n_proc)
		# results = differential_evolution(self.cost_function,bounds=list(self.free_params.values()),disp=True,maxiter=self.max_iters)

		inferred_params = {}
		for key,value in zip(free_params.keys(),results.x):
			inferred_params[key] = value
		with open('inferred_params.json','w') as file:
			file.write(json.dumps(inferred_params, indent = 4))




if __name__ == '__main__':
	##/ calibrate
	n_proc = sys.argv[1]
	print('number of assigned processers:',n_proc)
	calib_obj = Calibrate(free_params)
	calib_obj.optimize(n_proc)
