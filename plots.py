import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "serif"
plt.style.use('seaborn-deep')
# plt.style.use('Agg')
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
##/ post processing and plotting //##
class Plot_bar:
	"""
	Plots the results of a study by allocting a figure for each target and a bar for each ID
	"""
	def __init__(self,study,observations):
		self.measurement_scheme = observations[study]['measurement_scheme']
		self.study = study
		self.observations = observations
		if study == 'Valles_2020_IL10':
			self.graph_size = [10,10]
			self.bar_width = .2
			self.error_bar_width = .2
			self.colors = ['lime' , 'violet', 'yellowgreen', 'peru', 'skyblue']
			self.legend_font_size = 30
			self.tick_font_size = 30
			self.title_font_size = 30 
			self.delta = .1
		elif study == 'Qiao_2021_IL8':
			self.graph_size = [10,10]
			self.bar_width = .2
			self.error_bar_width = .2
			self.colors = ['lime' , 'violet', 'yellowgreen', 'peru', 'skyblue']
			self.legend_font_size = 30
			self.tick_font_size = 30
			self.title_font_size = 30 
			self.delta = .1
		elif study == 'Qiao_2021_IL1b':
			self.graph_size = [10,10]
			self.bar_width = .2
			self.error_bar_width = .2
			self.colors = ['lime' , 'violet', 'yellowgreen', 'peru', 'skyblue']
			self.legend_font_size = 30
			self.tick_font_size = 30
			self.title_font_size = 30 
			self.delta = .1
		elif study == 'Chen_2018':
			self.graph_size = [10,10]
			self.bar_width = .2
			self.error_bar_width = .2
			self.colors = ['lime' , 'violet', 'yellowgreen', 'peru', 'skyblue']
			self.legend_font_size = 30
			self.tick_font_size = 30
			self.title_font_size = 30 
			self.delta = .1
		elif study == 'Valles_2020_TNFa':
			self.graph_size = [10,10]
			self.bar_width = .2
			self.error_bar_width = .2
			self.colors = ['lime' , 'violet', 'yellowgreen', 'peru', 'skyblue']
			self.legend_font_size = 30
			self.tick_font_size = 30
			self.title_font_size = 30 
			self.delta = .1
		else:
			raise ValueError('input not defined')
	def plot(self,simulation_results):
		##/ sort out based on the measurement_scheme
		IDs = list(simulation_results.keys())
		x_labels = self.adjust_x_label(IDs)
		exp_target_results,sim_target_results = self.sort(simulation_results)
		x_exp,x_sim = self.bar_positions(simulation_results)

		##/ plot for each target
		target_n = len(self.measurement_scheme)
		fig = plt.figure(figsize=(self.graph_size[0],self.graph_size[1]))
		fig.canvas.draw()
		fig.tight_layout()
		for target,ii in zip(self.measurement_scheme.keys(),range(target_n)):
			ax = fig.add_subplot(target_n,1,ii+1)
			sim_values = [item[0] for item in sim_target_results[target]]
			ax.bar(x=x_sim,height=sim_values,width = self.bar_width, label = "Sim", 
					facecolor = self.colors[0],
					 edgecolor="black", yerr =  0,
					 error_kw = dict(capsize= self.error_bar_width))
			exp_values = [exp_target_results[target][i]['mean'] for i in range(len(exp_target_results[target]))]
			exp_values = [item[0] for item in exp_values]
			ax.bar(x=x_exp,height=exp_values,width = self.bar_width, label = 'Exp', 
					facecolor = self.colors[1],
					 edgecolor="black", yerr =  0,
					 error_kw = dict(capsize= self.error_bar_width))
			
			ax.legend(bbox_to_anchor=(2, 1),loc = 'upper right', borderaxespad=2,prop={ 'family':'Times New Roman','size':self.legend_font_size},ncol=1)
		#     ax.set_ylim(yrange)
			# x_labels = [item.get_text() for item in ax.get_xticklabels()]
			ax.set_xticks(ticks = x_sim)
			ax.set_xticklabels(x_labels)

		#     ax.get_yaxis().set_major_formatter(
		#         matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x)/1000, ',')))
			for label in (ax.get_xticklabels() + ax.get_yticklabels()):
				label.set_fontname('Times New Roman')
				label.set_fontsize(self.tick_font_size)
			ax.set_ylabel('yaxis_title',fontdict ={'family':'Times New Roman','size':self.title_font_size})
			# ax.set_xlabel('Days',fontdict ={'family':'Times New Roman','size':self.title_font_size})

			ax.set_title(target,fontdict ={'family':'Times New Roman','size':self.title_font_size, 'fontweight':'bold'})
			plt.savefig(self.study+'.svg',bbox_inches='tight')

	def sort(self,sim_results):
		exp_target_results = {}
		for target in self.measurement_scheme:
			exp_target_results[target] = []
		for target in self.measurement_scheme:
			for ID in self.observations[self.study]['IDs']:
				ID_observations = self.observations[self.study][ID]['expectations']
				exp_target_results[target].append(ID_observations[target])
		sim_target_results = {}
		for target in self.measurement_scheme:
			sim_target_results[target] = []
		for target in self.measurement_scheme:
			for ID,ID_result in sim_results.items():
				sim_target_results[target].append(ID_result[target])
		return exp_target_results,sim_target_results
	def bar_positions(self,sim_results):
		for i in range(len(self.measurement_scheme)):
			x_exp =[float(j) + self.delta for j in range(len(sim_results.keys()))]
			x_sim =[float(j) - self.delta for j in range(len(sim_results.keys()))]
		return x_exp,x_sim

	def adjust_x_label(self,labels):
		adj_labels = []
		for label in labels:
			if label == 'ctr':
				adj_labels.append('0')
			elif label == 'IL10_.01':
				adj_labels.append('0.01')
			elif label == 'IL10_.1':
				adj_labels.append('0.1')
			elif label == 'IL10_1':
				adj_labels.append('1')
			elif label == 'IL10_10':
				adj_labels.append('10')
			elif label == 'IL10_100':
				adj_labels.append('100')
			elif label == 'TNFa_.1':
				adj_labels.append('0.1')
			elif label == 'TNFa_1':
				adj_labels.append('1')
			elif label == 'TNFa_10':
				adj_labels.append('10')
			elif label == 'IL8_1':
				adj_labels.append('1')
			elif label == 'IL8_10':
				adj_labels.append('10')
			elif label == 'IL8_100':
				adj_labels.append('100')
			elif label == 'IL1b_1':
				adj_labels.append('1')
			elif label == 'IL1b_10':
				adj_labels.append('10')
			elif label == 'IL1b_100':
				adj_labels.append('100')
			else:
				raise ValueError('not defined')
		return adj_labels
