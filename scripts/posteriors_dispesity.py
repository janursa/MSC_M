"""
This script is designed to plot the inferred parameter values of a study in a normalized fashion compared to other studies
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

def studies_func(n):
	studies = {}
	for i in range(n):
		key = 'A%d'%i
		value = 'inferred_params_%d.json'%i
		studies[key] = value
	return studies

class settings:
	# studies =  studies_func(2)
	studies = {'IL':'inferred_params_IL.json',
	'Mg':'inferred_params_Mg.json',}

	axis_font = {'fontname':'Times New Roman', 'size':'15'}
	legend_font = { 'family':'Times New Roman','size':'13'}
	colors = ['indigo' , 'darkred', 'royalblue', 'olive']
	symbols = ["3" , 'x', '+', "o"]
	linewidth = 1.5

##/ read the inferred params from the files and normalized them based on the range of the free params
data = {} # stores data based on study tag
for study,file in settings.studies.items():
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

fig = plt.figure(figsize=(3,12))
ax = fig.add_subplot(1, 1, 1)

study_n = len(data.keys())
study_i = 0
for (study,params),i in zip(data.items(),range(study_n)):
	xs = list(params.values())
	ys = [i for i in range(len(params.keys()))]
	# ax.scatter(xs, ys,
 #               marker = settings.symbols[i], s=150,color = settings.colors[i],
 #               alpha = 0.8,label = study)
	for jj in range(len(xs)):
		if xs[jj] == None:
			continue
		else:
			if jj == 0:
				ax.scatter(xs[jj], ys[jj],
			                s=150,
			               alpha = 0.8,label = study,color = settings.colors[study_i],marker =settings.symbols[study_i] )
			else:
				ax.scatter(xs[jj], ys[jj],
			                s=150,
			               alpha = 0.8,color = settings.colors[study_i],marker =settings.symbols[study_i] )
	study_i+=1

plt.yticks([(i) for i in range(len(free_params_all.keys()))], free_params_all.keys(),rotation=0)
# ax.set_xlim([0,2])
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
	label.set_fontname(settings.axis_font['fontname'])
	label.set_fontsize(float(settings.axis_font['size']))

plt.legend(bbox_to_anchor=(0.05, 1.07), loc='upper left', borderaxespad=0.,prop=settings.legend_font,ncol=4)
plt.xlabel('Scaled values',fontsize = 17, family = settings.axis_font['fontname'])
plt.savefig("posteriors_dispesity.svg",bbox_inches="tight")
