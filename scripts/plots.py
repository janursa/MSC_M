import matplotlib.pyplot as plt
import matplotlib
import copy
plt.rcParams["font.family"] = "serif"
plt.style.use('seaborn-deep')
# plt.style.use('Agg')
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
##/ post processing and plotting //##
def barplot_annotate_brackets(significance, center, height, yerr=None, dh=.05, barh=.02, fs=12, maxasterix=None):
    """ 
    Annotate barplot with p-values.

    :param num1: number of left bar to put bracket over
    :param num2: number of right bar to put bracket over
    :param data: string to write or number for generating asterixes
    :param center: centers of all bars (like plt.bar() input)
    :param height: heights of all bars (like plt.bar() input)
    :param yerr: yerrs of all bars (like plt.bar() input)
    :param dh: height offset over bar / bar + yerr in axes coordinates (0 to 1)
    :param barh: bar height in axes coordinates (0 to 1)
    :param fs: font size
    :param maxasterix: maximum number of asterixes to write (for very small p-values)
    """

    if type(significance) is str:
        text = significance
    else:
        # * is p < 0.05
        # ** is p < 0.005
        # *** is p < 0.0005
        # etc.
        text = ''
        p = .05

        while significance < p:
            text += '*'
            p /= 10.

            if maxasterix and len(text) == maxasterix:
                break

        if len(text) == 0:
            text = 'n. s.'

    lx, rx = center[0], center[1]

    ax_y0, ax_y1 = plt.gca().get_ylim()
    dh *= (ax_y1 - ax_y0)
    barh *= (ax_y1 - ax_y0)

    y = height + dh

    barx = [lx, lx, rx, rx]
    bary = [y, y+barh, y+barh, y]
    mid = ((lx+rx)/2, y+barh)

    plt.plot(barx, bary, c='black')

    kwargs = dict(ha='center', va='bottom')
    if fs is not None:
        kwargs['fontsize'] = fs

    plt.text(*mid, text, **kwargs)
	
def barplot_annotate_stars(significance, center, height, yerr=None, dh=.05, barh=.02, fs=12, maxasterix=None):
    """ 
    Annotate barplot with p-values by putting starts on topc of bars.

    :param num1: number of left bar to put bracket over
    :param num2: number of right bar to put bracket over
    :param data: string to write or number for generating asterixes
    :param center: centers of all bars (like plt.bar() input)
    :param height: heights of all bars (like plt.bar() input)
    :param yerr: yerrs of all bars (like plt.bar() input)
    :param dh: height offset over bar / bar + yerr in axes coordinates (0 to 1)
    :param barh: bar height in axes coordinates (0 to 1)
    :param fs: font size
    :param maxasterix: maximum number of asterixes to write (for very small p-values)
    """

    if type(significance) is str:
        text = significance
    else:
        # * is p < 0.05
        # ** is p < 0.005
        # *** is p < 0.0005
        # etc.
        text = ''
        p = .05

        while significance < p:
            text += '*'
            p /= 10.

            if maxasterix and len(text) == maxasterix:
                break

        if len(text) == 0:
            text = 'n. s.'

    # lx, rx = center[0], center[1]

    # ax_y0, ax_y1 = plt.gca().get_ylim()
    # dh *= (ax_y1 - ax_y0)
    # barh *= (ax_y1 - ax_y0)

    # y = height + dh

    # barx = [lx, lx, rx, rx]
    # bary = [y, y+barh, y+barh, y]
    # mid = ((lx+rx)/2, y+barh)

    # plt.plot(barx, bary, c='black')

    kwargs = dict(ha='center', va='bottom')
    if fs is not None:
        kwargs['fontsize'] = fs
    mid = (center, height)
    plt.text(*mid, text, **kwargs)
	

