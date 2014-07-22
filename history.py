from table_util import table
from phenotype import Phenotype
from saveableparams import parameters
from listeners import Listeners

class History:

    def __init__(self, env, silent = False):

	self.params = [
	("generation", lambda: self.e.generation, 1.0),
	("avg aut transposons", lambda: self.e.average_funct_trim_outliers(lambda p: p.aut_transposons), 1.0),
#	("median aut transposons", lambda: self.e.median_funct(lambda p: p.aut_transposons), 1.0),
	("avg nonaut transposons", lambda: self.e.average_funct_trim_outliers(lambda p: p.nonaut_transposons), 1.0/10.0),
#	("max transposons", lambda: self.e.fold_funct(lambda p, x: max(p.transposons, x), 0), 1.0/10.0),
	("avg inactive transp", lambda: self.e.average_funct_trim_outliers(lambda p: p.inactive_transposons), 1.0/100.0),
#	("stdev transposons", lambda: self.e.stdev_funct(lambda p: p.transposons), 1.0),
	("avg fitness", lambda: self.e.average_funct(lambda p: p.fitness()), 1.0),
#	("stdev fitness", lambda: self.e.stdev_funct(lambda p: p.fitness()), 1.0),
	("avg transp activ", lambda: self.e.average_funct_trim_outliers(lambda p: p.transposase_activity), 1.0),
#	("stdev transp activ", lambda: self.e.stdev_funct(lambda p: p.transposase_activity), 1.0),
#	("survivors", lambda: float(self.e.survivors), 1.0/10.0),
#	("avg transpositions", lambda: float(self.e.avg_transpositions_in_this_generation), 1.0),
	("avg transpositions", lambda: self.e.average_funct_trim_outliers(lambda p: p.transpositions), 1.0),
	("avg distance between plants", lambda: self.e.average_distance(100), 1.0/1.0),
#	("avg dist to opt", lambda: self.e.average_funct(lambda p: Phenotype.distance(p.phenotype, self.e.optimal_phenotype)), 1.0/1.0),
#	("min dist to opt", lambda: self.e.fold_funct(lambda p, x: min(p.distance_to_opt(), x), 1000000000.0), 1.0),
	("max fitness", lambda: self.e.fold_funct(lambda p, x: max(p.fitness(), x), -1000000000.0), 1.0),
#	("no plants", lambda: len(self.e.plants), 1.0/1000.0),
#	("no maxfit plants", lambda: self.e.fold_funct(ffold, (-1e100, 0))[1], 1.0),
	("avg prob of beneficial mutation from TE insertion", lambda: self.e.average_funct(lambda p: p.phenotype.closing_by_mutation_prob(self.e.optimal_global_phenotype)), 10.0),
	("avg total transp", lambda: self.e.average_funct_trim_outliers(lambda p: p.total_transposons()), 1.0/100.0),
	]

	self.silent = silent
	self.e = env
	self.t = table()

	for parset in self.params:
	    self.t.add_column(parset[0])

	self.scales = []
	self.scalesdict = {}
	for parset in self.params:
	    self.scalesdict[parset[0]] = parset[2]
	    self.scales.append(parset[2])



	if not self.silent:
	    print self.t.header()
    
    def update(self):
        if not parameters.plots_enabled:
	    return

	e = self.e
	row = []
	for parset in self.params:
	    row.append(parset[1]())
        self.t.add_row(row)
#        e.average_funct(lambda p: p.transposons)/10.0,
#	e.fold_funct(lambda p, x: max(p.transposons, x), 0)/10.0,
#	e.average_funct(lambda p: p.inactive_transposons)/100.0,
#       e.stdev_funct(lambda p: p.transposons),
#        e.average_funct(lambda p: p.fitness()),
        #e.stdev_funct(lambda p: p.fitness()) * 10,
#        e.average_funct(lambda p: p.transposase_activity),
#       e.stdev_funct(lambda p: p.transposase_activity),
#       float(e.survivors) / 100.0,
#        float(e.transpositions_in_this_generation) / 100.0,
        #e.average_distance(100)/1000.0,
        #e.average_funct(lambda p: Phenotype.distance(p.phenotype, e.optimal_phenotype))/1000.0,
        #e.fold_funct(lambda p, x: min(p.distance_to_opt(), x), 1000000000.0)/1000.0,
        #e.fold_funct(lambda p, x: max(p.fitness(), x), -1000000000.0) * 10,
#       len(e.plants)/1000.0,
#       e.fold_funct(ffold, (-1e100, 0))[1]
#        ])

	Listeners.save_generation()

	if not self.silent:
            print self.t.row()


