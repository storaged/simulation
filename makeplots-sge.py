import multiprocessing
import time
import sys
import os
import shutil
import random
import signals
import glob
from count_params import count_params

signals.setup_ignore()

instances_init = count_params()



instances = glob.glob("batch-run-*")


random.shuffle(instances)

p = multiprocessing.Pool(1)


def writescript(instance):
    with open("make-plot-"+str(instance)+".sh", "w") as f:
	f.write("#!/bin/bash\n")
	f.write("cd "+str(instance)+"\n")
	f.write("R -q --no-save --vanilla -f ../makeplot.R\n")
	
    


commands = []
for i in instances:
    writescript(i)
    try:
	os.unlink("plot-output-" + str(i))
    except OSError:
	pass
#    commands.append("qsub -cwd -sync y -q sim -j y -l pamiec_virt=4G -o output-" + str(i) + " run-sim-" + str(i) + ".sh")
    commands.append("qsub -S /bin/bash -cwd -q sim -j y -o plot-output-" + str(i) + " make-plot-" + str(i) + ".sh")

p.map(os.system, commands)