class Plot_bar:
	"""
	Plots the results of a study by allocting a figure for each target and a bar for each ID
	"""
	def __init__(self,study,observations):
		self.measurement_scheme = observations[study]['measurement_scheme']
		self.study = study
		self.observations = observations
		self.colors = ['lime' , 'violet', 'yellowgreen', 'peru', 'skyblue']

		if study == 'Valles_2020_IL10':
			self.graph_size = [10,10]
			self.bar_width = .2
			self.error_bar_width = .2
			self.colors = ['lime' , 'violet', 'yellowgreen', 'peru', 'skyblue']
			self.legend_font_size = 30
			self.tick_font_size = 30
			self.title_font_size = 30 
			self.delta = .1
		elif study == 'Qiao_2021_IL1b' or study == 'Qiao_2021_IL8':
			self.graph_size = [4,4]
			self.bar_width = .25
			self.error_bar_width = 5
			self.legend_font_size = 20
			self.tick_font_size = 20
			self.title_font_size = 20 
			self.delta = .14
		elif study == 'Qiao_2021_IL8_IL1b':
			self.graph_size = [3,4]
			self.bar_width = .15
			self.error_bar_width = 5
			self.legend_font_size = 20
			self.tick_font_size = 20
			self.title_font_size = 20 
			self.delta = .09
		elif study == 'Chen_2018':
			self.graph_size = [6,8]
			self.bar_width = .3
			self.error_bar_width = 4
			self.legend_font_size = 21
			self.tick_font_size = 21
			self.title_font_size = 21 
			self.delta = .17
		elif study == 'Valles_2020_TNFa':
			self.graph_size = [10,10]
			self.bar_width = .2
			self.error_bar_width = .2
			self.legend_font_size = 30
			self.tick_font_size = 30
			self.title_font_size = 30 
			self.delta = .1
		else:
			raise ValueError('input not defined')
	@staticmethod
	def determine_yrange(study,target):
		if study == 'Qiao_2021_IL8_IL1b':
			yrange_value = [0,65]
		elif study == 'Qiao_2021_IL8' :
			yrange_value = [0,160]
		elif study == 'Qiao_2021_IL1b':
			yrange_value = [0,60]
		elif study == 'Qiao_2021_Mg':
			yrange_value = [0,27]
		elif study == 'Chen_2018' and target=='ALP':
			yrange_value = [0,7]
		elif study == 'Chen_2018' and target=='ARS':
			yrange_value = [0,5.5]
		elif study == 'Valles_2020_TNFa' and target=='ALP':
			yrange_value = [0,7]
		elif study == 'Valles_2020_TNFa' and target=='ARS':
			yrange_value = [0,5.5]
		elif study == 'Valles_2020_IL10' and target=='ALP':
			yrange_value = [0,7]
		elif study == 'Valles_2020_IL10' and target=='ARS':
			yrange_value = [0,5.5]

		return yrange_value
	@staticmethod
	def determine_xrange(study,target):
		if study == 'Qiao_2021_IL8_IL1b' and target == 'ALP':
			yrange_value = [-.3,1.3]
		elif study == 'Qiao_2021_IL8' or study == 'Qiao_2021_IL1b':
			raise ValueError('not needed')
		return yrange_value

	@staticmethod
	def p_values_positions(study,target,xx):
		if study == 'Qiao_2021_IL8_IL1b':
			Xs = xx
			Ys = 50
		elif study == 'Qiao_2021_IL8':
			Xs = [[xx[0],xx[2]],[xx[0],xx[3]]]
			Ys = [70,130]
		elif study == 'Qiao_2021_IL1b':
			Xs = [xx[0],xx[2]]
			Ys = 50
		elif study == 'Qiao_2021_Mg':
			Xs = [[[xx[0][0],xx[1][0]],[xx[0][0],xx[2][0]]],[[xx[0][1],xx[1][1]],[xx[0][1],xx[2][1]]]]
			Ys = [[11,17],[18,23]]
		elif study == 'Chen_2018' and target == 'ALP':
			Xs = [xx[2]+.15,xx[3]+.15, xx[4]+.15, xx[5]+.15,xx[6]+.15]
			Ys = [3,6,4.7,1.6,1.7]
		elif study == 'Chen_2018' and target == 'ARS':
			Xs = [xx[2]+.15,xx[3]+.15, xx[4]+.15, xx[5]+.15,xx[6]+.15]
			Ys = [2.1,4.6,3.5,.7,.7]
		elif study == 'Valles_2020_TNFa' and target == 'ALP':
			Xs = []
			Ys = []
		elif study == 'Valles_2020_TNFa' and target == 'ARS':
			Xs = []
			Ys = []
		elif study == 'Valles_2020_IL10' and target == 'ALP':
			Xs = []
			Ys = []
		elif study == 'Valles_2020_IL10' and target == 'ARS':
			Xs = []
			Ys = []
		return Xs,Ys
	@staticmethod
	def draw_p_values(ax,study,target,Xs,Ys):
		if study == 'Qiao_2021_IL8_IL1b':
			X,Y = Xs,Ys
			barplot_annotate_brackets(significance=0.001,center=Xs,height=Ys)
		elif study == 'Qiao_2021_IL8':
			significance_list = [0.001,0.001]
			for i in range(len(significance_list)):
				barplot_annotate_brackets(significance=significance_list[i],
					center=Xs[i],height=Ys[i])
		elif study == 'Qiao_2021_IL1b':
			X,Y = Xs,Ys
			significance = 0.01 
			barplot_annotate_brackets(significance=significance,
				center=X,height=Y)
		elif study == 'Qiao_2021_Mg':
			significance_list = [[0.01,0.01],[0.01,0.001]]
			for group_i in range(2):
				for i in range(len(significance_list[group_i])):
					barplot_annotate_brackets(significance=significance_list[group_i][i],
						center=Xs[group_i][i],height=Ys[group_i][i])
		elif study == 'Chen_2018' and target == 'ALP':
			significance_list = [0.01,0.01,0.01,0.01,0.01]
			for i in range(len(significance_list)):
				barplot_annotate_stars(significance=significance_list[i],
					center=Xs[i],height=Ys[i])
		elif study == 'Chen_2018' and target == 'ARS':
			significance_list = [0.01,0.01,0.01,0.01,0.01]
			for i in range(len(significance_list)):
				barplot_annotate_stars(significance=significance_list[i],
					center=Xs[i],height=Ys[i])
		
	@staticmethod
	def determine_ylabel(study,target):
		label = ''
		unit_value = ''
		if study == 'Qiao_2021_IL8_IL1b' or study == 'Qiao_2021_IL8' or study == 'Qiao_2021_IL1b' or study == 'Qiao_2021_Mg':
			unit_value = '\n (nmol/min/mg.protein)'
		elif study == 'Chen_2018':
			unit_value = '\n (Relative fold)'
		label = target+unit_value
		return label
	@staticmethod
	def determine_xlabel(study,target):
		label = ''
		if study == 'Qiao_2021_IL8_IL1b':
			pass
		elif study == 'Qiao_2021_IL8':
			label = 'IL-8 (ng/ml)'
		elif study == 'Qiao_2021_IL1b':
			label = 'IL-1$\\beta$ (ng/ml)'
		elif study == 'Qiao_2021_Mg':
			label = 'Days'
		elif study == 'Chen_2018' and target == 'ARS':
			label = 'IL-10 (ng/ml)'
		elif study == 'Chen_2018' and target == 'ALP':
			pass
		return label
	

	def plot(self,simulation_results):
		##/ sort out based on the measurement_scheme
		IDs = list(simulation_results.keys())
		x_labels = self.adjust_x_label(IDs)
		exp_target_results,sim_target_results = self.sort(simulation_results)
		x_exp,x_sim,base_x = self.bar_positions(simulation_results)

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
			exp_std = [exp_target_results[target][i]['std'] for i in range(len(exp_target_results[target]))]
			exp_values = [item[0] for item in exp_values]
			exp_std = [item[0] for item in exp_std]
			ax.bar(x=x_exp,height=exp_values,width = self.bar_width, label = 'Exp', 
					facecolor = self.colors[1],hatch=r'\\\\',
					 edgecolor="black", yerr =  exp_std,
					 error_kw = dict(capsize= self.error_bar_width))
			
			# ax.legend(bbox_to_anchor=(2, 1),loc = 'upper right', borderaxespad=2,prop={ 'family':'Times New Roman','size':self.legend_font_size},ncol=1)
			# ax.set_xlim([-.3,1.3])
			# x_labels = [item.get_text() for item in ax.get_xticklabels()]
			x_ticks = [(i+j)/2 for i,j in zip(x_sim,x_exp)]
			x_ticks_adj,x_labels_adj = self.add_adjustements(ax=ax,study=self.study,target=target,base_x=base_x,x_ticks=x_ticks,x_labels=x_labels)
		#     ax.get_yaxis().set_major_formatter(
		#         matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x)/1000, ',')))
			self.finalize_and_save(ax=ax,target=target,exp_xx=x_ticks_adj,x_ticks=x_ticks_adj,x_labels=x_labels_adj)
	def add_adjustements(self,ax,study,target,base_x,x_ticks,x_labels):
		x_ticks_adj = copy.deepcopy(x_ticks)
		x_labels_adj = copy.deepcopy(x_labels)
		if study == 'Chen_2018':
			x_ticks_adj.insert(0,base_x)
			x_labels_adj.insert(0,'ctr')
			if target == 'ALP':
				ax.bar(x=base_x,height=1,width = self.bar_width, label = 'Exp', 
					facecolor = self.colors[1],hatch=r'\\\\',
					 edgecolor="black", yerr =  0,
					 error_kw = dict(capsize= self.error_bar_width))
			elif target == 'ARS':
				ax.bar(x=base_x,height=0.1,width = self.bar_width, label = 'Exp', 
					facecolor = self.colors[1],hatch=r'\\\\',
					 edgecolor="black", yerr =  0,
					 error_kw = dict(capsize= self.error_bar_width))
		return x_ticks_adj,x_labels_adj
	def finalize_and_save(self,ax,target,x_ticks,x_labels,exp_xx):
		ax.set_ylim(self.determine_yrange(target = target, study = self.study))
		try:
			ax.set_xlim(self.determine_xrange(target = target, study = self.study))
		except:
			pass
		ax.set_xticks(ticks = x_ticks)
		ax.set_xticklabels(x_labels)
		for label in (ax.get_xticklabels() + ax.get_yticklabels()):
			label.set_fontname('Times New Roman')
			label.set_fontsize(self.tick_font_size)
		# unit_value = Plot_bar.unit(study = self.study,target=target)
		ax.set_ylabel(Plot_bar.determine_ylabel(study=self.study,target = target),fontdict ={'family':'Times New Roman','size':self.title_font_size})
		ax.set_xlabel(Plot_bar.determine_xlabel(study=self.study,target = target),fontdict ={'family':'Times New Roman','size':self.title_font_size})

		# ax.set_title(target,fontdict ={'family':'Times New Roman','size':self.title_font_size, 'fontweight':'bold'})
		Xs,Ys = Plot_bar.p_values_positions(study=self.study,target=target,xx = exp_xx)	
		Plot_bar.draw_p_values(ax,study=self.study,target=target,Xs=Xs,Ys=Ys)
		if self.study == 'Qiao_2021_Mg':
			ax.get_xaxis().set_major_formatter(
				matplotlib.ticker.FuncFormatter(lambda x, p: format(int(int(x)/24), ',')))
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
		base = None
		if self.study == 'Chen_2018':
			base = -0.9

		return x_exp,x_sim,base

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
			elif label == 'IL1b_IL8':
				adj_labels.append('IL-8 + IL-1$\\beta$')
			else:
				raise ValueError('not defined')
		return adj_labels


