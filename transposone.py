import distributions
from saveableparams import parameters
import random
##KG
##Transposone class, representing a TE on the DNA-string
##has an id numer and link to it's parent 
##there is one instance of TE with given id, plants only store the id
class Transposone:
    counter = 0
    
    def __init__(self, aut, parent = None):
        self.id = self.__class__.counter
        self.__class__.counter += 1
        self.parent = parent
        self.is_aut = aut
        self.trait_no = 0
        if parameters.multidim_changes:
            self.mutation_rate = []
            for i in xrange(parameters.no_phenotype_properties):
                self.mutation_rate.append(distributions.rnorm(0.0, parameters.transposition_mutation_stdev))
        else:
            self.trait_no = random.randint(0, parameters.no_phenotype_properties-1)
            self.mutation_rate = distributions.rnorm(0.0, parameters.transposition_mutation_stdev)
        
        
	def __repr__(self):
		return "TE #" + str(self.id) + ", parent: " + str(self.parent) + ", aut= " + str(self.is_aut)

	def __str__(self):
		return "TE #" + str(self.id) + ", parent: " + str(self.parent) + ", aut= " + str(self.is_aut)
