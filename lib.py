from table_util import table
import select
import sys
#import pdb
import code
#import parameters
import signals
#----------------------------------------------------------------------------------------------------

def run_model(paramfile = 'parameters.py', outdir = 'out', batch = False, batch_run_no = 0, default_random = False, interactive = False, seed_file = None):


    import model_init


    model_init.model_init(paramfile, outdir, batch, batch_run_no, default_random = default_random, seed_file = seed_file)

    e = model_init.Runinfo.environment
    from saveableparams import parameters

    i = 0
    cont = True
    while cont: 
	i += 1
	try:
	    e.advance_generation()
	    if not parameters.plots_enabled:
		print "Still alive, generation " + str(e.generation)

	except ZeroDivisionError:
	    print "Extinction has occured."
	    cont = False
	parameters.env_changes(i, e)
	if interactive:
	    file, _, _ = select.select([sys.stdin], [], [], 0)
	    if len(file) > 0:
		code.interact(local=locals())
	signals.save_if_requested()

	if parameters.generations <= i:
	    cont = False
