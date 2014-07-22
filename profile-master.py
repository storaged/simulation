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
    appends = ["batchinfo",  "initial",  "parameters.py",  "plot-1.png",  "plot-2.png",  "plot-3.png"]
    for a in appends:
	if not os.path.exists(os.path.join(dirname, a)):
	    shutil.rmtree(dirname, True)
	    return False
    return True

instances = []

for inst in xrange(instances_init):
    if not check_dir(inst):
	instances.append(inst)




def writescript(nr):
    with open("run-sim-"+str(i)+".sh", "w") as f:
	f.write("#!/bin/bash\n")
	f.write("hostname\n")
	f.write('date\n')
	f.write("if [ -f /home/mist-sim/pypy-1.8/bin/pypy ]\n")
	f.write("then\n")
	f.write("	/home/mist-sim/pypy-1.8/bin/pypy batchrun-profile.py " + str(i) + "\n")
	f.write("else\n")
	f.write("       pypy-c1.8 batchrun-profile.py " + str(i) + "\n")
#	f.write("python batchrun.py " + str(i) + "\n")
	f.write("fi\n")
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
    commands.append("qsub -S /bin/bash -l profile_slots=1 -cwd -q sim -j y -o output-" + str(i) + " run-sim-" + str(i) + ".sh")

with open("stop-this.sh", 'w') as f:
    f.write('#!/bin/bash\n')
    os.chmod("stop-this.sh", stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH | stat.S_IXGRP | stat.S_IXOTH)
    for command in commands:
	o = subprocess.check_output(command, shell=True)
	print o,
	nr = int(o.split()[2])
	f.write('qdel ' + str(nr) + '\n')
    f.write('rm -f stop-this.sh')


