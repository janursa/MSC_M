import sys

sys.path.insert(0,'/Users/matin/Downloads/testProjs/MSC_M/fuzzy_cpp/build/binds')
from fuzzy_cpp import *
sys.path.insert(0,'/Users/matin/Downloads/testProjs/MSC_M/')
from MSC_osteogenesis import all_params

def Fuzzy_Mg_test():
	print('\\** Evaluation of Mg **\\')
	ctr = Fuzzy_Mg(all_params)
	oo = ctr.forward({'Mg':0})
	assert oo['early_diff'] < 0.5, 'Checkpoint 11' 
	assert oo['late_diff'] == 0.5, 'Checkpoint 21' 
	oo = ctr.forward({'Mg':0.8})
	assert oo['early_diff'] == 0.5, 'Checkpoint 21' 
	oo = ctr.forward({'Mg':5})
	assert oo['early_diff'] > 0.5, 'Checkpoint 31' 
	oo = ctr.forward({'Mg':17.5})
	assert oo['early_diff'] == 0.5, 'Checkpoint 41' 
	oo = ctr.forward({'Mg':60})
	assert oo['early_diff'] < 0.5, 'Checkpoint 41' 
	oo = ctr.forward({'Mg':25}) # any value over 1.8 mM
	assert oo['late_diff'] < 0.5, 'Checkpoint 51' 
	print('\\** PASSED **\\')

def Fuzzy_TNFa_test():
	print('\\** Evaluation of TNFa **\\')
	ctr = Fuzzy_TNFa(all_params)
	oo = ctr.forward({'TNFa':0})
	assert oo['early_diff'] == 0.5, 'Checkpoint 11' 
	assert oo['late_diff'] == 0.5, 'Checkpoint 12' 
	oo = ctr.forward({'TNFa':10}) # high
	assert oo['early_diff'] == 0.5, 'Checkpoint 21' 
	assert oo['late_diff'] == 0.5, 'Checkpoint 22' 
	oo = ctr.forward({'TNFa':1}) # stim
	assert oo['early_diff'] >= .5, 'Checkpoint 31' 
	assert oo['late_diff'] >= .5, 'Checkpoint 32' 
	assert oo['early_diff'] <= 1, 'Checkpoint 41'
	assert oo['late_diff'] <= 1, 'Checkpoint 42' 
	oo = ctr.forward({'TNFa':100}) # inhib
	assert oo['early_diff'] <= .5, 'Checkpoint 51'
	assert oo['late_diff'] <= .5, 'Checkpoint 52' 
	print('\\** PASSED **\\')
def Fuzzy_IL10_test():
	print('\\** Evaluation of IL10 **\\')
	print('\\** Evaluation of above 48 **\\')
	ctr = Fuzzy_IL10(all_params,True)
	oo = ctr.forward({'IL10':0})
	assert oo['early_diff'] == 0.5, 'Checkpoint 11' 
	assert oo['late_diff'] == 0.5, 'Checkpoint 12' 
	oo = ctr.forward({'IL10':0.1}) # high
	assert oo['early_diff'] > 0.5, 'Checkpoint 21' 
	assert oo['late_diff'] > 0.5, 'Checkpoint 22' 
	oo = ctr.forward({'IL10':1}) # stim
	assert oo['early_diff'] > .5, 'Checkpoint 31' 
	assert oo['late_diff'] > .5, 'Checkpoint 32' 
	assert oo['early_diff'] < 1, 'Checkpoint 41'
	assert oo['late_diff'] == 1, 'Checkpoint 42' 
	
	oo = ctr.forward({'IL10':10}) # inhib
	assert oo['early_diff'] < .5, 'Checkpoint 51'
	assert oo['late_diff'] < .5, 'Checkpoint 52' 
	print('\\** PASSED: Evaluation of above 48 **\\')

	print('\\** Evaluation of below 48 **\\')
	ctr = Fuzzy_IL10(all_params,False)
	oo = ctr.forward({'IL10':0})
	assert oo['early_diff'] == 0.5, 'Checkpoint 11' 
	assert oo['late_diff'] == 0.5, 'Checkpoint 12' 
	oo = ctr.forward({'IL10':1}) # high
	assert oo['early_diff'] > 0.5, 'Checkpoint 21' 
	assert oo['late_diff'] > 0.5, 'Checkpoint 22' 
	oo = ctr.forward({'IL10':10}) # stim
	assert oo['early_diff'] > .5, 'Checkpoint 31' 
	assert oo['late_diff'] > .5, 'Checkpoint 32' 
	assert oo['early_diff'] < 1, 'Checkpoint 41'
	assert oo['late_diff'] == 1, 'Checkpoint 42' 
	
	oo = ctr.forward({'IL10':100}) # inhib
	assert oo['early_diff'] < .5, 'Checkpoint 51'
	assert oo['late_diff'] < .5, 'Checkpoint 52' 
	print('\\** PASSED **\\')
def Fuzzy_IL8_IL1b_test():
	print('\\** Evaluation of IL8 **\\')
	ctr = Fuzzy_IL8_IL1b(all_params)
	oo = ctr.forward({'IL8':0})
	assert oo['early_diff'] == 0.5, 'Checkpoint 11' 
	oo = ctr.forward({'IL8':25}) # high
	assert oo['early_diff'] > 0.5, 'Checkpoint 21' 
	assert oo['early_diff'] < 1, 'Checkpoint 22' 
	oo = ctr.forward({'IL8':100}) # stim
	assert oo['early_diff'] == 1, 'Checkpoint 31' 
	oo = ctr.forward({'IL8':40}) # random
	assert oo['early_diff'] > 0.5, 'Checkpoint 41'
	assert oo['early_diff'] < 1, 'Checkpoint 42' 
	print('\\** PASSED **\\')


if __name__ == '__main__':
	Fuzzy_TNFa_test()
	Fuzzy_IL10_test()
	Fuzzy_IL8_IL1b_test()
	Fuzzy_Mg_test()
