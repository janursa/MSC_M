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
from observations import observations
if __name__ == '__main__':
	##/ run test simultions and plot

	with open('inferred_params.json') as file:
		inferred_params = json.load(file)
	# inferred_params['maturity_t'] = .7

	obj = MSC_model(fixed_params=fixed_params,free_params = inferred_params,debug=True)
	simulation_results = obj.simulate_studies()
	# print(simulation_results)
	error = obj.run()
	print('Error is ',error)



	for study in observations['studies']:
		if study == 'Qiao_2021_Mg' or study == 'Ber_2016':
			plot_obj = Plot_line(study,observations)
		else:
			plot_obj = Plot_bar(study,observations)
		plot_obj.plot(simulation_results[study])
