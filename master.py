import multiprocessing
import time
import sys
import os
import shutil
import random
from count_params import count_params
import signals

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

random.shuffle(instances)

p = multiprocessing.Pool(25)


commands = []
for i in instances:
    commands.append("python batchrun.py " + str(i) + " > output-" + str(i))

p.map(os.system, commands)


