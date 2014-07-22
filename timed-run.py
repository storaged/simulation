from distselect import distr_init
from selectors import *
from distributions import *
import random
from table_util import table
from environment import Environment
from phenotype import Phenotype
import select
import sys
#import pdb
import code
import plots
import datetime
from distselect import seed_with_default
   
#----------------------------------------------------------------------------------------------------
distr_init()
parameters.load_from_file()
parameters.headless_mode = True
parameters.plotting_frequency = 0

seed_with_default()


print "Start..."
starttime = datetime.datetime.now()

e = Environment()


i = 0
cont = True
while cont: 
    i += 1
    if i >= 100:
	cont = False
    try:
	e.advance_generation()
    except ZeroDivisionError:
	plots.Plot.plot_all(e)
	print "Extinction has occured, generation:", i
	cont = False
    parameters.env_changes(i, e)

endtime = datetime.datetime.now()
print "Done."

print "Elapsed time:", endtime-starttime
