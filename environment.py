#from distributions import *
import distributions
import random
#import parameters
from saveableparams import parameters
from table_util import table
from history import History
import selectors
import numpy
import debug
import array
#from plant import Plant

    
#----------------------------------------------------------------------------------------------------

class Environment:
    environments = 0
    def __init__(self):
        
        #-----location part
        if parameters.location_mode:
            self.mesh_size = 1./parameters.LD0range/2
            f = lambda size: [[{} for x in xrange(int(size)+1)] for y in xrange(int(size)+1)]
            self.mesh = f(self.mesh_size)
            map_path = parameters.map_phenotype_image(parameters.maps)
            self.load_terrain(map_path+".info.tmp", map_path+".tmp")
        #------------------

        from plant import Plant
        from phenotype import Phenotype

        self.plants = {}
        self.allplantslist = []
        self.generation = 0
        self.__class__.default = self
        self.__class__.environments += 1
        debug.g("niche %d" % parameters.niche_size)
        for i in xrange(parameters.niche_size):
            if parameters.location_mode:
                Plant.new(parameters.get_start_point(parameters.maps))
            else:
                Plant.new((0,0))
        debug.g("*** %d" % len(self.plants))
        self.optimal_global_phenotype = Phenotype()
        self.base_phenotype = Phenotype()
        self.survivors = parameters.niche_size
        self.randomkiller = selectors.KillerRandom()
        (self.killer, self.reproducer) = selectors.getSelectors()
        self.phenotype_link = Phenotype
        self.history = History(self)
        self.history.update()

    def load_terrain(self, info_filename, data_filename):
        size = (0,0)
        with open(info_filename) as f:
            arrinfo = array.array('L')
            arrinfo.fromfile(f, 2)
            size = (arrinfo[0], arrinfo[1])
        self.map_size = size
        self.phenotype_map = [[(1,1,1) for y in xrange(size[1])] for x in xrange(size[0])]

        with open(data_filename) as f:
            scale = lambda x: (float(x-127)/128)*parameters.map_phenotype_amplitude/2

            arr = array.array('B')
            arr.fromfile(f, size[0]*size[1]*3)
            for y in xrange(size[1]):
                for x in xrange(size[0]):
                    self.phenotype_map[x][y] = map(scale, (lambda nr: arr[nr:nr+3])(3*x+3*size[0]*y))
                    #debug.g(size)
                    #for x in xrange(63):
                    #	debug.g(self.phenotype_map[x*10][0])

    def register_new_plant(self, number, plant):
        self.plants[number] = plant
        ##TODO
        if parameters.location_mode:
            try:
                self.mesh[plant.scalex()][plant.scaley()][number] = plant
            except:
                debug.g(plant.scalex())
                debug.g(plant.scaley())
                debug.g(number)
                0/0

    def unregister_plant(self, number):
        ##TODO
        if parameters.location_mode:
            plant = self.plants[number]
            del self.mesh[plant.scalex()][plant.scaley()][number]
        del self.plants[number]

    def advance_generation(self):
        from phenotype import Phenotype
        from plant import Plant
        from math import log, sqrt
        #self.avg_transpositions_in_this_generation = 0

    #if self.generation%10==0:
    #	debug.g("====") 
    #	debug.g(self.optimal_global_phenotype.properties)
    #	debug.g(self.base_phenotype.properties)

        if parameters.random_pressure > 0.0:
        #    for plant in self.plants.values():
        #if happened(random_pressure):
        #    plant.die()
            self.randomkiller.eliminate(self.plants.values())
        self.killer.eliminate(self.plants.values())

        #=========LOCATION
        if parameters.location_mode:
            r = parameters.LD0range
            r2 = r*r

            def important_fields_in_mesh(location):
                f = lambda (x,y): [(x,y),(x-r,y-r),(x,y-r),(x+r,y-r),(x-r,y),(x+r,y),(x-r,y+r),(x,y+r),(x+r,y+r)]
                g = lambda x: -1<x and x<self.mesh_size
                h = lambda (x,y): (Plant.scale(x),Plant.scale(y))
                i = lambda (x,y): g(x) and g(y)
            #debug.g(location)
            #debug.g(r)
                fields = set() 
                for x in filter(i, map(h, f(location))): fields.add(x)
                return fields

            def shuffle(l):
                random.shuffle(l)
                return l
          
            def maybe_neighbour_kill(p1, p2):
                fitness_val = p1.fitness()
            
                d2_fun = lambda ((x1,y1), (x2,y2)): (x2-x1)**2+(y2-y1)**2
                d2 = d2_fun((p1.location, p2.location))
            
            ##range_val = -2*log(d/r)
            #try: range_val = 2*logr-log(d2)
            #except: range_val = 1
                import math
                f = lambda (y,ymax,ymin): (y-ymin)/(ymax-ymin)
                range_val = f((math.e**(d2), math.e**(r2), 1.))
                if range_val <= 1.:
                    return not distributions.happened(range_val * fitness_val)
                else: return False
            #debug.g("%f, %f" %(range_val, math.sqrt(d2)))

            for plant in shuffle(self.plants.values()):
                if not plant.dead:
                    for (x,y) in important_fields_in_mesh(plant.location):
                        if plant.dead: break
                        for killer_plant in (self.mesh[x][y]).values():
                            if maybe_neighbour_kill(plant, killer_plant) and plant.id != killer_plant.id: 
                                plant.die()
                                break
        #=================

        #transpositions_itg = 0
        #for plant in self.plants.values():
        #    transpositions_itg += plant.transpositions
        #self.avg_transpositions_in_this_generation = float(transpositions_itg) / float(len(self.plants.values()))
    
        self.history.update()

        v = self.plants.values()
        self.survivors = len(v)
        self.reproducer.reproduce(self.plants)

        ##KG
