from model_init import Runinfo
import atexit
import os
import array
from model_init import Runinfo
from process_results import process_results
import parameters
from saveableparams import parameters as parameters2
import debug

class Listeners:
    listeners = []
    synced = False
    localtmp = True
    tmperase = True
    number = 0
    @staticmethod
    def save_generation():
	for listener in Listeners.listeners:
	    listener.save_generation()
    @staticmethod
    def register_listener(l):
	Listeners.listeners.append(l)

    @staticmethod
    def flush_all():
	for listener in Listeners.listeners:
	    listener.outfile.flush()


class GenericListener:
    def __init__(self, name):
	Listeners.register_listener(self)
	self.filepath = os.path.join(Runinfo.out_dir_path, 'output-%s.bin' % name)
	if Listeners.localtmp:
	    self.filepath = os.path.join(parameters.tmpdir, "output-%s-%s-%s.bin" % (name, os.getpid(), Listeners.number))
	self.outfile = open(self.filepath, 'w+')
	Listeners.number += 1
	self.name = name
	if Listeners.tmperase:
	    os.unlink(self.filepath)
	atexit.register(self.cleanup)

    def cleanup(self):
	self.outfile.close()

    def cflush(self):
	if Listeners.synced:
	    self.outfile.flush()

    def save_generation(self):
	raise NotImplementedError('That\'s an abstract class')


class ListenerHeatmap(GenericListener):
    def __init__(self, name, funct, data_type, trim_percentile = 0.0):
	GenericListener.__init__(self, name)
	self.funct = funct
	self.data_type = data_type
	self.outfile.write(data_type)
	self.trim_percentile = trim_percentile
	self.cflush()

    def save_generation(self):
	values = array.array(self.data_type)
	for plant in sorted(Runinfo.environment.plants.values(), key=lambda p: p.ord_counter):
		#try:
		#	values.append(self.funct(plant))
		#except:
		#	debug.g(plant)
		#	debug.g(self.data_type)
		#	debug.g(plant.ord_counter)
		#	debug.g(self.funct(plant))
		#	debug.g(self.name)
		values.append(self.funct(plant))
	
	lenarr = array.array('L')
	lenarr.append(len(values))
	lenarr.tofile(self.outfile)
	values.tofile(self.outfile)
	self.cflush()

    def cleanup(self):
        self.outfile.flush()
	self.outfile.seek(0)
	tfilepath = os.path.join(Runinfo.out_dir_path, 'output-%s.bin' % self.name)
	process_results(self.outfile, tfilepath + ".Rdata", tfilepath + ".desc.Rdata", trim_percentile = self.trim_percentile)
	GenericListener.cleanup(self)

class ListenerSingleValue(GenericListener):
    def __init__(self, name, funct):
	GenericListener.__init__(self, name)
	self.funct = funct
	self.collecteddata = []
	
    def save_generation(self):
        self.collecteddata.append(str(self.funct()))

    def cleanup(self):
        with open(os.path.join(Runinfo.out_dir_path, 'output-%s.bin.Rdata' % self.name), 'w') as f:
	    f.write('\n'.join(self.collecteddata))
	GenericListener.cleanup(self)

class ListenerImage(GenericListener):
    def __init__(self, name, funct):
        GenericListener.__init__(self, name)
	self.funct = funct
	self.data = []
	self.maxlen = 0
#	self.fhandle = open(os.path.join(Runinfo.out_dir_path, 'imagedata-%s.bin.Rdata' % self.name), 'w')
	

    def save_generation(self):
        gen = [self.funct(p) for p in sorted(Runinfo.environment.plants.values(), key=lambda p: p.ord_counter)]
        self.data.append(gen)
	self.maxlen = max(self.maxlen, len([self.funct(p) for p in sorted(Runinfo.environment.plants.values(), key=lambda p: p.ord_counter)]))

    def cleanup(self):
        with open(os.path.join(Runinfo.out_dir_path, 'imagedata-%s.bin.Rdata' % self.name), 'w') as f:
	    for row in self.data:
		rs = []
	        for i in xrange(self.maxlen):
		    if i<len(row):
		        rs.append(str(row[i]))
		    else:
		        try: rs.append(str(row[0] - row[0]))
		        except: debug.terminate("simulation error in listeners.py line 125")
		rs.append('\n')
		f.write(' '.join(rs))
		    

