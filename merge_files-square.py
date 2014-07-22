import glob
from misc import ListDict


glob_pattern = 'avg_aut*.txt'

def get_key(filename):
    return float(filename.rsplit('.', 1)[0].split('_')[2])


te_contents = ListDict()

files = []
minl = 999999999999999
for filename in sorted(glob.glob(glob_pattern), key=get_key):
    with open(filename) as f:
        l = f.readlines()
	minl = min(minl, len(l))
	te_contents.list_insert(get_key(filename), float(l[-1]))
	print get_key(filename)
	files.append(l)

if minl == 999999999999999:
    import sys
    sys.exit(0)

with open('square.Rdata', 'w') as outfile:
    for stress_level in sorted(te_contents.keys()):
        line = [str(stress_level)]
        for value in te_contents[stress_level]:
	    line.append(str(value))
	line.append('\n')
	outfile.write(' '.join(line))
	print len(line)
	
