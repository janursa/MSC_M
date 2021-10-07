from fuzzy_cpp import Fuzzy_TNFa
from pympler import muppy,tracker


params = {
	'a':2
}

def func():
	obj = Fuzzy_TNFa(params)
	oo = obj.forward({'TNFa':0})
	print(oo)

if __name__ == '__main__':
    tr = tracker.SummaryTracker() # to show the initial list of objects
    for i in range(100000):
        func()
        if i%500==0: # we monitor different in the list of objects every 500 iterations
            print('Iteration ',i)
            tr.print_diff() #
