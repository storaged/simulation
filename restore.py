import sys
import lib

lib.run_model(paramfile = 'batch-run-%s/parameters.py' % sys.argv[1], outdir = 'batch-run-%s' % sys.argv[1], batch = True, batch_run_no = int(sys.argv[1]), interactive = False, seed_file = 'batch-run-%s/initial' % sys.argv[1])


