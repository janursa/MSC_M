"""
This script is designed to plot the inferred parameter values of a study in a normalized fashion compared to other files
"""

import os
import sys
import matplotlib.pyplot as plt
import json
import copy
import numpy as np
from scipy.stats import levene
import json
import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')
sys.path.insert(0,dir_to_dirs)
from dirs import dir_to_MSC_osteogenesis
sys.path.insert(0,dir_to_MSC_osteogenesis)
from parameters import free_params_all
plt.rcParams["font.family"] = "serif"
plt.style.use('seaborn-deep')
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

results_file = os.path.join(dir_to_dirs,'results')


class settings:
	files = {'IL':'inferred_params_IL.json',
	'Mg':'inferred_params_Mg.json',}

	axis_font = {'fontname':'Times New Roman', 'size':'15'}
	legend_font = { 'family':'Times New Roman','size':'13'}
	colors = ['indigo' , 'darkred', 'olive','royalblue']
	symbols = [ '3', '+',"o"]

def relabel(lables):
	lables_adjusted = []
	for label in lables:
		if label == 'ALP_M_n':
			adj_label = '$n_{ALP}$'
		elif label == 'ARS_M_n':
			adj_label = '$n_{ARS}$'
		elif label == 'ALP_0':
			adj_label = '$\\beta_{ALP}$'
		elif label == 'ARS_0':
			adj_label = '$\\beta_{ARS}$'
		elif label == 'Mg_stim':
			adj_label = '$p_{ms}$'
		elif label == 'Mg_dest':
			adj_label = '$p_{md}$'
		elif label == 'IL1b_ineffective':
			adj_label = '$p_{1bie}$'
		elif label == 'IL1b_stim':
			adj_label = '$p_{1bs}$'
		elif label == 'IL8_favorable':
			adj_label = '$p_{8f}$'
		elif label == 'maturity_t':
			adj_label = '$M_{t}$'
		elif label == 'early_diff_slow':
			adj_label = '$p_{es}$'
		elif label == 'early_diff_fast':
			adj_label = '$p_{ef}$'
		elif label == 'early_diff_very_fast':
			adj_label = '$p_{evf}$'
		elif label == 'late_diff_slow':
			adj_label = '$p_{ds}$'
		elif label == 'late_diff_fast':
			adj_label = '$p_{df}$'
		elif label == 'a_early_diff_stim':
			adj_label = '$\\alpha_{es}$'
		elif label == 'a_early_diff_inhib':
			adj_label = '$\\alpha_{ei}$'
		elif label == 'a_late_diff_stim':
			adj_label = '$\\alpha_{ls}$'
		elif label == 'a_late_diff_inhib':
			adj_label = '$\\alpha_{li}$'
		elif label == 'diff_time':
			adj_label = '$T_{d}$'
		elif label == 'a_Chen_2018_ALP':
			adj_label = 'a_Chen_2018_ALP'
		elif label == 'a_Chen_2018_ARS':
			adj_label = 'a_Chen_2018_ARS'
		elif label == 'a_Valles_2020_ALP':
			adj_label = 'a_Valles_2020_ALP'
		elif label == 'a_Valles_2020_ARS':
			adj_label = 'a_Valles_2020_ARS'
		elif label == 'a_Qiao_2021_ALP':
			adj_label = 'a_Qiao_2021_ALP'

		else:
			adj_label = label
		lables_adjusted.append(adj_label)
	return lables_adjusted

def edit_params(free_params_all): # get rid of this parameters
	del free_params_all['a_Chen_2018_ALP']
	del free_params_all['a_Chen_2018_ARS']
	del free_params_all['a_Valles_2020_ALP']
	del free_params_all['a_Valles_2020_ARS']
	del free_params_all['a_Qiao_2021_ALP']
	return free_params_all
free_params_all = edit_params(free_params_all)
fig = plt.figure(figsize=(3,7))
ax = fig.add_subplot(1, 1, 1)
def plot(data):
	study_n = len(data.keys())
	study_i = 0
	for (study,params),i in zip(data.items(),range(study_n)):
		xs = list(params.values())
		ys = [i for i in range(len(params.keys()))]
		for jj in range(len(xs)):
			if xs[jj] == None:
				continue
			else:
				if jj == 0:
					ax.scatter(xs[jj], ys[jj],
			                s=150,alpha = 0.8,label = study,color = settings.colors[study_i],marker =settings.symbols[study_i] )
				else:
					ax.scatter(xs[jj], ys[jj],
				                s=150,
				               alpha = 0.8,color = settings.colors[study_i],marker =settings.symbols[study_i])
				
		study_i+=1
##/ read the inferred params from the files and normalized them based on the range of the free params


data = {} # stores data based on study tag
for study,file in settings.files.items():
	with open(os.path.join(results_file,file)) as ff:
		params = json.load(ff)
	normalized_params = {}
	for key,value in free_params_all.items():
		norm_value = None
		if key not in params:
			pass
		else:
			denominator = np.mean([max(free_params_all[key]),min(free_params_all[key])])
			norm_value = params[key]/denominator
		normalized_params[key] = norm_value
	data[study] = normalized_params
plot(data = data)





plt.yticks([(i) for i in range(len(free_params_all.keys()))], relabel(free_params_all.keys()),rotation=0)
ax.set_xlim([-.25,2.25])
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
	label.set_fontname(settings.axis_font['fontname'])
	label.set_fontsize(float(settings.axis_font['size']))

plt.legend(bbox_to_anchor=(0.05, 1.07), loc='upper left', borderaxespad=0.,prop=settings.legend_font,ncol=4)
plt.xlabel('Scaled values',fontsize = 17, family = settings.axis_font['fontname'])
plt.savefig("posteriors_dispesity.svg",bbox_inches="tight")
