import sys
import pathlib
import os
current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')
sys.path.insert(0,dir_to_dirs)
from dirs import dir_to_MSC_osteogenesis
sys.path.insert(0,dir_to_MSC_osteogenesis)
import parameters 
from MSC_osteogenesis import MSC_model,single_run
from barneySA import tools
import json
import copy

class settings:
    results_folder = os.path.join(dir_to_dirs,'results')
    files = {
    'Qiao_Mg':'Qiao_Mg.json',
    'Qiao_IL8_IL1b':'Qiao_IL8_IL1b/inferred_params_0_400.json',
    'Chen_2018':'Chen/inferred_params_0_200.json',
    'Valles_2020':'Valles/inferred_params_0_200.json',
    'Ber_2016':'Ber.json',
    'All':'all.json',
    }

SA_settings = { # define settings
    "MPI_flag": True,
    "replica_n": 1,
    "output_path": "",
    "model":MSC_model, # this runs the mode
    "args": {'fixed_params':parameters.fixed_params,'observations':None}
}
tricky_keys = { 'Qiao_IL8_IL1b':['ALP_M_n',  'IL1b_ineffective',  'IL8_favorable',  'a_early_diff_stim', 'diff_time', 'a_Qiao_2021_ALP'],
                
                'Valles_2020':[ 'diff_time', 'a_Valles_2020_ALP', 'a_Valles_2020_ARS'],
                
                'Chen_2018':['a_early_diff_stim', 'a_late_diff_stim', 'diff_time', ],

                'Ber_2016':[  'a_late_diff_inhib'],

                'Qiao_Mg':[   'Mg_stim', 'a_Valles_2020_ALP'],

                'All':[ 'a_Valles_2020_ALP', 'a_Valles_2020_ARS', 'a_Chen_2018_ALP',  'a_Qiao_2021_ALP', 'a_early_diff_inhib', 'a_late_diff_stim', 'a_late_diff_inhib',  'IL1b_ineffective', 'ALP_M_n',  'diff_time',]

}
                

def limit_bounds(study,bounds):
    for key in tricky_keys[study]:
        if key in bounds.keys():
            # bounds[key] = [int(item) for item in bounds[key]]
            bounds[key] = parameters.free_params_all[key]

    for key,value in bounds.items():
        lower_limit,upper_limit = parameters.free_params_all[key]
        if bounds[key][0] < lower_limit:
            bounds[key][0] = lower_limit
        if bounds[key][1] > upper_limit:
            bounds[key][1] = upper_limit
    return bounds

def sensitivity_analysis(bounds,SA_settings):
    obj = tools.SA(free_params = bounds,settings = SA_settings)
    obj.sample()
    obj.run()
    PTTSs = obj.postprocessing()
    return PTTSs
def remove_params(params):
    # if 'ARS_0' in params:
    #     del params['ARS_0']
    # if 'ALP_0' in params:
    #     del params['ALP_0']
    # if 'OC_0' in params:
    #     del params['OC_0']
    # if 'OC_M_n' in params:
    #     del params['OC_M_n']
    # if 'ALP_M_n' in params:
    #     del params['ALP_M_n']
    # if 'ARS_M_n' in params:
    #     del params['ARS_M_n']
    return params

if __name__ == '__main__':
    if False:
        PTTSs_studies = {}
        for study,file in settings.files.items():
            print(study)
            with open(os.path.join(settings.results_folder,file)) as file:
                inferred_params = json.load(file)
            # inferred_params = remove_params(inferred_params)
            #// Create bounds by 50% variation
            bounds = {}
            for key,value in inferred_params.items():
                bounds[key] = [round(value*.5,3),round(value*1.5,3)]

            bounds = limit_bounds(study,bounds)
            obs,_ = parameters.specifications(study)
            SA_settings['args']['observations'] = obs
            PTTSs= sensitivity_analysis(bounds,SA_settings)
            PTTSs_studies[study] = PTTSs

        with open(os.path.join(settings.results_folder,'PTTSs.json'),'w') as file:
            file.write(json.dumps(PTTSs_studies,indent=2))

    #// run the model for the variation of each parameter and obtain the contribution each paramter make for the accuracy of the results
    study_params_errors = {}
    for study,file in settings.files.items():
        print(study)
        with open(os.path.join(settings.results_folder,file)) as file:
            inferred_params = json.load(file)
        #// Create bounds by multiplying and dividing to 2
        bounds = {}
        for key,value in inferred_params.items():
            bounds[key] = [round(value*0.5,3),round(value*1.5,3)]
        bounds = limit_bounds(study,bounds)
        #// run the model for each bound
        obs,_ = parameters.specifications(study)
        original_error = single_run(free_params=inferred_params,fixed_params=parameters.fixed_params,observations=obs)
        params_errors = {}
        for key,bound in bounds.items():
            errors = []
            free_params =copy.deepcopy(inferred_params)
            for item in bound:
                free_params[key] = item
                error = single_run(free_params=free_params,fixed_params=parameters.fixed_params,observations=obs)
                errors.append(error)
            params_errors[key] = errors
        # print('\n',params_errors)    
        params_errors_nomalized={}
        for key in inferred_params.keys():
            errors = params_errors[key]
            diff = [abs(error-original_error) for error in errors]
            diff_max = max(diff)
            # nn = round(diff_max/original_error,3)
            params_errors_nomalized[key] = int(diff_max*100)

        study_params_errors[study] = params_errors_nomalized
    with open(os.path.join(settings.results_folder,'contributed_errors.json'),'w') as file:
        file.write(json.dumps(study_params_errors,indent=2))
            





