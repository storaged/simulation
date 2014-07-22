import array
import os
import gc
import atexit
import batchhelper


class HeatmapData:
    incr = 0
    paths = []
    registered = False
    def __init__(self, e, function, title):
	self.env = e
	self.values = []
	self.funct = function
	self.xdim = 0
	self.ydim = 0
	self.title = title
	self.filedesc = None
	self.filepath = None
	if True: # TODO: if save_run
	    import os.path
	    self.filepath = os.path.join(batchhelper.batchinfo.dirname, "heatmap-%s-%s-%s.bin" % (self.title, os.getpid(), HeatmapData.incr))
	    HeatmapData.incr += 1
	    self.filedesc = open(self.filepath, "wb+")
#	    os.unlink(self.filepath)
	    HeatmapData.paths.append(self.filepath)
	if not HeatmapData.registered:
	    def hm_cleanup():
	        for path in HeatmapData.paths:
		    os.unlink(path)
	    atexit.register(hm_cleanup)

	    HeatmapData.registered = True
	


    def save_generation(self):
	v = map(lambda plant: self.funct(plant), sorted(self.env.plants.values(), key = lambda p: p.ord_counter))
	v.sort(reverse = True)
	self.ydim = max(len(v), self.ydim)
	self.xdim += 1
	if self.filedesc == None:
	    self.values.append(v)
	else:
	    lenarr = array.array('L')
	    lenarr.append(len(v))
	    lenarr.tofile(self.filedesc)
	    varr = array.array('f')
	    varr.fromlist(v)
	    varr.tofile(self.filedesc)

    def prepare_for_drawing(self):
        if self.filedesc == None:
	    return
        self.filedesc.seek(0, 0)
        try:
	    while True:
		lenarr = array.array('L')
		lenarr.fromfile(self.filedesc, 1)
		varr = array.array('f')
		varr.fromfile(self.filedesc, lenarr[0])
		self.values.append(varr)
	except EOFError:
	    pass

    def done_drawing(self):
        if self.filedesc == None:
	    return
	del self.values
	self.values = []
	gc.collect()


    def __getitem__(self, coord, def_val = -1):
	(x, y) = coord
	if x < 0 or y < 0 or x >= self.xdim or y >= self.ydim:
	    raise IndexError("Index out of range")
	try:
	    return self.values[x][y]
	except IndexError:
	    return def_val
