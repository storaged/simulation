import select
import sys
import code
import os
from saveableparams import Parameters
parameters = Parameters()

'''
pnames = None
if len(sys.argv)>2:
    pnames = parameters.load_batch_mode(int(sys.argv[2]), sys.argv[1])
else:
    batch_run_no = int(os.path.normpath(sys.argv[1]).split('-')[-1])
    pnames = parameters.load_batch_mode(batch_run_no, os.path.join(sys.argv[1], 'parameters.py'))


for name in pnames:
    if not parameters.__dict__[name].__class__.__name__ in ['function', 'module', 'ReproducerDefault'] and not name in ['draw_legends', 'headless_mode', 'plotting_frequency', 'heatmaps_enabled', 'tmpdir']:
	print name, " 	= ", parameters.__dict__[name]
'''

def extract_params_str(param_filepath, batch_no):
    parameters = Parameters()

    pnames = parameters.load_batch_mode(batch_no, param_filepath)

#    lines = []

#    for name in pnames:
#        if not parameters.__dict__[name].__class__.__name__ in ['function', 'module', 'ReproducerDefault'] and not name in ['draw_legends', 'headless_mode', 'plotting_frequency', 'heatmaps_enabled']:
#	    lines.append(name + "   = " +  str(parameters.__dict__[name]))

    return str(parameters)


def extract_params_in_dir(dirname):
    batch_run_no = int(os.path.normpath(dirname).split('-')[-1])
    param_path = os.path.join(dirname, 'parameters.py')
    with open(os.path.join(dirname, 'params.txt'), 'w') as f:
	f.write(extract_params_str(param_path, batch_run_no))

if len(sys.argv)==2:
    extract_params_in_dir(sys.argv[1])
else:
    import glob
    for dirn in glob.glob("batch-run-*"):
        try:
	    extract_params_in_dir(dirn)
	except OSError:
	    pass
    

