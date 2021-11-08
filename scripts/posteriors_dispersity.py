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
# plt.rcParams["font.family"] = "serif"
# plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

class settings:
	results_folder = os.path.join(dir_to_dirs,'results')
	studies = {
		'Qiao_2021_Mg':{'individual_files':'Qiao_2021_Mg/batch_calibration',
						'mean_folder':'Qiao_2021_Mg',
						'run_count':200},
		'Ber_2016':{  'individual_files':'Ber_2016/batch_calibration',
						'mean_folder':'Ber_2016',
						'run_count':120},
		'Valles_2020':{ 'individual_files':'Valles_2020/batch_calibration',
						'mean_folder':'Valles_2020',
						'run_count':200},
		'Chen_2018':{	'individual_files':'Chen_2018/batch_calibration',
		                'mean_folder':'Chen_2018',
						'run_count':200},
		'Qiao_2021_ILs':{
						'individual_files':'Qiao_2021_ILs/batch_calibration',
						'mean_folder':'Qiao_2021_ILs',
						'run_count':400},
		'All':{
						'individual_files':'All/batch_calibration',
						'mean_folder':'All',
						'run_count':200},
	}
	width_ration = [1.1,1]
	graph_dims = (1,2)
	axis_font = {'fontname':'Times New Roman', 'size':'14'}
	legend_font = { 'family':'Times New Roman','size':'13'}
	title_font = { 'family':'Times New Roman','size':'14','fontweight':'bold'}
	colors_dispersity = ['indigo' , 'darkred', 'olive','royalblue','blue','red']
	symbols_dispersity = [ '1', '2',"3",'4','+','o']

	colors_distribution = ['indigo' , 'olive', 'red','green']
	symbols_distribution = [ '>', '<','o','x']

	symbol_size_major = 100
	symbol_size_minor = 30
	alpha = .6
	fig_size = (6,7)
def determine_title(study):
	title = ''
	if study == 'Qiao_2021_Mg':
		title = 'C1'
	elif study == 'Ber_2016':
		title = 'C2'
	elif study == 'Valles_2020':
		title = 'C3'
	elif study == 'Chen_2018':
		title = 'C4'
	elif study == 'Qiao_2021_ILs':
		title = 'C5' 
	elif study == 'All':
		title = 'C1-5'
	return title

def relabel(lables):
	lables_adjusted = []
	for label in lables:
		if label == 'ALP_M_n':
			adj_label = r'$n_{ALP}$'
		elif label == 'ARS_M_n':
			adj_label = '$n_{ARS}$'
		elif label == 'OC_M_n':
			adj_label = '$n_{OC}$'
		elif label == 'ALP_0':
			adj_label = '$\\beta_{ALP}$'
		elif label == 'ARS_0':
			adj_label = '$\\beta_{ARS}$'
		elif label == 'OC_0':
			adj_label = '$\\beta_{OC}$'
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
			adj_label = '$p_{ls}$'
		elif label == 'late_diff_fast':
			adj_label = '$p_{lf}$'
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
			adj_label = '$k_{ALP,2}$'
		elif label == 'a_Chen_2018_ARS':
			adj_label = '$k_{ARS,2}$'
		elif label == 'a_Valles_2020_ALP':
			adj_label = '$k_{ALP,3}$'
		elif label == 'a_Valles_2020_ARS':
			adj_label = '$k_{ARS,3}$'
		elif label == 'a_Qiao_2021_ALP':
			adj_label = '$k_{ALP,1}$'
		elif label == 'a_Ber_2016_ALP':
			adj_label = '$k_{ALP,4}$'
		elif label == 'a_Ber_2016_OC':
			adj_label = '$k_{OC,4}$'
		else:
			adj_label = label
		lables_adjusted.append(adj_label)
	return lables_adjusted

