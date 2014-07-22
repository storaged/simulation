from distselect import distr_init, save_run
import distributions
import random
from table_util import table
import select
import sys
#import pdb
import code
#import parameters
import signals
   
#----------------------------------------------------------------------------------------------------

import model_init

pfile = 'parameters.py'
if len(sys.argv) > 1:
    pfile = sys.argv[1]

model_init.model_init(pfile, 'output', False, 0)

e = model_init.Runinfo.environment

from saveableparams import parameters

i=0
cont = True
while cont: 
    i += 1
    try:
	e.advance_generation()
    except ZeroDivisionError:
        print "Extinction has occured."
	plots.Plot.plot_all(e)
	cont = False
	code.interact(local=locals())
#    if i % 25 == 0:
#	e.history.plot()
    parameters.env_changes(i, e)
    file, _, _ = select.select([sys.stdin], [], [], 0)
    if len(file) > 0:
	code.interact(local=locals())
    signals.save_if_requested()
