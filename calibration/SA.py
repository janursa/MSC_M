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