def relabel_description(lables):
	lables_adjusted = []
	for label in lables:
		if label == 'ALP_M_n':
			adj_label = r'$n_{ALP}$'+r': nonlinearity of ALP-maturity '
		elif label == 'ARS_M_n':
			adj_label = '$n_{ARS}$'+': nonlinearity of ARS-maturity '
		elif label == 'OC_M_n':
			adj_label = '$n_{OC}$'+': nonlinearity of OC-maturity '
		elif label == 'ALP_0':
			adj_label = '$\\beta_{ALP}$'+': ALP baseline'
		elif label == 'ARS_0':
			adj_label = '$\\beta_{ARS}$'+': ARS baseline'
		elif label == 'OC_0':
			adj_label = '$\\beta_{OC}$'+': OC baseline'
		elif label == 'Mg_stim':
			adj_label = '$p_{ms}$'+': fuzzy Stimulatory Mg$^{2+}$ ions'
		elif label == 'Mg_dest':
			adj_label = '$p_{md}$'+': fuzzy Destructive Mg$^{2+}$ ions'
		elif label == 'IL1b_ineffective':
			adj_label = '$p_{1bie}$'+': fuzzy Ineffective IL-1$\\beta$'
		elif label == 'IL1b_stim':
			adj_label = '$p_{1bs}$'+': fuzzy Stimulatory IL-1$\\beta$'
		elif label == 'IL8_favorable':
			adj_label = '$p_{8f}$'+': fuzzy Favorable IL-8'
		elif label == 'maturity_t':
			adj_label = '$M_{t}$'+': early maturity threshold'
		elif label == 'early_diff_slow':
			adj_label = '$p_{es}$'+': fuzzy Slow early diff.'
		elif label == 'early_diff_fast': 
			adj_label = '$p_{ef}$'+': fuzzy Fast early diff.'
		elif label == 'early_diff_very_fast':
			adj_label = '$p_{evf}$'+': fuzzy Very fast early diff.'
		elif label == 'late_diff_slow':
			adj_label = '$p_{ls}$'+': fuzzy Slow late diff.'
		elif label == 'late_diff_fast':
			adj_label = '$p_{lf}$'+': fuzzy Fast late diff.'
		elif label == 'a_early_diff_stim':
			adj_label = '$\\alpha_{es}$'+': scale early diff., stimulatory'
		elif label == 'a_early_diff_inhib':
			adj_label = '$\\alpha_{ei}$'+': scale early diff., inhibitory'
		elif label == 'a_late_diff_stim':
			adj_label = '$\\alpha_{ls}$'+': scale late diff., stimulatory'
		elif label == 'a_late_diff_inhib':
			adj_label = '$\\alpha_{li}$'+': scale late diff., inhibitory'
		elif label == 'diff_time':
			adj_label = '$T_{d}$' + ': differentiation time'
		elif label == 'a_Chen_2018_ALP':
			adj_label = '$k_{ALP,2}$'+': scale factor of ALP in study 2'
		elif label == 'a_Chen_2018_ARS':
			adj_label = '$k_{ARS,2}$'+': scale factor of ARS in study 2'
		elif label == 'a_Valles_2020_ALP':
			adj_label = '$k_{ALP,3}$'+': scale factor of ALP in study 3'
		elif label == 'a_Valles_2020_ARS':
			adj_label = '$k_{ARS,3}$'+': scale factor of ARS in study 3'
		elif label == 'a_Qiao_2021_ALP':
			adj_label = '$k_{ALP,1}$'+': scale factor of ALP in study 1'
		elif label == 'a_Ber_2016_ALP':
			adj_label = '$k_{ALP,4}$'+': scale factor of ALP in study 4'
		elif label == 'a_Ber_2016_OC':
			adj_label = '$k_{OC,4}$'+': scale factor of OC in study 4'
		else:
			adj_label = label
		lables_adjusted.append(adj_label)
	return lables_adjusted

def edit_params(free_params_all): # get rid of this parameters
	del free_params_all['a_Chen_2018_ALP']
	del free_params_all['a_Chen_2018_ARS']
	del free_params_all['a_Valles_2020_ALP']
	del free_params_all['a_Valles_2020_ARS']
	del free_params_all['a_Ber_2016_ALP']
	del free_params_all['a_Ber_2016_OC']
	del free_params_all['a_Qiao_2021_ALP']
	return free_params_all


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
							s=settings.symbol_size_major,alpha = settings.alpha,label = study,color = settings.colors_distribution[study_i],marker =settings.symbols_distribution[study_i] )
					first_label_flag = False
				elif label_flag:
					ax.scatter(xs[jj], ys[jj],
								s=settings.symbol_size_major, alpha = settings.alpha,color = settings.colors_distribution[study_i],marker =settings.symbols_distribution[study_i])
				
				elif indivitual_label_flag == True and study_i ==0:
					indivitual_label_flag = False
					ax.scatter(xs[jj], ys[jj],
								s=settings.symbol_size_minor,
							   alpha = settings.alpha,label='Single run',color = settings.colors_distribution[-1],marker =settings.symbols_distribution[-1])
				else:
					ax.scatter(xs[jj], ys[jj],
								s=settings.symbol_size_minor,
							   alpha = settings.alpha,color = settings.colors_distribution[-1],marker =settings.symbols_distribution[-1])
				
		study_i+=1
def normalize(free_params_all,params):
	normalized_params = {}
	for key,value in free_params_all.items():
		norm_value = None
		if key not in params:
			pass
		else:
			denominator = np.mean([max(free_params_all[key]),min(free_params_all[key])])
			norm_value = params[key]/denominator
		normalized_params[key] = norm_value
	return normalized_params
