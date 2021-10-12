import sys
import pathlib
import os
current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')
sys.path.insert(0,dir_to_dirs)
from dirs import dir_to_MSC_osteogenesis
sys.path.insert(0,dir_to_MSC_osteogenesis)
from MSC_osteogenesis import *
from barneySA import tools
settings = { # define settings
    "MPI_flag": True,
    "replica_n": 1,
    "output_path": "",
    "model":MSC_model # this is your model
}
obj = tools.SA(free_params = free_params,settings = settings)

obj.sample()

obj.run()

obj.postprocessing()
