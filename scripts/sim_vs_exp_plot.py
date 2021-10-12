import sys
import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')
sys.path.insert(0,dir_to_dirs)
from dirs import dir_to_MSC_osteogenesis
sys.path.insert(0,dir_to_MSC_osteogenesis)
from MSC_osteogenesis import *
from plots import *
from observations import observations
if __name__ == '__main__':
	##/ run test simultions and plot

	with open('inferred_params.json') as file:
		inferred_params = json.load(file)
	# inferred_params['a_Valles_2020_ARS'] = 1
	# inferred_params['ALP_M_n'] = 5
	# inferred_params['a_Qiao_2021_IL1b_ALP'] = 60
	# inferred_params['diff_time'] = 800


	obj = MSC_model(free_params = inferred_params,debug=True)
	simulation_results = obj.simulate_studies()
	print(simulation_results)
	# study = 'Qiao_2021_Mg'
	# study = 'Qiao_2021_Mg'

	for study in observations['studies']:
		if study == 'Qiao_2021_Mg' or study == 'Ber_2016':
			plot_obj = Plot_line(study,observations)
		else:
			plot_obj = Plot_bar(study,observations)
		plot_obj.plot(simulation_results[study])
