
fixed_params = {
    'ALP_M_n':1, # n in the equation ALP = a*(M^n + ALP_0)
    'ARS_M_n':1,
    'ALP_0':.2, # the default value of ALP when maturity is zero
    'ARS_0':.2, # the default value of ARS when maturity is zero

    'Mg_stim':5, # stimulatory conc of Mg
    'Mg_dest':30, # detrimental conc of Mg
    'IL1b_ineffective':120, # detrimental threshold IL1b
    'IL1b_stim':10,
    'IL8_favorable':25, # medium threshold for IL8

    'maturity_t':.5, # early maturity threshold 
    'early_diff_slow':.25, # center of low membership function
    'early_diff_fast':.65, # center of high membership function
    'early_diff_very_fast':.85, # center of high membership function
    'late_diff_slow':.25, # center of low membership function
    'late_diff_fast':.75, # center of high membership function
    'a_early_diff_stim':1, # scale factor, stimulatory
    'a_early_diff_inhib':2, # scale factor, inhibitory
    'a_late_diff_stim':2, # scale factor
    'a_late_diff_inhib':2, # scale factor
    'diff_time':30*24, # days required for full differentiation   

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
    'ALP_M_n':[0,20], # n in the equation ALP = a*(M^n + ALP_0)
    'ARS_M_n':[0,10], # n in the equation ARS = a*(M^n + ARS_0)
    'ALP_0':[0,10], # the default value of ALP when maturity is zero
    'ARS_0':[0,1], # the default value of ARS when maturity is zero

    'Mg_stim':[2,10], # stimulatory conc of Mg --
    'Mg_dest':[20,40], # detrimental conc of Mg --
    'IL1b_ineffective':[30,199], # high threshold IL1b --
    'IL1b_stim':[1,29], # stimulatory threshold of IL1b --
    'IL8_favorable':[1,99], # medium threshold for IL8 --

    'maturity_t':[0,1], # early maturity threshold.  ----
    'early_diff_slow':[0.1,0.4], # center of low membership function --
    'early_diff_fast':[0.5,0.75], # center of high membership function --
    'early_diff_very_fast':[0.6,1], # center of high membership function --
    'late_diff_slow':[0.1,0.4], # center of low membership function --
    'late_diff_fast':[0.6,0.9], # center of high membership function --
    'a_early_diff_stim':[0,5], # scale factor, upregulatory --
    'a_early_diff_inhib':[0,1], # scale factor, downregulatory --
    'a_late_diff_stim':[0,5], # scale factor --
    'a_late_diff_inhib':[0,1], # scale factor --
    'diff_time':[15*24,45*24], # days required for full differentiation ---

    'a_Chen_2018_ALP':[0,10],
    'a_Chen_2018_ARS':[0,10],

    'a_Valles_2020_ALP':[0,1000],
    'a_Valles_2020_ARS':[0,1000],

    'a_Qiao_2021_ALP':[0,200],
}
free_params_Qiao_Mg = {
    'ALP_M_n':[0,20], # n in the equation ALP = a*(M^n + ALP_0)
    # 'ARS_M_n':[0,10], # n in the equation ARS = a*(M^n + ARS_0)
    'ALP_0':[0,10], # the default value of ALP when maturity is zero
    # 'ARS_0':[0,1], # the default value of ARS when maturity is zero

    'Mg_stim':[2,10], # stimulatory conc of Mg --
    'Mg_dest':[20,40], # detrimental conc of Mg --
    # 'IL1b_ineffective':[30,199], # high threshold IL1b --
    # 'IL1b_stim':[1,29], # stimulatory threshold of IL1b --
    # 'IL8_favorable':[1,99], # medium threshold for IL8 --

    'maturity_t':[0,1], # early maturity threshold.  ----
    # 'early_diff_slow':[0.1,0.4], # center of low membership function --
    'early_diff_fast':[0.5,0.75], # center of high membership function --
    # 'early_diff_very_fast':[0.6,1], # center of high membership function --
    # 'late_diff_slow':[0.1,0.4], # center of low membership function --
    # 'late_diff_fast':[0.6,0.9], # center of high membership function --
    'a_early_diff_stim':[0,5], # scale factor, upregulatory --
    # 'a_early_diff_inhib':[0,1], # scale factor, downregulatory --
    # 'a_late_diff_stim':[0,5], # scale factor --
    # 'a_late_diff_inhib':[0,1], # scale factor --
    'diff_time':[15*24,45*24], # days required for full differentiation ---

    # 'a_Chen_2018_ALP':[0,10],
    # 'a_Chen_2018_ARS':[0,10],

    'a_Valles_2020_ALP':[0,1000],
    # 'a_Valles_2020_ARS':[0,1000],

    # 'a_Qiao_2021_ALP':[0,200],
}
free_params_Qiao_IL8_IL1b = {
    'ALP_M_n':[0,20], # n in the equation ALP = a*(M^n + ALP_0)
    # 'ARS_M_n':[0,10], # n in the equation ARS = a*(M^n + ARS_0)
    'ALP_0':[0,10], # the default value of ALP when maturity is zero
    # 'ARS_0':[0,1], # the default value of ARS when maturity is zero

    # 'Mg_stim':[2,10], # stimulatory conc of Mg --
    # 'Mg_dest':[20,40], # detrimental conc of Mg --
    'IL1b_ineffective':[30,199], # high threshold IL1b --
    'IL1b_stim':[1,29], # stimulatory threshold of IL1b --
    'IL8_favorable':[1,99], # medium threshold for IL8 --

    'maturity_t':[0,1], # early maturity threshold.  ----
    # 'early_diff_slow':[0.1,0.4], # center of low membership function --
    # 'early_diff_fast':[0.5,0.75], # center of high membership function --
    'early_diff_very_fast':[0.6,1], # center of high membership function --
    # 'late_diff_slow':[0.1,0.4], # center of low membership function --
    # 'late_diff_fast':[0.6,0.9], # center of high membership function --
    'a_early_diff_stim':[0,5], # scale factor, upregulatory --
    # 'a_early_diff_inhib':[0,1], # scale factor, downregulatory --
    # 'a_late_diff_stim':[0,5], # scale factor --
    # 'a_late_diff_inhib':[0,1], # scale factor --
    'diff_time':[15*24,45*24], # days required for full differentiation ---

    # 'a_Chen_2018_ALP':[0,10],
    # 'a_Chen_2018_ARS':[0,10],

    # 'a_Valles_2020_ALP':[0,1000],
    # 'a_Valles_2020_ARS':[0,1000],

    'a_Qiao_2021_ALP':[0,200],
}
free_params_Chen = {
    'ALP_M_n':[0,20], # n in the equation ALP = a*(M^n + ALP_0)
    'ARS_M_n':[0,10], # n in the equation ARS = a*(M^n + ARS_0)
    'ALP_0':[0,10], # the default value of ALP when maturity is zero
    'ARS_0':[0,1], # the default value of ARS when maturity is zero

    # 'Mg_stim':[2,10], # stimulatory conc of Mg --
    # 'Mg_dest':[20,40], # detrimental conc of Mg --
    # 'IL1b_ineffective':[30,199], # high threshold IL1b --
    # 'IL1b_stim':[1,29], # stimulatory threshold of IL1b --
    # 'IL8_favorable':[1,99], # medium threshold for IL8 --

    'maturity_t':[0,1], # early maturity threshold.  ----
    'early_diff_slow':[0.1,0.4], # center of low membership function --
    'early_diff_fast':[0.5,0.75], # center of high membership function --
    'early_diff_very_fast':[0.6,1], # center of high membership function --
    'late_diff_slow':[0.1,0.4], # center of low membership function --
    'late_diff_fast':[0.6,0.9], # center of high membership function --
    'a_early_diff_stim':[0,5], # scale factor, upregulatory --
    'a_early_diff_inhib':[0,1], # scale factor, downregulatory --
    'a_late_diff_stim':[0,5], # scale factor --
    'a_late_diff_inhib':[0,1], # scale factor --
    'diff_time':[15*24,45*24], # days required for full differentiation ---

    'a_Chen_2018_ALP':[0,10],
    'a_Chen_2018_ARS':[0,10],

    # 'a_Valles_2020_ALP':[0,1000],
    # 'a_Valles_2020_ARS':[0,1000],

    # 'a_Qiao_2021_ALP':[0,200],
}
free_params_Valles = {
    'ALP_M_n':[0,20], # n in the equation ALP = a*(M^n + ALP_0)
    'ARS_M_n':[0,10], # n in the equation ARS = a*(M^n + ARS_0)
    'ALP_0':[0,10], # the default value of ALP when maturity is zero
    'ARS_0':[0,1], # the default value of ARS when maturity is zero

    # 'Mg_stim':[2,10], # stimulatory conc of Mg --
    # 'Mg_dest':[20,40], # detrimental conc of Mg --
    # 'IL1b_ineffective':[30,199], # high threshold IL1b --
    # 'IL1b_stim':[1,29], # stimulatory threshold of IL1b --
    # 'IL8_favorable':[1,99], # medium threshold for IL8 --

    'maturity_t':[0,1], # early maturity threshold.  ----
    'early_diff_slow':[0.1,0.4], # center of low membership function --
    'early_diff_fast':[0.5,0.75], # center of high membership function --
    'early_diff_very_fast':[0.6,1], # center of high membership function --
    'late_diff_slow':[0.1,0.4], # center of low membership function --
    'late_diff_fast':[0.6,0.9], # center of high membership function --
    'a_early_diff_stim':[0,5], # scale factor, upregulatory --
    'a_early_diff_inhib':[0,1], # scale factor, downregulatory --
    'a_late_diff_stim':[0,5], # scale factor --
    'a_late_diff_inhib':[0,1], # scale factor --
    'diff_time':[15*24,45*24], # days required for full differentiation ---

    # 'a_Chen_2018_ALP':[0,10],
    # 'a_Chen_2018_ARS':[0,10],

    'a_Valles_2020_ALP':[0,1000],
    'a_Valles_2020_ARS':[0,1000],

    # 'a_Qiao_2021_ALP':[0,200],
}

# free_params = free_params_Qiao_IL8_IL1b
# free_params = free_params_Qiao_Mg
# free_params = free_params_Chen
free_params = free_params_Valles