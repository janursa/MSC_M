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
SA_settings = { # define settings
    "MPI_flag": True,
    "replica_n": 1,
    "output_path": "",
    "model":MSC_model, # this runs the mode
    "args": {'fixed_params':fixed_params}
}

def sensitivity_analysis(free_params,SA_settings):
    obj = tools.SA(free_params = free_params,settings = SA_settings)
    obj.sample()
    obj.run()
    PTTS = obj.postprocessing()
    return PTTS

    
if __name__ == '__main__':
    sensitivity_analysis(free_params,SA_settings)
