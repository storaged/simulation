import sys
import lib
import cProfile

cProfile.run('''lib.run_model(paramfile = 'parameters.py', outdir = 'batch-run-%s' % sys.argv[1], batch = True, batch_run_no = int(sys.argv[1]), interactive = False, default_random=True)''')