class ListenerMapByPlant(GenericListener):
  def __init__(self, name, funct, snapshots):
    GenericListener.__init__(self, name)
    self.funct = funct
    self.data = []
    self.snapshotsDict = {}

    self.snapshotsList = snapshots
    with open(os.path.join(Runinfo.out_dir_path, 'mapdata-%s-generations.bin.Rdata' % self.name), 'w') as f:
      for generation in self.snapshotsList:
        f.write("%d\n" % generation)
    self.savedCounter = 0

    self.xyval_to_row = lambda ((x,y),(halo1, fill1, halo2, fill2)): "%f %f %f %f %f %f" % (x,y,halo1,fill1,halo2,fill2) 
    for x in snapshots: self.snapshotsDict[x]=True

  def save_generation(self):
    generation = Runinfo.environment.generation
    if self.snapshotsDict.has_key(generation): 
      self.data += [(generation, [self.funct(p) for p in Runinfo.environment.plants.values()])]
      self.savedCounter+=1
      if self.savedCounter == parameters.ListenerMapByPlant_savingInterval: self.cleanup()

  def cleanup(self):
    debug.g("saving some data...")
    self.savedCounter = 0
    for generation, points in self.data:
      data = "".join(map(lambda point:"%s\n" % self.xyval_to_row(point), points))
      with open(os.path.join(Runinfo.out_dir_path, 'mapdata-%s-gen%d.bin.Rdata' % (self.name,generation)), 'w') as f:
        f.write(data)
    del self.data
    self.data = []


class ListenerMapByLocation(ListenerMapByPlant):
	def __init__(self, name, funct_xy, funct_arr, snapshots):
		ListenerMapByPlant.__init__(self, name, funct_xy, snapshots)
		self.funct_arr = funct_arr


	def save_generation(self):
		generation = Runinfo.environment.generation
		if self.snapshotsDict.has_key(generation): 
			arr = self.funct_arr(Runinfo.environment)
			tmp=[]
			sizex = len(arr)
			sizey = len(arr[0])
			scale = lambda (v, vsize): 2*(v/float(vsize)-0.5)
			for x in xrange(sizex):
				for y in xrange(sizey): 
					tmp+=[((scale((x, sizex)), scale((y, sizey))), self.funct(arr[x][y]))]
			self.data += [(generation, tmp)]


def setup_listeners():
    ListenerHeatmap('aut_transposons', lambda p: p.aut_transposons, 'L')
    ListenerHeatmap('nonaut_transposons', lambda p: p.nonaut_transposons, 'L')
    ListenerHeatmap('fitness', lambda p: p.fitness(), 'f')
    ListenerHeatmap('total_mutations', lambda p: p.total_mutations, 'L')
    ListenerSingleValue('transpositions', lambda: Runinfo.environment.average_funct(lambda p: p.transpositions))
    ListenerSingleValue('transpositions-median', lambda: Runinfo.environment.median_funct(lambda p: p.transpositions))
    ListenerSingleValue('random_mutations', lambda: Runinfo.environment.average_funct(lambda p: p.random_mutations))
    
    ListenerImage('aut_transposons_i', lambda p: p.aut_transposons)
    ListenerImage('nonaut_transposons_i', lambda p: p.nonaut_transposons)
    ListenerImage('fitness_i', lambda p: p.fitness())
    #ListenerMapByPlant('alive_locations', lambda p: (p.location, p.fitness()), parameters.location_plots())

    if parameters2.location_mode:
        alive_loc_fun = lambda p: (p.location, (p.nonaut_transposons, min(1, p.aut_transposons), p.fitness(), 1))
        ListenerMapByPlant('alive_locations', alive_loc_fun, parameters.location_plots())

    #phfun = lambda x: (x/parameters.map_phenotype_amplitude+0.5, 1)
    #ListenerMapByLocation('phenotype_map_RED',   lambda (ph1, _, __): phfun(ph1), lambda env: env.phenotype_map, [0])
    #ListenerMapByLocation('phenotype_map_GREEN', lambda (_, ph2, __): phfun(ph2), lambda env: env.phenotype_map, [0])
    #ListenerMapByLocation('phenotype_map_BLUE',  lambda (_, __, ph3): phfun(ph3), lambda env: env.phenotype_map, [0])
