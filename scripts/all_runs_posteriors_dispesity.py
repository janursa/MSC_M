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
from posterior_dispersity import relabel,edit_params
plt.rcParams["font.family"] = "serif"
plt.style.use('seaborn-deep')
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

studies = ['Qiao_IL8_IL1b','Qiao_Mg']
# studies = ['Qiao_IL8_IL1b']
class settings:
	axis_font = {'fontname':'Times New Roman', 'size':'15'}
	legend_font = { 'family':'Times New Roman','size':'15'}
	title_font = { 'family':'Times New Roman','size':'14'}
	colors = ['indigo' , 'darkred', 'olive','royalblue']
	symbols = ["3" , 'x', "o",'+']
	graph_size = (6,7)
def determine_title(study):
	title = ''
	if study == 'Qiao_IL8_IL1b':
		title = 'Qiao_IL8_IL1b' 
	elif study == 'Qiao_Mg':
		title = 'Qiao_Mg'
	return title



free_params_all = edit_params(free_params_all)
def files_func(n1,n2):
	files = {}
	for i in range(n1,n2):
		key = 'A%d'%i
		value = 'inferred_params_%d.json'%i
		files[key] = value
	return files
def plot(ax,data,label_flag = False):
	study_n = len(data.keys())
	study_i = 0
	for (study,params),i in zip(data.items(),range(study_n)):
		xs = list(params.values())
		ys = [i for i in range(len(params.keys()))]
		for jj in range(len(xs)):
			if xs[jj] == None:
				continue
			else:
				if jj == 0 and label_flag:
					ax.scatter(xs[jj], ys[jj],
			                s=150,alpha = 0.8,label = study,color = settings.colors[study_i],marker =settings.symbols[study_i] )
				elif label_flag:
					ax.scatter(xs[jj], ys[jj],
				                s=150, alpha = 0.8,color = settings.colors[study_i],marker =settings.symbols[study_i])
				
				elif study_i == 0 and jj == 0:
					ax.scatter(xs[jj], ys[jj],
				                s=50,
				               alpha = 0.8,label='Indivitual run',color = settings.colors[-1],marker =settings.symbols[-1])
				else:
					ax.scatter(xs[jj], ys[jj],
				                s=50,
				               alpha = 0.8,color = settings.colors[-1],marker =settings.symbols[-1])
				
		study_i+=1

fig = plt.figure(figsize=settings.graph_size)
fig.canvas.draw()
fig.tight_layout()
fig.subplots_adjust(wspace=.02)

study_ii=0
for study in studies:
	mean_results_file = os.path.join(dir_to_dirs,'results',study)
	individual_results_file = os.path.join(mean_results_file,'batch_calibration')

	individual_files =  files_func(0,20)
	mean_files = {'Mean of 1st 200 runs':'inferred_params_0_200.json',
		'Mean of 2nd 200 runs':'inferred_params_200_400.json',
		'Mean of 400 runs':'inferred_params_0_400.json'}

	individual_data = {} # stores data based on study tag
	for file_ID,file in individual_files.items():
		with open(os.path.join(individual_results_file,file)) as ff:
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
		individual_data[file_ID] = normalized_params

	mean_data = {} # stores data based on study tag
	for file_ID,file in mean_files.items():
		with open(os.path.join(mean_results_file,file)) as ff:
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
		mean_data[file_ID] = normalized_params


	ax = fig.add_subplot(1,len(studies),study_ii+1)
	plot(ax=ax, data=individual_data)
	plot(ax=ax, data=mean_data,label_flag=True)
	ax.set_xlim([-.25,2.25])
	ax.set_xticks(ticks = [0,1,2])
	for label in (ax.get_xticklabels() + ax.get_yticklabels()):
		label.set_fontname(settings.axis_font['fontname'])
		label.set_fontsize(float(settings.axis_font['size']))
	if study_ii == 0:
		plt.yticks([(i) for i in range(len(free_params_all.keys()))], relabel(free_params_all.keys()),rotation=0)
		plt.legend(bbox_to_anchor=(0.05, 1.15), loc='upper left', borderaxespad=0.,prop=settings.legend_font,ncol=4)
	else:
		plt.yticks([], [],rotation=0)
	plt.xlabel('Scaled values',fontsize = 17, family = settings.axis_font['fontname'])
	ax.set_title(determine_title(study),fontdict =settings.title_font,fontweight='bold')
	study_ii+=1
plt.savefig("posteriors_dispesity.svg",bbox_inches="tight")