class Plot_line:
	"""
	Plots the results of a study by allocting a line graph for each ID and a complete figure for each target
	"""
	def __init__(self,study,observations):
		self.measurement_scheme = observations[study]['measurement_scheme']
		self.colors = ['lime' , 'violet', 'yellowgreen', 'peru', 'skyblue']
		self.study = study
		self.observations = observations 
		if study == 'Qiao_2021_Mg':
			self.graph_size = [5,5]
			self.bar_width = 4
			self.error_bar_width = 2
			self.legend_font_size = 30
			self.tick_font_size = 30
			self.title_font_size = 30
			self.legend_location = [3,1]
			self.yaxis_title = ''
			self.xaxis_title = ''
			self.D = 50 # the length in which all Mg dosages are plotted in a certain time point
			self.delta = 2 # gap between exp and sim
		elif study == 'Ber_2016':
			self.graph_size = [5,5]
			self.bar_width = 10
			self.error_bar_width = 5
			self.legend_font_size = 30
			self.tick_font_size = 30
			self.title_font_size = 30
			self.legend_location = [2.5,1]
			self.yaxis_title = ''
			self.xaxis_title = ''
			self.D = 100 # the length in which all Mg dosages are plotted in a certain time point
			self.delta = 5 # gap between exp and sim
		else:
			raise ValueError('not defined')

	def bar_positions(self,study,IDs,checkpoints):
		IDs_n = len(IDs)
		d = self.D/(IDs_n+1) # the length allocation to a pair of exp-sim
		xs = [] # the location of bars sorted by Mg count
		for i in range(IDs_n):
			x_exp =[(float(j)-self.D/2) + d*(i+1) - self.delta for j in checkpoints]
			x_sim =[(float(j)-self.D/2) + d*(i+1) + self.delta for j in checkpoints]
			xs.append([x_exp,x_sim])
		return xs
	@staticmethod
	def ID_label(ID):
		if ID == 'Mg_.08':
			return '0.08 mM'
		elif ID == 'Mg_.8':
			return '0.8 mM'
		elif ID == 'Mg_8':
			return '8 mM'
		elif ID == 'Mg_5':
			return '5 mM'
		else:
			raise ValueError('invalid entry')
	def plot(self,simulation_results):
		
		##/ sort out based on the targets
		exp_target_results,sim_target_results = self.sort(simulation_results)
		IDs = simulation_results.keys()
		# checkpoints = self.observations[self.study]['measurement_scheme'].values()[0]
		checkpoints = list(self.measurement_scheme.values())[0]
		xs = self.bar_positions(study = self.study, IDs = IDs, checkpoints = checkpoints)

		##/ plot for each target
		target_n = len(self.measurement_scheme)
		fig = plt.figure(figsize=(self.graph_size[0],self.graph_size[1]))
		fig.canvas.draw()
		fig.tight_layout()
		for target,ii in zip(self.measurement_scheme,range(target_n)):
			ax = fig.add_subplot(target_n,1,ii+1)
			mean_exp_sorted = [exp_target_results[target][i]['mean'] for i in range(len(exp_target_results[target]))]
			std_exp_sorted = [exp_target_results[target][i]['std'] for i in range(len(exp_target_results[target]))]

			for jj in range(len(self.observations[self.study]['IDs'])):
				ID = self.observations[self.study]['IDs'][jj]
				ID_lebel = self.ID_label(ID)
				ax.bar(x=xs[jj][0],height=sim_target_results[target][jj],width = self.bar_width, label = "Sim_"+ID_lebel, 
						facecolor = self.colors[jj],
						 edgecolor="black", yerr =  0,
						 error_kw = dict(capsize= self.error_bar_width))
				ax.bar(x=xs[jj][1],height=mean_exp_sorted[jj],width = self.bar_width, label = 'Exp_'+ID_lebel, 
						facecolor = self.colors[jj],hatch=r'\\\\',
						 edgecolor="black", yerr =  std_exp_sorted[jj],
						 error_kw = dict(capsize= self.error_bar_width))
				
			ax.legend(bbox_to_anchor=self.legend_location,loc = 'upper right', borderaxespad=2,prop={ 'family':'Times New Roman','size':self.legend_font_size},ncol=1)
		#     ax.set_ylim(yrange)
			# x_labels = [item.get_text() for item in ax.get_xticklabels()]
			ax.set_xticks(ticks = checkpoints)
			ax.set_xticklabels(checkpoints)
		#     ax.get_yaxis().set_major_formatter(
		#         matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x)/1000, ',')))
			for label in (ax.get_xticklabels() + ax.get_yticklabels()):
				label.set_fontname('Times New Roman')
				label.set_fontsize(self.tick_font_size)
			ax.set_ylabel(self.yaxis_title,fontdict ={'family':'Times New Roman','size':self.title_font_size})
			# ax.set_xlabel('Days',fontdict ={'family':'Times New Roman','size':self.title_font_size})

			ax.set_title(target,fontdict ={'family':'Times New Roman','size':self.title_font_size, 'fontweight':'bold'})
			plt.savefig(self.study+'.svg',bbox_inches='tight')

	def sort(self,sim_results):
		exp_target_results = {}
		for target in self.measurement_scheme:
			exp_target_results[target] = []
		for target in self.measurement_scheme:
			for ID in self.observations[self.study]['IDs']:
				ID_observations = self.observations[self.study][ID]['expectations']
				exp_target_results[target].append(ID_observations[target])
		sim_target_results = {}
		for target in self.measurement_scheme:
			sim_target_results[target] = []
		for target in self.measurement_scheme:
			for ID,ID_result in sim_results.items():
				sim_target_results[target].append(ID_result[target])
		return exp_target_results,sim_target_results

	# def adjust_x_label(self,labels):
	# 	adj_labels = []
	# 	for label in labels:
	# 		if label == 'Mg_.08':
	# 			adj_labels.append('0.08')
	# 		elif label == 'Mg_.8':
	# 			adj_labels.append('0.8')
	# 		elif label == 'Mg_8':
	# 			adj_labels.append('8')
	# 		else:
	# 			raise ValueError('not defined')
	# 	return adj_labels