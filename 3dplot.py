import multiprocessing
import time
import sys
import os
from lib import simulate

def simwork(corr):
    return simulate(corr, "parameters-3d.py", 5000)

pool = multiprocessing.Pool(5)


par1name = 'expected_mutation_shift'
par1 = [x*0.0002 for x in range(0, 100)]
#[0.0, 0.0001, 0.0002, 0.0003, 0.0005, 0.001, 0.002, 0.003, 0.0005, 0.001, 0.002, 0.003, 0.005, 0.01, 0.011, 0.012, 0.013, 0.014, 0.015, 0.016, 0.017]

corrections = []

for p in par1:
    d = {}
    d[par1name] = p
    corrections.append(d)




res = pool.map(simwork, corrections)

import cPickle

ofile = open("results.table", "w")

for penv in res:
    env = cPickle.loads(penv)
    print
    print
    for i in xrange(0, 5001, 100):
	try:
	    ofile.write(str(env.history.t.datarows[i][env.history.t.get_colnr_by_id("avg inactive transp")]) + " ")
	except IndexError:
	    ofile.write("NaN ")
    ofile.write('\n')


ofile.flush()
ofile.close()
	#print env.average_funct(lambda p: p.inactive_transposons)


