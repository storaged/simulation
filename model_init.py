import os
from distselect import distr_init, save_run
from saveableparams import Parameters
import atexit

class Runinfo:
    pass



def model_init(paramfile = "parameters.py", outdir = "output", in_batch = False, batch_no = 0, default_random = False, seed_file = None):
    Runinfo.param_file_path = paramfile
    Runinfo.out_dir_path = outdir
    Runinfo.in_batch = in_batch
    Runinfo.batch_no = batch_no


    with open(paramfile, 'r') as params_file:
	Runinfo.params_file_text = params_file.read()

    try:
        if outdir != None:
	    os.mkdir(Runinfo.out_dir_path)
    except OSError:
	pass

    if outdir != None:
	with open(os.path.join(outdir, 'parameters.py'), 'w') as params_out_file:
	    params_out_file.write(Runinfo.params_file_text)

    distr_init(seed_file, fast = default_random)
    if outdir != None:
	save_run(os.path.join(outdir, 'initial'))
	
	import cPickle as pickle
	import platform
	import subprocess
	import sys

	d = {
	'argv[0]':		sys.argv[0],
	'argv':			' '.join(sys.argv),
	'cwd':			os.getcwd(),
	'hostname':		platform.node(),
	'version':		platform.python_version(),
	'implementation':	platform.python_implementation(),
	'svnversion':		'NONE', #subprocess.check_output('svnversion .', shell=True)
	}
	with open(os.path.join(outdir, 'info'), 'w') as f:
	    pickle.dump(d, f)
	import pprint
	pprint.pprint(d)
	
	

    Parameters()
    print Parameters.default
    import saveableparams
    saveableparams.parameters = Parameters.default

    if in_batch:
	Parameters.default.load_batch_mode(batch_no, paramfile)
    else:
	Parameters.default.load_from_file(paramfile)

    print str(saveableparams.parameters)

    from environment import Environment
    Runinfo.environment = Environment()

    import signals
    signals.setup()

    import listeners

    if outdir != None:
	listeners.setup_listeners()

    def save_params_for_viewer():
	with open(os.path.join(outdir, 'params.txt'), 'w') as f:
	    f.write(saveableparams.parameters.initstr)

    if outdir != None:
	atexit.register(save_params_for_viewer)
