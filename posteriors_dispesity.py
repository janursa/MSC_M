"""
This script is designed to plot the inferred parameter values of a study in a normalized fashion compared to other studies
"""
import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
import os
import sys
import matplotlib.pyplot as plt
import json
import copy
import numpy as np
from scipy.stats import levene
import json
from MSC_osteogenesis import free_params
plt.rcParams["font.family"] = "serif"
plt.style.use('seaborn-deep')
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

class settings:
	params_keys = free_params.keys()
	studies = {
		'Chen_2018':'inferred_params_chen.json',
		'Valles_2019':'inferred_params_valles.json',
		'all':'inferred_params_all.json'
	}
	axis_font = {'fontname':'Times New Roman', 'size':'15'}
	legend_font = { 'family':'Times New Roman','size':'13'}
	colors = ['indigo' , 'darkred', 'royalblue', 'olive']
	symbols = ["3" , 'x', '+', "o"]
	linewidth = 1.5

##/ read the inferred params from the files and normalized them based on the range of the free params
data = {} # stores data based on study tag
for study,file in settings.studies.items():
	with open(file) as ff:
		params = json.load(ff)
	normalized_params = {}
	for key,value in params.items():
		denominator = max(free_params[key])-min(free_params[key])
		normalized_params[key] = value/denominator
	data[study] = normalized_params

fig = plt.figure(figsize=(3,12))
ax = fig.add_subplot(1, 1, 1)

study_n = len(data.keys())
for (study,params),i in zip(data.items(),range(study_n)):
	xs = params.values()
	ys = range(len(params.keys()))
	ax.scatter(xs, ys,
               marker = settings.symbols[i], s=150,color = settings.colors[i],
               alpha = 0.8,label = study)

plt.yticks([(i) for i in range(len(free_params.keys()))], free_params.keys(),rotation=0)
# ax.set_xlim([0,2])
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
	label.set_fontname(settings.axis_font['fontname'])
	label.set_fontsize(float(settings.axis_font['size']))

plt.legend(bbox_to_anchor=(0.05, 1.07), loc='upper left', borderaxespad=0.,prop=settings.legend_font,ncol=4)
plt.xlabel('Scaled values',fontsize = 17, family = settings.axis_font['fontname'])
plt.savefig("posteriors_dispesity.svg",bbox_inches="tight")



exit(2)
#read the sensitivity analsis data
pre_fix = os.path.join(current_file,'../../../','results','SA')
# sys.path.insert(1,os.path.join(current_file,'../../../','results','SA'))

SA_file_tags = ['C1','C2','C3','C1-3'];
SA_data ={}
for tag in SA_file_tags:
	with open(os.path.join(pre_fix,tag+'.json'),'r') as F:
		PTTSs = json.load(F)
	SA_data.update({tag:PTTSs})

calib_params = {
	"CD_H_t": [None,0.75,None,None],
	"MG_L_t": [None,3.95,None,3.75],
	"MG_M_t": [None,None,None,None],
	"MG_H_t": [None,None,None,None],
	"B_Mo": [0.0009,0.0004,0.0007,0.0005],
	"a_Mo": [5.68,4.24,None,5.26],
	"a_Pr_Mo": [None,None,None,7.7],
	"a_c_Mo": [54.65,None,19.26,90.79],
	"a_Diff": [3.6,3.2,7.35,4],
	"B_Pr": [0.074,0.03,0.028,0.065],
	"a_P": [1.98,8.42,16.4,2.23],
	"pH_t": [9.21,None,None,None],
	"maturity_t": [None,0.93,None,None],
	# "b_BMP": [0.04,0.015,0.04,0.016],
	# "b_TGF": [None,0.045,0.079,0.039],
	"a_m_ALP": [None,0.64,None,None],
	"a_m_OC": [None,0.54,None,0.67],
	"a_TGF_nTGF":[None,0.034,None,0.047],
	"a_BMP_nBMP":[None,0.035,None,0.045],
	"c_weight":[None,0.17,None,0.3]
}
data = {'C1':{'x':[],'y':[]},'C2':{'x':[],'y':[]},'C3':{'x':[],'y':[]},'C1-3':{'x':[],'y':[]}}
xs = [i for i in range(len(calib_params))] # x indices to mark which parameter is None and which is not
for (key,values),x in zip(calib_params.items(),xs):
	if key == 'c_weight':
		print(free_parameters[key])
		print(values)
	if values[0] != None:
		data['C1']['x'].append(x)
		standardized_value = values[0]/np.mean(free_parameters[key])
		data['C1']['y'].append(standardized_value)
	if values[1] != None:
		data['C2']['x'].append(x)
		standardized_value = values[1]/np.mean(free_parameters[key])
		data['C2']['y'].append(standardized_value)
	if values[2] != None:
		data['C3']['x'].append(x)
		standardized_value = values[2]/np.mean(free_parameters[key])
		data['C3']['y'].append(standardized_value)
	if values[3] != None:
		data['C1-3']['x'].append(x)
		standardized_value = values[3]/np.mean(free_parameters[key])
		data['C1-3']['y'].append(standardized_value)

