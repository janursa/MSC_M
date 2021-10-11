from skfuzzy import control as ctrl
from pympler import muppy,tracker
import skfuzzy as fuzz
import numpy as np
import sys
from MSC_osteogenesis import *

def fuc():

	[getattr(MSC_model, attr) for attr in dir(MSC_model) if not attr.startswith("__")]
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