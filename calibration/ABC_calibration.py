import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
import os
import sys
ABC_path = '/Users/matin/Downloads/testProjs/ABayesianC'
sys.path.insert(1,ABC_path)
from ABayesianC import tools
import json
import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')
sys.path.insert(0,dir_to_dirs)
from dirs import dir_to_MSC_osteogenesis
sys.path.insert(0,dir_to_MSC_osteogenesis)
from MSC_osteogenesis import *



class Optimize(object):
	"""docstring for ClassName"""
	def __init__(self, calib_params):
		self.calib_params = calib_params
	def run(self):
		obj = MSC_model(free_params = self.calib_params)
		error = obj.run()
		return error

settings = {
	"MPI_flag": True,
	"sample_n": 100000,
	"top_n": 100,
    "replica_n": 1,
	"output_path": "ABC",
	"test": False,
	"model":Optimize
}


working_dir = os.getcwd()
output_dir = os.path.join(working_dir,settings["output_path"])
try:
	os.makedirs(output_dir)
except:
	pass
sys.path.insert(1,output_dir)


if __name__ == "__main__":
	obj = tools.ABC(settings=settings,free_params=free_params)
	obj.sample()
	obj.run()
	inferred_params = obj.postprocessing()
	with open('inferred_params.json','w') as file:
		file.write(json.dumps(inferred_params, indent = 4))
	# obj.run_tests()