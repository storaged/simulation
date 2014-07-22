##KG
##Transposone class, representing a TE on the DNA-string
##has an id numer and link to it's parent 
##there is one instance of TE with given id, plants only store the id
import distributions
from plant import Plant
from phenotype import Phenotype
from saveableparams import parameters as param

def merge(t1, t2):
    res = []
    i, j = 0, 0
    while i < len(t1) and j < len(t2) :
        if t1[i].id < t2[j].id : 
            res.append(t1[i])
            i += 1
        else: 
            res.append(t2[j])
            j += 1
    if i < len(t1):
        res += t1[i:]
    if j < len(t2):
        res += t2[j:]
    return res

class Gamete:
    
    def __init__(self, aut_TE_list, nonaut_TE_list, origin, sex=None):
        self.aut_TE_list = aut_TE_list
        self.nonaut_TE_list = nonaut_TE_list
        self.origin = origin
        self.sex = sex

    def crossbreed(self, gamete):
        parent1 = self.origin
        parent2 = gamete.origin

        new_aut_TE = merge(self.aut_TE_list, gamete.aut_TE_list)
        new_nonaut_TE = merge(self.nonaut_TE_list, gamete.nonaut_TE_list)
        new_transposase_activity = 0.5 * (parent1.transposase_activity + parent2.transposase_activity)

        if param.location_mode :
            p = Plant.new(parent1.location, len(new_aut_TE), new_transposase_activity)
        else :
            p = Plant.new((0,0), len(new_aut_TE), new_transposase_activity)

        p.inactive_transposons = 0 #self.inactive_transposons

        p.phenotype = parent1.phenotype.generate_phenotype(parent2.phenotype)
        p.ord_counter = parent1.ord_counter #nie wiem co tu ma byc

        p.aut_transposons_list = new_aut_TE
        p.aut_transposons = len(new_aut_TE)

        p.nonaut_transposons_list = new_nonaut_TE
        p.nonaut_transposons = len(new_nonaut_TE)

        return p 
