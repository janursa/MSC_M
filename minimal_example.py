from skfuzzy import control as ctrl
from pympler import muppy,tracker
import skfuzzy as fuzz
import numpy as np
import sys


class TestClass:
	def __init__(self):
		self.var =np.arange(0,1000,.01)
	def fun1(self):
		a = np.arange(0,1000,.01)



def fuc():
	range_value = np.arange(0, 1, .01)
	consequent = ctrl.Consequent(range_value, 'consequent')
	consequent['L']=fuzz.gaussmf(range_value, .5, .05)

	antecedent = ctrl.Antecedent(range_value, 'antecedent')
	antecedent['M']=fuzz.gaussmf(range_value, .5, .05)
	rule1 = ctrl.Rule(antecedent['M'] , consequent['L'])

	# aa = [attr for attr in dir(rule1.antecedent) if not attr.startswith("__")]
	# attrs = ['cuts', 'full_label', 'label', 'membership_value', 'mf', 'parent', 'view']
	attrs = ['membership_value']
	[getattr(rule1.antecedent, attr) for attr in attrs if not attr.startswith("__")]
	# print(aa)
	# sys.exit(2)
	# obj = TestClass()
	# aa= [getattr(obj, attr) for attr in dir(obj) if not attr.startswith("__")]
	# print(aa)


if __name__ == '__main__':
    tr = tracker.SummaryTracker()
    for i in range(100000):
        fuc()
        if i%500==0:
            print('Iteration ',i)
            tr.print_diff() 