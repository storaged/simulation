import glob



glob_pattern = 'avg_aut*.txt'

def get_key(filename):
    return int(filename.rsplit('.', 1)[0].split('_')[2])



files = []
minl = 999999999999999
for filename in sorted(glob.glob(glob_pattern), key=get_key):
    with open(filename) as f:
        l = f.readlines()
	minl = min(minl, len(l))
	files.append(l)

if minl == 999999999999999:
    import sys
    sys.exit(0)

with open('heatmap.Rdata', 'w') as outfile:
    for i in xrange(minl):
        line = []
        for srcfilelines in files:
	    line.append(str(float(srcfilelines[i])))
	line.append('\n')
	outfile.write(' '.join(line))

	
