
from skfuzzy import control as ctrl
from pympler import muppy,tracker
import skfuzzy as fuzz
import numpy as np
import sys

def base_example():
	quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
	service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
	tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')
	quality.automf(3)
	service.automf(3)
	tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
	tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
	tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])
	rule1 = ctrl.Rule(quality['poor'] | service['poor'], tip['low'])
	rule2 = ctrl.Rule(service['average'], tip['medium'])
	rule3 = ctrl.Rule(service['good'] | quality['good'], tip['high'])
	tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
	tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
	tipping.input['quality'] = 6.5
	tipping.input['service'] = 9.8
	tipping.compute()
if __name__ == '__main__':
    tr = tracker.SummaryTracker() # to show the initial list of objects
    for i in range(100000):
        base_example()
        if i%500==0: # we monitor different in the list of objects every 500 iterations
            print('Iteration ',i)
            tr.print_diff() # to show the difference beween this iteration and the base one