import sys
import pathlib
import os
import importlib

current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')
sys.path.insert(0,dir_to_dirs)
from dirs import dir_to_MSC_osteogenesis
sys.path.insert(0,dir_to_MSC_osteogenesis)
import MSC_osteogenesis 
import json
import plots
import parameters
import numpy as np 
importlib.reload(plots)
importlib.reload(parameters)
importlib.reload(MSC_osteogenesis)

def rearrange_errors(errors,targets):
#     print(errors)
#     print(targets)
    target_errors = {}
    for target in targets:
        target_error_list = []
        for ID,ID_error in errors.items():
            target_error_list.append(ID_error[target])
        target_errors[target] = np.mean(target_error_list)
    return target_errors
    
##/ run test simultions and plot
results_folder = os.path.join(dir_to_dirs,'results')
with open(os.path.join(results_folder,'Valles.json')) as file:
    inferred_params = json.load(file)
# inferred_params['a_late_diff_inhib'] = 10
all_studies_flag = False
obs,_ = parameters.specifications('Valles_2020')

obj = MSC_osteogenesis.MSC_model(fixed_params=parameters.fixed_params,free_params = inferred_params,observations=obs, debug=False)
simulation_results = obj.simulate_studies()
study_errors = obj.cost_studies(simulation_results)

error = obj.run()
# print(studies_errors)

print('Overall error is ',error)

for study in obs['studies']:
    targets = list(obs[study]['measurement_scheme'].keys())
    study_error = rearrange_errors(study_errors[study],targets)
    if study == 'Qiao_2021_Mg' or study == 'Ber_2016':
        plot_obj = plots.Plot_bar_2(study=study,observations=obs,errors=study_error)
    else:
        plot_obj = plots.Plot_bar(study,obs,errors=study_error)
    plot_obj.plot(simulation_results[study])