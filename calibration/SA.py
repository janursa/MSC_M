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
sys.path.insert(0,'/Users/matin/Downloads/testProjs/barneySA')
from barneySA import tools
import json
import copy

class settings:
    results_folder = os.path.join(dir_to_dirs,'results')
    files = {
    # 'Qiao_2021_Mg': 'Qiao_2021_Mg/inferred_params_0_200.json',
    # 'Ber_2016': 'Ber_2016/inferred_params_0_120.json',
    # 'Valles_2020': 'Valles_2020/inferred_params_0_200.json',
    # 'Chen_2018': 'Chen_2018/inferred_params_0_200.json',
    # 'Qiao_2021_ILs': 'Qiao_2021_ILs/inferred_params_0_400.json',
    # 'All': 'All/inferred_params_0_200.json',
    'All': 'inferred_params.json',
    }

SA_settings = { # define settings
    "MPI_flag": True,
    "replica_n": 1,
    "output_path": "",
    "model":MSC_model, # this runs the mode
    "args": {'fixed_params':parameters.fixed_params,'observations':None}
}
tricky_keys = { 'Qiao_2021_ILs':['ALP_M_n',  'IL1b_ineffective',  'IL8_favorable',  'a_early_diff_stim', 'diff_time', 'a_Qiao_2021_ALP'],
                
                'Valles_2020':[ 'diff_time', 'a_Valles_2020_ALP', 'a_Valles_2020_ARS'],
                
                'Chen_2018':['a_early_diff_stim', 'a_late_diff_stim', 'diff_time', ],

                'Ber_2016':[  'a_late_diff_inhib'],

                'Qiao_2021_Mg':[ 'ALP_M_n', 'ALP_0', 'Mg_stim', 'Mg_dest', 'maturity_t', 'early_diff_fast', 'a_early_diff_stim', 'diff_time', 'a_Valles_2020_ALP'],

                'All':[ 'a_Valles_2020_ALP', 'a_Valles_2020_ARS', 'a_Chen_2018_ALP',  'a_Qiao_2021_ALP', 'a_early_diff_inhib', 'a_late_diff_stim', 'a_late_diff_inhib',  'IL1b_ineffective', 'ALP_M_n',  'diff_time',]

}
                

def limit_bounds(study,bounds):
    for key in tricky_keys[study]:
        if key in bounds.keys():
            bounds[key] = [int(item) for item in bounds[key]]
            # bounds[key] = parameters.free_params_all[key]

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
def detailed_errors(set1,set2):
    study_detailed_errors = {}
    for study_name in set1.keys():
        if study_name not in set2:
            raise ValueError('set1 and set2 doent have same study names')

        assert(set1[study_name].keys() == set2[study_name].keys()) # both should have same IDs
        IDs = list(set1[study_name].keys())
        set1_results = set1[study_name]
        set2_results = set2[study_name]

        IDs_detailed_errors = {}
        for ID in IDs:
            set1_ID_results = set1_results[ID]
            set2_ID_results = set2_results[ID]
            target_detailed_errors = {}
            for target in set1_ID_results.keys():
                set1_target_results = set1_ID_results[target]
                set2_target_results = set2_ID_results[target]
                assert(len(set1_target_results) == len(set2_target_results))
                errors = []
                for i in range(len(set1_target_results)):
                    error = abs(set1_target_results[i]-set2_target_results[i])/2
                    errors.append(error)
                target_detailed_errors[target] = errors
            IDs_detailed_errors[ID] = target_detailed_errors
        study_detailed_errors[study_name] = IDs_detailed_errors
    return study_detailed_errors



if __name__ == '__main__':
    if False:
        PTTSs_studies = {}
        for study,file in settings.files.items():
            with open(os.path.join(settings.results_folder,file)) as file:
                inferred_params = json.load(file)
            # inferred_params = remove_params(inferred_params)
            #// Create bounds by 50% variation
            bounds = {}
            for key,value in inferred_params.items():
                bounds[key] = [round(value*.5,3),round(value*1.5,3)]
            # print(bounds)
            # bounds = limit_bounds(study,bounds)
            obs,_ = parameters.specifications(study)
            SA_settings['args']['observations'] = obs
            PTTSs= sensitivity_analysis(bounds,SA_settings)
            PTTSs_studies[study] = PTTSs

        with open(os.path.join(settings.results_folder,'PTTSs.json'),'w') as file:
            file.write(json.dumps(PTTSs_studies,indent=2))

    #// run the model for the variation of each parameter and obtain the contribution each paramter make for the accuracy of the results
    study_params_errors = {}
    study_detailed_errors = {} # errors for each measurement day and item for each scenario of perturbation
    for study,file in settings.files.items():
        print(study)
        with open(os.path.join(settings.results_folder,file)) as file:
            inferred_params = json.load(file)
        #// Create bounds by multiplying and dividing to 2
        bounds = {}
        for key,value in inferred_params.items():
            bounds[key] = [round(value*0.85,3),round(value*1.15,3)]
        bounds = limit_bounds(study,bounds)
        #// run the model for each bound
        obs,_ = parameters.specifications(study)
        original_error = single_run(free_params=inferred_params,fixed_params=parameters.fixed_params,observations=obs) # get the overall error for SA
        obj = MSC_model(free_params=inferred_params,fixed_params=parameters.fixed_params,observations=obs) # get the specific errors for each measurement points for standard deviation
        original_results = obj.simulate_studies()

        params_errors = {}
        study_detailed_errors [study] = [] # we insert results of each variation of paramter perturbation into the study list and then find the max values
        for key,bound in bounds.items():
            errors = []
            free_params =copy.deepcopy(inferred_params)
            for item in bound:
                free_params[key] = item
                error = single_run(free_params=free_params,fixed_params=parameters.fixed_params,observations=obs)
                errors.append(error)

                obj = MSC_model(free_params=free_params,fixed_params=parameters.fixed_params,observations=obs) # get the specific errors for each measurement points for standard deviation
                sub_results = obj.simulate_studies()
                sub_errors = detailed_errors(sub_results,original_results)
                study_detailed_errors[study].append(sub_errors)

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
    with open(os.path.join(settings.results_folder,'detailed_errors.json'),'w') as file:
        file.write(json.dumps(study_detailed_errors,indent=2))
            





