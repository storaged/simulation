import os 
import sys
import datetime


def get_runtime(path):

    try:
	start = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(str(path), 'initial')))
	end = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(str(path), 'plot-3.png')))

	return end - start
    except OSError:
	return None

def get_file_contents(path):
  try:
    with open(path) as f:
	return f.read().rstrip()
  except IOError:
    return 'None'

if len(sys.argv) > 2:
    print get_runtime(sys.argv[1])
else:
    import glob
    list_t = []
    for path in glob.glob('batch-run-*'):
        rt = get_runtime(path)
        list_t.append((rt, path + ':	'+ str(get_runtime(path)) + '	' + get_file_contents(os.path.join(path, 'output-aut_transposons.bin.desc.Rdata')) + '	' + get_file_contents(os.path.join(path, 'output-aut_transposons.bin.desc.Rdata'))))

    for s in sorted(list_t, key = lambda x: x[0] if x[0] != None else datetime.timedelta.max):
	print s[1]
