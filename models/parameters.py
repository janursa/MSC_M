import sys
import pathlib
import os
current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')
sys.path.insert(0,dir_to_dirs)
from dirs import dir_to_MSC_osteogenesis
sys.path.insert(0,dir_to_MSC_osteogenesis)
from observations import observations
fixed_params = {
    'diff_time':30*24, # days required for full differentiation   
    'maturity_t':.5, # early maturity threshold 

    'early_diff_slow':.25, # center of low membership function
    'early_diff_fast':.65, # center of high membership function
    'early_diff_very_fast':.85, # center of high membership function
    'late_diff_slow':.25, # center of low membership function
    'late_diff_fast':.75, # center of high membership function

    'Mg_stim':5, # stimulatory conc of Mg
    'Mg_dest':30, # detrimental conc of Mg
    'IL1b_ineffective':120, # detrimental threshold IL1b
    'IL1b_stim':10,
    'IL8_favorable':25, # medium threshold for IL8
    
    'a_early_diff_stim':1, # scale factor, stimulatory
    'a_early_diff_inhib':2, # scale factor, inhibitory
    'a_late_diff_stim':2, # scale factor
    'a_late_diff_inhib':2, # scale factor

    'ALP_M_n':5, # n in the equation ALP = a*(M^n + ALP_0)
    'ARS_M_n':5, # n in the equation ARS = a*(M^n + ARS_0)
    'OC_M_n':5, # n in the equation ARS = a*(M^n + ARS_0)
    'ALP_0':5, # the default value of ALP when maturity is zero
    'ARS_0':5, # the default value of ARS when maturity is zero 
    'OC_0':5, # the default value of ARS when maturity is zero 


    'a_Chen_2018_maturity_t':1,
    'a_Chen_2018_ALP':2,
    'a_Chen_2018_ARS':2,

    'a_Valles_2020_maturity_t':1,
    'a_Valles_2020_ALP':2,
    'a_Valles_2020_ARS':2,

    'a_Qiao_2021_maturity_t':1,
    'a_Qiao_2021_ALP':2,

    'a_Ber_2016_maturity_t':1, # correction coeff of maturity threshold for the given study considering that cells are inherintly different
    'a_Ber_2016_ALP':.5, # correlation ALP to maturity
    'a_Ber_2016_OC':.5,
}
free_params_all = {
    'a_Ber_2016_ALP': [0,1],
    'a_Ber_2016_OC':[0,1],

    'a_Valles_2020_ALP':[0,1000],
    'a_Valles_2020_ARS':[0,1000],

    'a_Chen_2018_ALP':[0,10],
    'a_Chen_2018_ARS':[0,10],

    'a_Qiao_2021_ALP':[0,200],

    'a_early_diff_stim':[0,20], # scale factor, upregulatory --
    'a_early_diff_inhib':[0,20], # scale factor, downregulatory --
    'a_late_diff_stim':[0,20], # scale factor --
    'a_late_diff_inhib':[0,20], # scale factor --


    'early_diff_slow':[0.1,0.4], # center of low membership function --
    'early_diff_fast':[0.5,0.75], # center of high membership function --
    'early_diff_very_fast':[0.6,1], # center of high membership function --
    'late_diff_slow':[0.1,0.4], # center of low membership function --
    'late_diff_fast':[0.6,0.9], # center of high membership function --

    'Mg_stim':[2,10], # stimulatory conc of Mg --
    'Mg_dest':[20,40], # detrimental conc of Mg --
    'IL1b_ineffective':[30,199], # high threshold IL1b --
    'IL1b_stim':[1,29], # stimulatory threshold of IL1b --
    'IL8_favorable':[1,99], # medium threshold for IL8 --

    'ALP_M_n':[0,10], # n in the equation ALP = a*(M^n + ALP_0)
    'ARS_M_n':[0,10], # n in the equation ARS = a*(M^n + ARS_0)
    'OC_M_n':[0,10], # n in the equation ARS = a*(M^n + ARS_0)
    'ALP_0':[0,10], # the default value of ALP when maturity is zero
    'ARS_0':[0,10], # the default value of ARS when maturity is zero 
    'OC_0':[0,10], # the default value of ARS when maturity is zero 

    'diff_time':[15*24,45*24], # days required for full differentiation ---
    'maturity_t':[0.2,.8] # early maturity threshold.  ---

}
free_params_Qiao_Mg = [
'ALP_M_n',
'ALP_0',
'Mg_stim', 
'Mg_dest',
'maturity_t',
'early_diff_fast',
'a_early_diff_stim',
'diff_time', 
'a_Valles_2020_ALP'
]

