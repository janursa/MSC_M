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
		'IL8':'inferred_params_IL8.json',
		'IL1b':'inferred_params_IL1b.json',
		'IL8_all':'inferred_params_IL8_all.json',
		'IL1b_all':'inferred_params_IL1b_all.json'
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
		denominator = np.mean([max(free_params[key]),min(free_params[key])])
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


