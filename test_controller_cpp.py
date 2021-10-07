sys.path.insert(0,'/Users/matin/Downloads/testProjs/MSC_M/fuzzy_cpp/build/binds')
from fuzzy_cpp import *
import sys
sys.path.insert(0,'/Users/matin/Downloads/testProjs/MSC_M/')
from MSC_osteogenesis import all_params

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
	print('\\** PASSED: evaluation of TNFa **\\')


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
	print('\\** PASSED: Evaluation of below 48 **\\')

def Fuzzy_IL8_IL1b_test():
	print('\\** Evaluation of IL8 **\\')
	ctr = Fuzzy_IL8_IL1b(all_params)
	oo = ctr.forward({'IL8':0})
	assert oo['early_diff'] == 0.5, 'Checkpoint 11' 
	assert oo['late_diff'] == 0.5, 'Checkpoint 12' 
	oo = ctr.forward({'IL8':25}) # high
	assert oo['early_diff'] > 0.5, 'Checkpoint 21' 
	assert oo['early_diff'] < 1, 'Checkpoint 21' 
	assert oo['late_diff'] > 0.5, 'Checkpoint 21' 
	assert oo['late_diff'] < 1, 'Checkpoint 21'  
	oo = ctr.forward({'IL8':100}) # stim
	assert oo['early_diff'] > 0.5, 'Checkpoint 21' 
	assert oo['early_diff'] < 1, 'Checkpoint 21' 
	assert oo['late_diff'] > 0.5, 'Checkpoint 21' 
	assert oo['late_diff'] < 1, 'Checkpoint 21'
	print('\\** PASSED: evaluation of IL8 **\\')


if __name__ == '__main__':
	Fuzzy_TNFa_test()
	Fuzzy_IL10_test()
	Fuzzy_IL8_IL1b_test()
