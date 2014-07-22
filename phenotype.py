import distributions
import random
#import parameters as parameters
from saveableparams import parameters
from table_util import table
import debug

	
    
#----------------------------------------------------------------------------------------------------
class Phenotype:
    no_map_phenotype_properties = 3
    if no_map_phenotype_properties > parameters.no_phenotype_properties:
	    debug.terminate("no_phenotype_properties > no_map_phenotype_properties")
    def __init__(self):
	self.properties = []
	for i in xrange(parameters.no_phenotype_properties):
	    self.properties.append(0)

    def get_map_phenotype(self, map_phenotype):
      ph = Phenotype()
      ph.properties = map_phenotype+self.properties[Phenotype.no_map_phenotype_properties:]
      return ph
    def get_phenotype_without_map(self):
      return self
    
    @staticmethod
    def distance(ph1, ph2):
	#Euclidean distance
	dist = 0.0
	for i in xrange(parameters.no_phenotype_properties):
	    dist += abs(ph1.properties[i] - ph2.properties[i])**2
	return dist**0.5

    @staticmethod
    def new():
	return Phenotype.new_random()

    def mutate_once(self, stdev = None):
	pos = distributions.runifint(0, parameters.no_phenotype_properties-1)
	if stdev == None:
	    self.properties[pos] += distributions.rnorm(0.0, parameters.mutation_stdev)
	else:
	    self.properties[pos] += distributions.rnorm(0.0, stdev)

    def TE_driven_mutation(self, change):
	pos = distributions.runifint(0, parameters.no_phenotype_properties-1)
	self.properties[pos] += change


    def mass_mutate(self, no_times, stdev = None):
	if stdev == None:
	    stdev = parameters.mutation_stdev
	mutations = distributions.n_balls_into_k_bins(no_times, len(self.properties))
	for i in xrange(len(self.properties)):
	    if mutations[i] > 0:
		self.properties[i] += distributions.rnorm(0.0, (mutations[i]**0.5)*stdev)

    def mutate(self, no_times, stdev = None):
        if no_times < 1:
	    return
	if no_times > parameters.no_phenotype_properties:
	    self.mass_mutate(no_times, stdev)
	else:
	    for i in xrange(no_times):
		self.mutate_once(stdev)

    def mutate_TE(self, no_times, stdev = None):
        if no_times < 1:
	    return
	if no_times > parameters.no_phenotype_properties:
	    self.mass_mutate(no_times, stdev)
	else:
	    for i in xrange(no_times):
		self.mutate_once(stdev)



    @staticmethod
    def new_random(stdev = None):
	p = Phenotype()
	if stdev == None:
	    stdev = parameters.initial_phenotype_stdev
	for i in xrange(parameters.no_phenotype_properties):
	    p.properties[i] = distributions.rnorm(0, stdev)
	return p

    def add(self, other):
	p = Phenotype()
	for i in xrange(parameters.no_phenotype_properties):
	    p.properties[i] = self[i] + other[i]
	return p

    # get random point (uniformly) from |properties|-dim cube. 
    def generate_phenotype(self, other):
	p = Phenotype()
	for i in xrange(parameters.no_phenotype_properties):
	    p.properties[i] = random.uniform(self[i], other[i])
	return p

 
    def closing_by_mutation_prob(self, other):
	sum = 0.0
	for i in xrange(parameters.no_phenotype_properties):
	    sum += distributions.pnorm(abs(other[i] - self[i])*2, 0.0, parameters.transposition_mutation_stdev) - 0.5
	return sum/parameters.no_phenotype_properties

#    def exp_dist_delta(self, other):
#	sum = 0.0
#	for i in xrange(

    def copy(self):
	np = Phenotype()
	np.properties = self.properties[:]
	return np

    def __str__(self):
	r = "Phenotype("
	for val in self.properties:
	    r += str(val) + ", "
	return r+")"

    def __getitem__(self, key):
	return self.properties[key]

    def __setitem__(self, key, item):
	self.properties[key] = item