class Plot_bar_2(Plot_bar):
	"""
	This one has more days (time points). Previous one had only the final time points
	"""
	def __init__(self,study,observations):
		try:
			super().__init__(study=study,observations=observations)
		except ValueError:
			pass

		if study == 'Qiao_2021_Mg':
			self.graph_size = [5,4]
			self.bar_width = 8
			self.error_bar_width = 3
			self.legend_font_size = 20
			self.tick_font_size = 20
			self.title_font_size = 20
			self.legend_location = [3,1]
			self.yaxis_title = ''
			self.xaxis_title = ''
			self.D = 85 # the length in which all Mg dosages are plotted in a certain time point
			self.delta = 5 # gap between exp and sim
		elif study == 'Ber_2016':
			self.graph_size = [5,5]
			self.bar_width = 10
			self.error_bar_width = 5
			self.legend_font_size = 20
			self.tick_font_size = 20
			self.title_font_size = 20
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

			exp_xx = [xs[jj][1] for jj in range(len(self.observations[self.study]['IDs']))]
			# ax.legend(bbox_to_anchor=(2, 1),loc = 'upper right', borderaxespad=0.,prop={ 'family':'Times New Roman','size':self.legend_font_size},ncol=1)

			self.finalize_and_save(ax=ax, target=target,x_ticks=checkpoints,x_labels=checkpoints,exp_xx=exp_xx)

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

	