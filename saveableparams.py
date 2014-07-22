import distributions
_ia = 0
_selected = None

class Parameters:
    default = None
    def __init__(self):
        Parameters.default = self
        self.paramnames = []

    def _memorise_text(self, filename):
	f = open(filename, "r")
	self.params_text = f.read()
	f.close()

    def load_from_file(self, filename = "parameters.py"):
	self._memorise_text(filename)

	from preparam import *
	vars  = []
	vars2 = []
	vars  = set(locals().keys())
	execfile(filename)
	vars2 = set(locals().keys())

	newnames = vars2 - vars

	for name in newnames:
	    self.__dict__[name] = locals()[name]
	
	self.paramnames = newnames
	self.initstr = str(self)
	
	return newnames

    def save_to_file(self, filename):
	f = open(filename, "w")
	f.write(self.params_text)
	f.flush()
	f.close()

    def load_batch_mode(self, id, filename = "parameters.py"):
	global _ia
	global _selected
	self._memorise_text(filename)
	_ia = 0
	batchparams = Parameters()
	paramnames = batchparams.load_from_file(filename)
	nameslist = sorted(paramnames)
	for name in nameslist:
	    if not isinstance(batchparams.__dict__[name], list):
		batchparams.__dict__[name] = [batchparams.__dict__[name]]

	_selected = None
		
	def splitname(namesl, parlist, acc):
	    if parlist == []:
		return
	    else:
		newacc = acc[:]
		newacc.append((namesl[0], parlist[0]))
		getassignments(namesl[1:], newacc)
		splitname(namesl, parlist[1:], acc)

	def getassignments(names, acc):
	    global _selected
	    global _ia
	    if names == []:
		if _ia == id:
		    _selected = acc
		_ia += 1
		return 
	    else:
		splitname(names, batchparams.__dict__[names[0]], acc)

	getassignments(nameslist, [])


	for (key, val) in _selected:
	    self.__dict__[key] = val

	self.paramnames = paramnames
	self.initstr = str(self)

	return paramnames

    def __repr__(self):
      
      
	lines = []

	for name in self.paramnames:
	    if not self.__dict__[name].__class__.__name__ in ['function', 'module', 'ReproducerDefault'] and not name in ['draw_legends', 'headless_mode', 'plotting_frequency', 'heatmaps_enabled']:
		lines.append(name + "   = " +  str(self.__dict__[name]))

	return '\n'.join(lines)


#parameters = Parameters()



