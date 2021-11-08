
import numpy as np
import json
import sys
import pathlib
import os
# from pympler import muppy,tracker
current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')
sys.path.insert(0,dir_to_dirs)
from dirs import dir_to_MSC_osteogenesis
sys.path.insert(0,dir_to_MSC_osteogenesis)
from MSC_osteogenesis import MSC_model, single_run
import parameters 
import sys
import psutil
import gc

process = psutil.Process(os.getpid())


# core_objects = ['core_objects','i', 'json', 'np', 'os', 'parameters', 'pathlib', 'single_run', 'sys']

def func_run(n):
    for i in range(n):
        # from MSC_osteogenesis import MSC_model
        obs,free_params = parameters.specifications('All')
        # error = single_run(free_params={}, fixed_params=parameters.fixed_params,observations=obs)
        obj = MSC_model(fixed_params = parameters.fixed_params,free_params={},observations=obs)
        error = obj.run()
        
        # print(i)
        if i%500==0:
            # del MSC_model
            print('Curr Memory usage: %s (KB)' % (process.memory_info().rss / 1024))
            # gc.collect()



            # print('Iteration ',i)
if __name__ == '__main__':
    func_run(1000)
    # func_run(1000)
if __name__ == '__main__':
    func_run(1000)
    # func_run(1000)