## settings
format = '.svg'
output_dir = os.path.join(current_file,'posteriors_dispesity')



if __name__ == "__main__":
	
	labels = []
	for key in calib_params.keys():
		if key == "a_Pr_Mo":
			key = "Weight of mitotic damage "+r"($\alpha_{PM})$"
		elif key == "MG_H_t":
			key =  "Fuzzy Destructive Mg"+r"$^{2+}$"+ "ions "+r"($c_{mht}$)"
		elif key == "B_Pr":
			key =  "Base proliferation change "+r"($\gamma_{P0}$)"
		elif key == "B_Mo":
			key =  "Base mortality chance "+r"($\gamma_{M0})$"
		elif key == "a_Mo":
			key =  "Scale factor of mortality chance "+r"($\alpha_{M}$)"
		elif key == "MG_L_t":
			key =  "Fuzzy Stimulus Mg"+r"$^{2+}$"+ "ions "+r"($c_{mlt}$)"
		elif key == "MG_M_t":
			key =  "Fuzzy High Mg"+r"$^{2+}$"+ "ions "+r"($c_{mmt})$"
		elif key == "a_c_Mo":
			key =  "Scale factor of passaging damage "+r"($\alpha_{CM}$)"
		elif key == "b_BMP":
			key =  "Base rate of BMP2 synthesize "+r"($r_{g1}$)"
		elif key == "b_TGF":
			key =  "Base rate of TGF-β1 synthesize "+r"($r_{g2})$"
		elif key == "a_Diff":
			key =  "Scale factor of differentiation "+r"($\alpha_{D}$)"
		elif key == "a_P":
			key =  "Scale factor of proliferation "+r"($\alpha_{P}$)"
		elif key == "pH_t":
			key =  "pH threshold "+r"($pH_{t}$)"
		elif key == "a_TGF_nTGF":
			key =  "TGF-β1 conversion coefficient "+r"($\beta_{g2}$)"
		elif key == "a_BMP_nBMP":
			key =  "BMP2 conversion coefficient "+r"($\beta_{g1}$)"
		elif key == "maturity_t":
			key =  "Maturity threshold "+r"($M_{t}$)"
		elif key == "a_m_OC":
			key = "OC conversion coefficient "+r"($\beta_{Mo}$)"
		elif key == "a_m_ALP":
			key = "ALP conversion coefficient "+r"($\beta_{Ma}$)"
		elif key == "c_weight":
			key = "Cellular weight "+r"($w_{c}$)"
		elif key == "CD_H_t":
			key = "Fuzzy Pressed cell density "+r"($c_{cht1})$"
		else:
			print("{} is not defined ".format(key))
			raise KeyError()
		labels.append(key)
	# plot posterior dispersity
	fig = plt.figure(figsize=(3,12))
	ax = fig.add_subplot(1, 1, 1)
	i = 0
	for key,values in data.items():
		ax.scatter(values['y'] ,  values['x'],
	               marker = symbols[i], s=150,color = colors[i],alpha = 0.8,label = key)

		i+=1
	plt.yticks([(i) for i in range(len(xs))], labels,rotation=0)
	ax.set_xlim([0,2])
	for label in (ax.get_xticklabels() + ax.get_yticklabels()):
		label.set_fontname(axis_font['fontname'])
		label.set_fontsize(float(axis_font['size']))

	plt.legend(bbox_to_anchor=(0.05, 1.07), loc='upper left', borderaxespad=0.,prop=legend_font,ncol=4)
	plt.xlabel('Scaled values',fontsize = 17, family = axis_font['fontname'])
	plt.savefig(os.path.join(output_dir,"posteriors_dispesity"+format),bbox_inches="tight")

	# plot sensitity
	fig = plt.figure(figsize=(12,3))
	plot_index = 1
	for tag,data in SA_data.items():
		ax = fig.add_subplot(1, 4, plot_index)
		param_names = list(data.keys())
		PTTSs = list(data.values())
		ax.bar(  param_names,PTTSs )
		plot_index+=1
	print(plt.yticks)
	plt.savefig(os.path.join(output_dir,"SA"+format),bbox_inches="tight")

