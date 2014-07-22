import subprocess
import time
import sys
import os
import shutil
import random
import signals
import stat

signals.setup_ignore()


import glob

instances = []

for path in glob.glob('batch-run-*'):
    instances.append(path.split('-')[-1])






def writescript(nr):
    with open("run-sim-"+str(i)+".sh", "w") as f:
	f.write("#!/bin/bash\n")
	f.write("hostname\n")
	f.write('date\n')
	f.write("for C in pypy-c1.9 pypy /home/mist-sim/pypy-1.9/bin/pypy pypy-c1.8 /home/mist-sim/pypy-1.8/bin/pypy python2.7 python\n")
	f.write("do\n")
	f.write("	if command -v $C\n")
	f.write("	then\n")
	f.write("		echo Interpreter: $C\n")
	f.write("		$C restore.py " + str(i) + "\n")
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
#    print "qsub -S /bin/bash -cwd -q sim -j y -o output-" + str(i) + " run-sim-" + str(i) + ".sh"


with open("stop-this.sh", 'w') as f:
    f.write('#!/bin/bash\n')
    os.chmod("stop-this.sh", stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH | stat.S_IXGRP | stat.S_IXOTH)
    for command in commands:
	o = subprocess.check_output(command, shell=True)
	print o,
	nr = int(o.split()[2])
	f.write('qdel ' + str(nr) + '\n')



