import sys
import lib

lib.run_model(paramfile = 'parameters.py', outdir = 'batch-run-%s' % sys.argv[1], batch = True, batch_run_no = int(sys.argv[1]), interactive = False)