#        for plant in self.plants.values():
#            print " >> after reproduction part" + str(plant.aut_transposons) + "==" + str(len(plant.aut_transposons_list))
#            for x in plant.aut_transposons_list : 
#                print "TE #" + str(x.id) + ", parent: " + str(x.parent) + ", aut= " + str(x.is_aut)

        for plant in self.plants.values():            
            plant.evolve()

        self.allplantslist = self.plants.values()

        if parameters.expected_horiz_transfers > 0.0:
            for plant in self.plants.values():
                plant.perform_horizontal_transfers()

        if self.generation >= parameters.stability_period:
            if parameters.is_drift_directed:
                for _unused in range(parameters.number_of_mutations):
                    self.base_phenotype[distributions.runifint(0, parameters.no_phenotype_properties-1)] += parameters.expected_mutation_shift
            else:
                for _unused in range(parameters.number_of_mutations):
                    self.base_phenotype.mutate_once(stdev = parameters.expected_mutation_shift)

        self.optimal_global_phenotype = None
        if parameters.fluctuations_magnitude > 0.0:
            self.optimal_global_phenotype = self.base_phenotype.add(Phenotype.new_random(parameters.fluctuations_magnitude))
        else:
            self.optimal_global_phenotype = self.base_phenotype

        allpl = sorted(self.plants.values(), key = lambda p: p.ord_counter)

        i = 0
        for p in allpl:
            p.ord_counter = i
            i += 1

        #self.history.update()
        self.generation += 1

    def optimal_phenotype_on_map(self, (x,y)):
        scale = lambda (v, length): int(round((length-1)*(v+1)/2))
        xp = scale((x, self.map_size[0]))
        yp = scale((y, self.map_size[1]))
        return self.optimal_global_phenotype.get_map_phenotype(self.phenotype_map[xp][yp])
    def optimal_phenotype_without_map(self):
        return self.optimal_global_phenotype.get_phenotype_without_map()

    def average_transposon_number(self):
        sum = 0
        for plant in self.plants.values():
            sum += plant.transposons
        return float(sum)/float(len(self.plants))

    def average_fitness(self):
        sum = 0.0;
        for plant in self.plants.values():
            sum += plant.fitness()
        return float(sum)/float(len(self.plants))

    def stdev_fitness(self):
        eval = self.average_fitness()
        stdev = 0.0
        for plant in self.plants.values():
            stdev += abs(eval - plant.fitness())
        return stdev/float(len(self.plants))

    def average_funct(self, funct):
        sum = 0.0;
        for plant in self.plants.values():
            sum += funct(plant)
        if len(self.plants)==0: return 0.
        return sum/float(len(self.plants))

    def stdev_funct(self, funct):
        eval = self.average_funct(funct)
        stdev = 0.0
        for plant in self.plants.values():
            stdev += abs(eval - funct(plant))
        return stdev/float(len(self.plants))

    def median_funct(self, funct):
        lst = sorted(map(funct,self.plants.values()))
        ll = len(lst)
        if ll==0: return 0
        elif ll%2: return (lst[ll/2]+lst[ll/2-1])/2
        else: return lst[ll/2]

    def average_funct_trim_outliers(self, funct, percentile = 0.05):
        if percentile == 0.0:
            return self.average_funct(funct)
        tbl = []
        for plant in self.plants.values():
            tbl.append(funct(plant))
        tbl.sort()
        startidx = int(len(tbl)*percentile)
        endidx = int(len(tbl)*(1.0-percentile))
        if endidx == startidx:
            startidx = 0
            endidx = len(tbl)
        sum = 0.0
        for plantnr in xrange(startidx, endidx):
            sum += tbl[plantnr]
        if endidx - startidx == 0: return 0.
        return float(sum)/float(endidx - startidx)

    def fold_funct(self, funct, startval):
        ret = startval
        for plant in self.plants.values():
            ret = funct(plant, ret)
        return ret

    def average_distance(self, mc_samples = None):
        if mc_samples == None:
            ret = 0.0
            for plant1 in self.plants.values():
                for plant2 in self.plants.values():
                    ret += Phenotype.distance(plant1.phenotype, plant2.phenotype)
            numpl = len(self.plants)
            if numpl == 0: return 0.
            return ret / (numpl**2 - numpl)
        else:
            ret = 0.0
            tries_done = 0
            tries_valid = 0
            spk = self.plants.keys()
            if spk == []: return 0.
            while tries_done < mc_samples:
                p1 = random.choice(spk)
                p2 = random.choice(spk)
                tries_done += 1
                if p1 != p2:
                    tries_valid += 1
                    ret += self.phenotype_link.distance(self.plants[p1].phenotype, self.plants[p2].phenotype)
            if tries_valid == 0:
                tries_valid += 1
            return ret / tries_valid

    def pickle(self):
        import cPickle
        import cStringIO

        ret = cStringIO.StringIO()

        histparams = self.history.params
        self.history.params = None

        heatmap_funs = {}
        for key, val in self.history.heatmaps.items():
            heatmap_funs[key] = val.funct
            val.funct = None
    
        cPickle.dump(self, ret)

        self.history.params = histparams

        for key, val in heatmap_funs.items():
            self.history.heatmaps[key].funct = val

        s = ret.getvalue()

        ret.close()

        return s