free_params_Qiao_IL8_IL1b = [
    'ALP_M_n',
    'ALP_0',
    'IL1b_ineffective',
    'IL1b_stim',
    'IL8_favorable',
    'maturity_t',
    'early_diff_very_fast',
    'a_early_diff_stim',
    'diff_time',
    'a_Qiao_2021_ALP'
]
free_params_Chen = [
    'a_Chen_2018_ALP',
    'a_Chen_2018_ARS',

    'a_early_diff_stim',
    'a_early_diff_inhib',
    'a_late_diff_stim',
    'a_late_diff_inhib',
    
    'early_diff_slow',
    'early_diff_fast',
    'early_diff_very_fast',
    'late_diff_slow',
    'late_diff_fast',

    'ALP_M_n',
    'ARS_M_n',
    'ALP_0',
    'ARS_0',

    'diff_time',
    'maturity_t'
]
free_params_Valles = [
    'ALP_M_n',
    'ARS_M_n',
    'ALP_0',
    'ARS_0',

    'maturity_t', 
    'early_diff_slow', 
    'early_diff_fast', 
    'early_diff_very_fast',
    'late_diff_slow',
    'late_diff_fast',
    'a_early_diff_stim',
    'a_early_diff_inhib',
    'a_late_diff_stim',
    'a_late_diff_inhib',
    'diff_time',

    'a_Valles_2020_ALP',
    'a_Valles_2020_ARS'

]
free_params_Ber = [

    'a_Ber_2016_ALP',
    'a_Ber_2016_OC',

    'a_early_diff_stim',
    'a_late_diff_inhib',


    'early_diff_very_fast',
    'late_diff_slow',

    'Mg_stim',
    'Mg_dest',
 
    'ALP_M_n',
    'OC_M_n',
    'ALP_0',
    'OC_0',

    'diff_time',
    'maturity_t'

]
# candidate = list(free_params_Qiao_IL8_IL1b.keys())
# candidate = free_params_Qiao_Mg
# candidate = free_params_Chen
# candidate = free_params_Valles
# candidate = list(free_params_Ber.keys())
# candidate = list(free_params_all.keys())
# free_params  = {}
# for key in candidate:
#     free_params[key] = free_params_all[key]
def specifications(study):
    
    if study == 'Qiao_2021_ILs':
        studies = ['Qiao_2021_IL8_IL1b','Qiao_2021_IL8','Qiao_2021_IL1b']
        candidate = free_params_Qiao_IL8_IL1b
    elif study == 'Qiao_2021_Mg':
        studies = ['Qiao_2021_Mg']
        candidate = free_params_Qiao_Mg
    elif study == 'Ber_2016':
        studies = ['Ber_2016']
        candidate = free_params_Ber
    elif study == 'Valles_2020':
        studies = ['Valles_2020_IL10','Valles_2020_TNFa']
        candidate = free_params_Valles
    elif study == 'Chen_2018':
        studies = ['Chen_2018']
        candidate = free_params_Chen
    elif study == 'All':
        studies = ['Valles_2020_TNFa','Valles_2020_IL10','Chen_2018','Qiao_2021_IL8_IL1b','Qiao_2021_IL8','Qiao_2021_IL1b','Qiao_2021_Mg','Ber_2016']
        candidate = list(free_params_all.keys())
    else:
        raise ValueError('specifications of {} not defined.'.format(study))
    free_params  = {}
    for key in candidate:
        free_params[key] = free_params_all[key]
    obs = {'studies':studies}
    for study in studies:
        obs[study] = observations[study]

    return obs,free_params





