import sys
import pathlib
import os
current_file = pathlib.Path(__file__).parent.absolute()
dir_to_dirs = os.path.join(current_file,'..')
sys.path.insert(0,dir_to_dirs)
from dirs import dir_to_MSC_osteogenesis
sys.path.insert(0,dir_to_MSC_osteogenesis)
from MSC_osteogenesis import *
from plots import *
import parameters

if __name__ == '__main__':
	##/ run test simultions and plot
	results_folder = os.path.join(dir_to_dirs,'results','Qiao_IL8_IL1b')
	with open(os.path.join(results_folder,'inferred_params_0_400.json')) as file:
		inferred_params = json.load(file)
	# inferred_params['a_late_diff_inhib'] = 10
	obs,_ = parameters.specifications('Qiao_IL8_IL1b')

	obj = MSC_model(fixed_params=parameters.fixed_params,free_params = inferred_params,observations=obs, debug=True)
	simulation_results = obj.simulate_studies()
	# print(simulation_results)
	error = obj.run()
	print('Error is ',error)



	for study in obs['studies']:
		if study == 'Qiao_2021_Mg' or study == 'Ber_2016':
			plot_obj = Plot_bar_2(study,obs)
		else:
			plot_obj = Plot_bar(study,obs)
		plot_obj.plot(simulation_results[study])
