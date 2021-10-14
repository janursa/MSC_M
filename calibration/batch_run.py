from SA import sensitivity_analysis
# from ABC_calibration import calibrate
from diff_calibration import Calibrate

import pathlib
import os
import sys
import numpy as np
import json

current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')
sys.path.insert(0,dir_to_dirs)
from dirs import dir_to_MSC_osteogenesis
sys.path.insert(0,dir_to_MSC_osteogenesis)
from MSC_osteogenesis import free_params

class Batch_calibrate:
	def __init__(self,replica_n):
		from mpi4py import MPI
		self.replica_n = replica_n
		self.comm = MPI.COMM_WORLD
		self.rank = self.comm.Get_rank()
		print("Number of CPUs assigned: ",self.comm.Get_size())
		self.dir_name = 'batch_calibration'
		if self.rank == 0:
			try:
				os.makedirs(self.dir_name)
			except OSError:
				print("Creation of the directory %s failed" % self.dir_name)
			else:
				print("Successfully created the directory %s " % self.dir_name)

	def run(self):
		"""Runs the user given model for the parameter sets.
		"""
		if self.rank == 0:
			import numpy as np
			CPU_n = self.comm.Get_size()
			run_n = self.replica_n[1]-self.replica_n[0]
			shares = np.ones(CPU_n,dtype=int)*int(run_n/CPU_n)
			print(shares)
			plus = run_n%CPU_n
			for i in range(plus):
				shares[i]+=1

			portions = []
			for i in range(CPU_n):
				start = sum(shares[0:i])
				end = start + shares[i]
				portions.append([start,end])

		else:
			portions = None

		portion = self.comm.scatter(portions,root = 0)

		def run_model(start,end):
			inferred_params_list = []
			for i in range(start,end):
				calib_obj = Calibrate(free_params)
				inferred_params = calib_obj.optimize(n_proc=1,disp=False)
				with open(os.path.join(self.dir_name,'inferred_params_{}.json'.format(i)),'w') as file:
					file.write(json.dumps(inferred_params, indent = 4))
				inferred_params_list.append(inferred_params)
				print('Iteration %d completed'%i)
			return inferred_params_list
		inferred_params_list_perCore = run_model(portion[0],portion[1])

		inferred_params_list_stacks = self.comm.gather(inferred_params_list_perCore,root = 0)
		if self.rank == 0:
			import numpy as np
			inferred_params_list = np.array([])
			for stack in inferred_params_list_stacks:
				inferred_params_list = np.concatenate([inferred_params_list,stack],axis = 0)

			inferred_params_accumulated = {}

			for key in inferred_params_list[0].keys():
				inferred_params_accumulated[key] = []
				for i in range(self.replica_n):
					inferred_params_accumulated[key].append(inferred_params_list[i][key])

			inferred_params_mean = {}
			for key,value in inferred_params_accumulated.items():
				inferred_params_mean[key]=np.mean(value)

			with open(os.path.join(self.dir_name,'inferred_params_mean.json'),'w') as file:
					file.write(json.dumps(inferred_params_mean, indent = 4))
			with open(os.path.join(self.dir_name,'inferred_params_accumulated.json'),'w') as file:
					file.write(json.dumps(inferred_params_accumulated, indent = 4))

if __name__ == '__main__':
	replica_n = [0,50]
	obj = Batch_calibrate(replica_n)
	obj.run()
