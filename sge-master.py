import subprocess
import time
import sys
import os
import shutil
import random
import signals
import stat
from count_params import count_params

signals.setup_ignore()

instances_init = count_params()


def check_dir(instance_no):
    dirname = "batch-run-"+str(instance_no)
    if not os.path.exists(dirname):
	return False
    appends = ["batchinfo",  "initial",  "parameters.py",  "plot-1.png",  "plot-2.png",  "plot-3.png", "plot-4.png"]
    for a in appends:
	if not os.path.exists(os.path.join(dirname, a)):
	    shutil.rmtree(dirname, True)
	    return False
    return True

instances = []

for inst in xrange(instances_init):
    if not check_dir(inst):
	instances.append(inst)

random.shuffle(instances)

from saveableparams import Parameters

run_nos = {}

def get_param_run_no(instance_no):
    try:
	return run_nos[instance_no]
    except KeyError:
	p = Parameters()
	p.load_batch_mode(instance_no, 'parameters.py')
	run_nos[instance_no] = p.run_no
	return p.run_no


inst_k = [(val, get_param_run_no(val)) for val in instances]

inst_k_sorted = sorted(inst_k, key = lambda x: x[1])

instances = [v[0] for v in inst_k_sorted]



def writescript(nr):
    with open("run-sim-"+str(i)+".sh", "w") as f:
	f.write("#!/bin/bash\n")
	f.write("hostname\n")
	f.write('date\n')
	f.write("for C in python /home/transp/pypy-2.2.1-linux64/bin/pypy pypy pypy-c2.0 pypy-c1.9 pypy /home/transp/pypy-1.9/bin/pypy /home/mist-sim/pypy-1.9/bin/pypy pypy-c1.8 /home/mist-sim/pypy-1.8/bin/pypy python2.7 python\n")
	f.write("do\n")
	f.write("	if command -v $C\n")
	f.write("	then\n")
	f.write("		echo Interpreter: $C\n")
	f.write("		$C batchrun.py " + str(i) + "\n")
	f.write("		break\n")
	f.write("	fi\n")
#	f.write("python batchrun.py " + str(i) + "\n")
	f.write("done\n")
	f.write("cd batch-run-" + str(nr) + '\n')
	f.write("R -q --no-save --vanilla -f ../makeplot.R\n")
	f.write('date\n')
	
    


commands = []
for i in instances:
    writescript(i)
    try:
	os.unlink("output-" + str(i))
    except OSError:
	pass
#    commands.append("qsub -cwd -sync y -q sim -j y -l pamiec_virt=4G -o output-" + str(i) + " run-sim-" + str(i) + ".sh")
    commands.append("qsub -p -100 -S /bin/bash -cwd -q sim -j y -o output-" + str(i) + " run-sim-" + str(i) + ".sh")
#    os.system("qsub -S /bin/bash -cwd -q sim -j y -o output-" + str(i) + " run-sim-" + str(i) + ".sh")
import debug
debug.g(len(commands))

with open("stop-this.sh", 'w') as f:
    f.write('#!/bin/bash\n')
    os.chmod("stop-this.sh", stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH | stat.S_IXGRP | stat.S_IXOTH)
    for command in commands:
	o = subprocess.check_output(command, shell=True)
	print o,
	nr = int(o.split()[2])
	f.write('qdel ' + str(nr) + '\n')



