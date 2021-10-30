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
sys.path.insert(0,current_file)
dir_to_dirs = os.path.join(current_file,'..')
sys.path.insert(0,dir_to_dirs)
from dirs import dir_to_MSC_osteogenesis
sys.path.insert(0,dir_to_MSC_osteogenesis)
from parameters import free_params_all
from posteriors_dispersity import relabel,edit_params,relabel_description
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

class settings:
	results_folder = os.path.join(dir_to_dirs,'raw_results')
	studies = ['Qiao_IL8_IL1b','Chen_2018','Valles_2020','Qiao_IL8_IL1b','Chen_2018','Valles_2020']
	# studies = ['Qiao_IL8_IL1b']
	runs = [400,200,200,400,200,200]
	# runs = [400]
	width_ration = [1,1,1,1,1,1]
	graph_dims = (1,6)
	axis_font = {'fontname':'Times New Roman', 'size':'14'}
	legend_font = { 'family':'Times New Roman','size':'14'}
	title_font = { 'family':'Times New Roman','size':'13'}
	colors = ['indigo' , 'olive', 'red','royalblue']
	symbols = [">" , '<', "o",'+']
	symbol_size_major = 70
	symbol_size_minor = 30
	alpha = .5
	fig_size = (9,7)
def determine_title(study):
	title = ''
	if study == 'Qiao_IL8_IL1b':
		title = 'C5' 
	elif study == 'Qiao_Mg':
		title = 'C1'
	elif study == 'Chen_2018':
		title = 'C3'
	elif study == 'Valles_2020':
		title = 'C4'
	elif study == 'Ber_2016':
		title = 'C2'
	elif study == 'All':
		title = 'C1-5'
	return title



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
		ys = [i for i in range(len(relabel(free_params_all.keys())))]
		first_label_flag = True
		indivitual_label_flag = True
		for jj in range(len(xs)):
			if xs[jj] == None:
				ax.scatter(0, 0,s=0.01)
			else:
				if first_label_flag == True and label_flag:
					ax.scatter(xs[jj], ys[jj],
							s=settings.symbol_size_major,alpha = settings.alpha,label = study,color = settings.colors[study_i],marker =settings.symbols[study_i] )
					first_label_flag = False
				elif label_flag:
					ax.scatter(xs[jj], ys[jj],
								s=settings.symbol_size_major, alpha = settings.alpha,color = settings.colors[study_i],marker =settings.symbols[study_i])
				
				elif indivitual_label_flag == True and study_i ==0:
					indivitual_label_flag = False
					ax.scatter(xs[jj], ys[jj],
								s=settings.symbol_size_minor,
							   alpha = settings.alpha,label='Indivitual run',color = settings.colors[-1],marker =settings.symbols[-1])
				else:
					ax.scatter(xs[jj], ys[jj],
								s=settings.symbol_size_minor,
							   alpha = settings.alpha,color = settings.colors[-1],marker =settings.symbols[-1])
				
		study_i+=1

if __name__ == '__main__':

	free_params_all = edit_params(free_params_all)
	fig = plt.figure()
	f, axes = plt.subplots(settings.graph_dims[0],settings.graph_dims[1],figsize=settings.fig_size, gridspec_kw={'width_ratios': settings.width_ration,'wspace':0.01})

	fig.subplots_adjust(wspace=.02)

	study_ii=0
	for study,run_count in zip(settings.studies,settings.runs):
		mean_results_file = os.path.join(settings.results_folder,study)
		individual_results_file = os.path.join(mean_results_file,'batch_calibration')

		# individual_files =  files_func(0,run_count)
		individual_files =  files_func(0,20)
		mean_files = {'1st half of samples':'inferred_params_0_%d.json'%int(run_count/2),
			'2nd half of samples':'inferred_params_%d_%d.json'%(run_count/2,run_count),
			'All samples':'inferred_params_0_%d.json'%run_count}

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


		ax = axes[study_ii]
		plot(ax=ax, data=individual_data)
		plot(ax=ax, data=mean_data,label_flag=True)
		# ax.set_xlim([-.25,2.25])
		ax.set_xticks(ticks = [0,1,2])
		if study_ii == 0:
			ax.set_yticks([(i) for i in range(len(free_params_all.keys()))])
			ax.set_yticklabels(relabel(free_params_all.keys()))
			ax.legend(bbox_to_anchor=(0.1, 1.13), loc='upper left', borderaxespad=0.,prop=settings.legend_font,ncol=4)

		elif study_ii == len(settings.width_ration)-1:
			ax.yaxis.set_label_position("right")
			ax.yaxis.tick_right()
			ax.set_yticks([(i) for i in range(len(free_params_all.keys()))])
			ax.set_yticklabels(relabel_description(free_params_all.keys()))
			left_edge = ax.spines["left"]
			left_edge.set_visible(False)


		else:
			left_edge = ax.spines["left"]
			left_edge.set_visible(False)
			ax.set_yticks([], [])

		ax.set_xticks([], [])
		# plt.xlabel('Scaled values',fontsize = 17, family = settings.axis_font['fontname'])
		ax.set_title(determine_title(study),fontdict =settings.title_font,fontweight = 'normal')
		study_ii+=1
	# plt.yticks([(i) for i in range(len(free_params_all.keys()))], relabel_description(free_params_all.keys()),rotation=0,fontweight='normal')
	for ax in axes:
		for label in (ax.get_xticklabels() + ax.get_yticklabels()):
			label.set_fontname(settings.axis_font['fontname'])
			label.set_fontsize(float(settings.axis_font['size']))
	# plt.text(0,-3, "Scaled values",**settings.title_font,
	#     horizontalalignment='center',
	#     verticalalignment='bottom')
	plt.savefig("posteriors_dispesity_all_runs.svg",bbox_inches="tight")
