import json
params_tags = {
    "a_Ber_2016_ALP": 0.6444057307430728,
    "a_Ber_2016_OC": 0.3933937521602641,
    "a_Valles_2020_ALP": 295.08832988425524,
    "a_Valles_2020_ARS": 691.0534145890491,
    "a_Chen_2018_ALP": 6.8988950274256045,
    "a_Chen_2018_ARS": 3.3007964775324807,
    "a_Qiao_2021_ALP": 31.66674314667242,
    "a_early_diff_stim": 8.612968136844628,
    "a_early_diff_inhib": 10.522441210151719,
    "a_late_diff_stim": 9.625923509720542,
    "a_late_diff_inhib": 9.91032038882803,
    "early_diff_slow": 0.25817386154512684,
    "early_diff_fast": 0.5846378310735942,
    "early_diff_very_fast": 0.8065433120464044,
    "late_diff_slow": 0.24058079009091748,
    "late_diff_fast": 0.7488612215358651,
    "Mg_stim": 8.666826458542669,
    "Mg_dest": 29.30558324294535,
    "IL1b_ineffective": 113.90711065973714,
    "IL1b_stim": 3.8761376310618014,
    "IL8_favorable": 9.937834285182312,
    "ALP_M_n": 1.6559117863917923,
    "ARS_M_n": 1.1200818866189335,
    "OC_M_n": 0.2235665824739317,
    "ALP_0": 0.3997589315686792,
    "ARS_0": 0.1704367079411658,
    "OC_0": 5.280803869675005,
    "diff_time": 867.6315379238918,
    "maturity_t": 0.7737321176835812
}
params_tags = list(params_tags.keys())

dir_c1_5 = '/Users/matin/Downloads/testProjs/MSC_M/results/All/inferred_params_0_200.json'
dir_c1 = '/Users/matin/Downloads/testProjs/MSC_M/results/Qiao_2021_Mg/inferred_params_0_200.json'
dir_c2 = '/Users/matin/Downloads/testProjs/MSC_M/results/Ber_2016/inferred_params_0_120.json'
dir_c3 = '/Users/matin/Downloads/testProjs/MSC_M/results/Valles_2020/inferred_params_100_200.json'
dir_c4 = '/Users/matin/Downloads/testProjs/MSC_M/results/Chen_2018/inferred_params_0_200.json'
dir_c5 = '/Users/matin/Downloads/testProjs/MSC_M/results/Qiao_2021_ILs/inferred_params_0_70.json'

dirs = [dir_c1,dir_c2,dir_c3,dir_c4,dir_c5,dir_c1_5]
data = {}
for i in range(6):
	with open(dirs[i],'r') as file:
		data_file = json.load(file)
		data[i+1] = data_file
file_data = ""
for param_tag in params_tags:
	log_string = param_tag+'\t'
	for i in range(1,7):
		data_i = data[i]
		if param_tag in data_i.keys():
			if param_tag == 'diff_time':
				value = data_i[param_tag]/24
				value = round(value,1)
			elif param_tag == 'maturity_t':
				value = round(data_i[param_tag],2)
			else:
				value = data_i[param_tag]
			log_string+=  str(value)+'\t'
		else:
			log_string+= '-'+'\t'
	
	file_data+=log_string+'\n'
with open('params_values.txt','w') as f:
	f.write(file_data)