if __name__ == '__main__':

	free_params_all = edit_params(free_params_all)
	fig = plt.figure()
	f, axes = plt.subplots(settings.graph_dims[0],settings.graph_dims[1],figsize=settings.fig_size, gridspec_kw={'width_ratios': settings.width_ration,'wspace':0.01})

	fig.subplots_adjust(wspace=.5)

	#// retreive the data for the distribution plot of All study
	study = 'All'
	run_count = settings.studies[study]['run_count']
	mean_results_folder = os.path.join(settings.results_folder,settings.studies[study]['mean_folder'])
	individual_results_folder = os.path.join(settings.results_folder,settings.studies[study]['individual_files'])

	# individual_files =  files_func(0,run_count)
	individual_files =  files_func(0,20)
	mean_files = {'1$^{st}$ batch':'inferred_params_0_%d.json'%int(run_count/2),
		'2$^{nd}$ batch':'inferred_params_%d_%d.json'%(run_count/2,run_count),
		'All samples':'inferred_params_0_%d.json'%run_count}

	individual_data = {} # stores data based on study tag
	for file_ID,file in individual_files.items():
		with open(os.path.join(individual_results_folder,file)) as ff:
			params = json.load(ff)
		individual_data[file_ID] = normalize(free_params_all=free_params_all,params=params)
	

	mean_data = {} # stores data based on study tag
	for file_ID,file in mean_files.items():
		with open(os.path.join(mean_results_folder,file)) as ff:
			params = json.load(ff)
		
		mean_data[file_ID] = normalize(free_params_all=free_params_all,params=params)

	#// retreive the data for the dispersity plot of individual studies vs each other
	dispersity_data = {} # stores data based on study tag
	for study,run_count in settings.studies.items():
		run_count = settings.studies[study]['run_count']
		mean_file = os.path.join(settings.studies[study]['mean_folder'],'inferred_params_0_%d.json'%run_count)
		with open(os.path.join(settings.results_folder,mean_file)) as ff:
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
		dispersity_data[study] = normalized_params
	#// plot distributions
	ax = axes[0]
	plot(ax=ax, data=individual_data)
	plot(ax=ax, data=mean_data,label_flag=True)
	ax.set_xticks([], [])
	ax.set_yticks([])
	# ax.set_yticks([(i) for i in range(len(free_params_all.keys()))])
	# ax.set_yticklabels(relabel(free_params_all.keys()))
	# ax.set_title('(A) Dispersity of the inferred values for C1-5',fontdict =settings.title_font,fontweight = 'bold')
	ax.legend(bbox_to_anchor=(-0.06, 1.15), loc='upper left', borderpad=.7,labelspacing=.5,handlelength=.05,prop=settings.legend_font,ncol=2)
	
	#// plot dispersity
	ax = axes[1]
	study_n = len(dispersity_data.keys())
	study_i = 0
	for (study,params),i in zip(dispersity_data.items(),range(study_n)):
		xs = list(params.values())
		ys = [i for i in range(len(params.keys()))]
		label_flag = True
		for jj in range(len(xs)):
			if xs[jj] == None:
				continue
			else:
				if label_flag == True:
					ax.scatter(xs[jj], ys[jj],
			                s=settings.symbol_size_major,alpha = settings.alpha,label = determine_title(study),color = settings.colors_dispersity[study_i],marker =settings.symbols_dispersity[study_i] )
					label_flag = False
				else:
					ax.scatter(xs[jj], ys[jj],
				                s=settings.symbol_size_major,
				               alpha = settings.alpha,color = settings.colors_dispersity[study_i],marker =settings.symbols_dispersity[study_i])
				
		study_i+=1
	ax.yaxis.set_label_position("right")
	ax.yaxis.tick_right()
	ax.set_yticks([(i) for i in range(len(free_params_all.keys()))])
	ax.set_yticklabels(relabel_description(free_params_all.keys()))
	# left_edge = ax.spines["left"]
	# left_edge.set_visible(False)
	ax.set_xticks([], [])
	# plt.xlabel('Scaled values',fontsize = 17, family = settings.axis_font['fontname'])
	# ax.set_title('(B) Dispersity of the inferred values from different calibration schemes',fontdict =settings.title_font,fontweight = 'bold')
	ax.legend(bbox_to_anchor=(-.03, 1.15), loc='upper left', borderpad=.7,labelspacing=.5,handlelength=0,prop=settings.legend_font,ncol=3)

	# plt.yticks([(i) for i in range(len(free_params_all.keys()))], relabel_description(free_params_all.keys()),rotation=0,fontweight='normal')
	for ax in axes:
		for label in (ax.get_xticklabels() + ax.get_yticklabels()):
			label.set_fontname(settings.axis_font['fontname'])
			label.set_fontsize(float(settings.axis_font['size']))
		ax.set_xlim([-.25,2.25])
	# plt.text(0,-3, "Scaled values",**settings.title_font,
	#     horizontalalignment='center',
	#     verticalalignment='bottom')
	plt.text(-3,27,"(A) Inferred values obtained \n during multiple runs of C1-5",**settings.title_font,
		horizontalalignment='left',
		verticalalignment='center')
	plt.text(-.25,27,"(B) Inferred values obtained during \n different calibration scenarios",**settings.title_font,
		horizontalalignment='left',
		verticalalignment='center')
	plt.savefig("posteriors_dispesity.svg",bbox_inches="tight")
