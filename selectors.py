import distributions
import random

class SelectorRandom:
    def __init__(self, _evalue):
	self.evalue = evalue
    def select(self, iterable):
	chosen = []
	leftbehind = []
	for element in iterable:
	    if(happened(evalue)):
		chosen.append(element)
	    else:
		leftbehind.append(element)
	return (chosen, leftbehind)


class ReproducerFitnessBasedDefault:
    def __init__(self):
        self.fallback = ReproducerRandom()
    def reproduce(self, plants):
        from saveableparams import parameters
#       global parameters.niche_size
        to_create = max(0, parameters.niche_size - len(plants))
        if to_create > 0:
            correction = 0.0
            minfit = 1e100
            for plant in plants.values():
                pf = plant.fitness()
                minfit = min(pf, minfit)
            for plant in plants.values():
                correction += plant.fitness() - minfit
            correction /= float(to_create)
#            numplants = len(plants)

            if correction == 0.0:
                self.fallback.reproduce(plants)
                return

            for plant in plants.values():
                pf = plant.fitness()
                f = (pf - minfit) / correction
                reps = distributions.rpois(f)
                for i in xrange(reps):
                    plant.copy()
#               print fitness:, pf,  corrected: , pf - minfit,  normalized:, f,  copies: , reps


class ReproducerFitnessBased01:
    def __init__(self):
	self.fallback = ReproducerRandom()
    def reproduce(self, plants):
	from saveableparams import parameters
	to_create = max(0, parameters.niche_size - len(plants))
	if to_create > 0:
	    correction = 0.0
	    for plant in plants.values():
		correction += plant.fitness()
	    correction /= float(to_create)
	    if correction == 0.0:
		self.fallback.reproduce(plants)
		return
	    for plant in plants.values():
		pf = plant.fitness()
		f = pf / correction
		reps = distributions.rpois(f)
		for i in xrange(reps):
		    plant.copy()




class ReproducerFitnessBased01Merged:
    def __init__(self):
	self.fallback = ReproducerRandom()
    def reproduce(self, plants):
	from saveableparams import parameters
	to_create = parameters.niche_size
	if to_create > 0:
	    correction = 0.0
	for plant in plants.values():
	    correction += plant.fitness()
	correction /= float(to_create)
	if correction == 0.0:
	    self.fallback.reproduce(plants)
	    return
	for plant in plants.values():
	    pf = plant.fitness()
	    f = pf / correction
	    reps = distributions.rpois(f)
	    if reps == 0:
	        plant.die()
	    else:
		for i in xrange(reps-1):
		    plant.copy()


class ReproducerFitnessBasedMerged:
    def __init__(self):
        self.fallback = ReproducerRandom()
    def reproduce(self, plants):
	from saveableparams import parameters
#	global parameters.niche_size
        to_create = parameters.niche_size #max(0, parameters.niche_size - len(plants))
        if to_create > 0:
            correction = 0.0
            minfit = 1e100
            for plant in plants.values():
                pf = plant.fitness()
                minfit = min(pf, minfit)
            for plant in plants.values():
                correction += plant.fitness() - minfit
            correction /= float(to_create)
#            numplants = len(plants)

	    if correction == 0.0:
		self.fallback.reproduce(plants)
		return

            for plant in plants.values():
                pf = plant.fitness()
                f = (pf - minfit) / correction
                reps = distributions.rpois(f)
		if reps == 0:
		    plant.die()
		else:
                    for i in xrange(reps-1):
                        plant.copy()
#               print fitness:, pf,  corrected: , pf - minfit,  normalized:, f,  copies: , reps




class ReproducerFitnessBasedMergedUnscaled:
    def __init__(self):
        self.fallback = ReproducerRandom()
    def reproduce(self, plants):
        from saveableparams import parameters
        import debug
        debug.g("%d" % len(plants.values()))
        to_create = parameters.niche_size #max(0, parameters.niche_size - len(plants))
        if to_create > 0:
            correction = 0.0
            for plant in plants.values():
                correction += plant.fitness()
            correction /= float(to_create)

            if correction == 0.0:
                self.fallback.reproduce(plants)
                return
            for plant in plants.values():
                pf = plant.fitness()
                f = pf / correction
                reps = distributions.rpois(f)
                if reps == 0:
                    plant.die()
                else:
                    for i in xrange(reps-1):
                        plant.copy()


class ReproducerLocationModeOff:
    def __init__(self):
        self.fallback = ReproducerRandom()
    def reproduce(self, plants):
        from saveableparams import parameters
        import debug
        #debug.g("plants size --- %d" % len(plants.values()))
        to_create = parameters.niche_size #max(0, parameters.niche_size - len(plants))
        total_fitness_male = 0.0
        total_fitness_female = 0.0
        male = []
        female = []

        # podliczamy fitness dla kazdej plci z osobna
        # i tworzymy dwie osobne listy z podzialem na plec
        # w przypadku populacji aseksualnej wszystkie rosliny sa plci meskiej ( i co teraz feministki? :) )
        for plant in plants.values():
            if plant.sex == 0: # male
                total_fitness_male += plant.fitness()
                male.append(plant)
            else :  # female
                total_fitness_female += plant.fitness()
                female.append(plant)
        #debug.g('total male fitness = %f' % total_fitness_male)
        #debug.g('total female fitness = %f' % total_fitness_female)
        # decydujemy kto bedzie rodzicem roslin z nastepnego pokolenia
        # wybieramy niche_size liczb z przedzialu [0, total_fitness_{male/female}]
        
        random.shuffle(male)

        if parameters.sexual_mode:
            mothers_chosen = sorted([x*random.random() for x in [total_fitness_female] * parameters.niche_size])
        
        fathers_chosen = sorted([x*random.random() for x in [total_fitness_male] * parameters.niche_size])
        
        #debug.g('fathers_chosen = %d' % len(fathers_chosen))

        #debug.g('mothers_chosen = %d' % len(mothers_chosen))


        iter_father = 0
        iter_mother = 0
        sum_fit_male = 0.0
        sum_fit_female = 0.0
        i_m = 0
        i_f = 0
        #debug.g('no plants: %d ' % len(plants.values()) )
        for i in xrange(parameters.niche_size):
            # zawsze potrzebujemy jednego rodzica
            tmp_fit_male = fathers_chosen[i]
            while sum_fit_male < tmp_fit_male and iter_father < len(male):
                sum_fit_male += male[iter_father].fitness()
                iter_father += 1
                if(iter_father >= 2):
                    male[iter_father - 2].die()
            if iter_father <= len(male):
                father = male[iter_father - 1]

                # jesli populacja sexualna to wybieramy pare
                if parameters.sexual_mode : 
                    tmp_fit_female = mothers_chosen[i]
                    while sum_fit_female < tmp_fit_female and iter_mother < len(female) :
                        sum_fit_female += female[iter_mother].fitness()
                        iter_mother += 1
                        if(iter_mother >= 2):
                            female[iter_mother - 2].die()
 
                    if iter_mother <= len(female):
                        mother = female[iter_mother - 1]
                        g1 = father.getGamete()
                        g2 = mother.getGamete()
                        g1.crossbreed(g2)

                # jesli aseksualna powielamy pierwszego rodzica
                else : 
                    father.copy()           
                    father.die(False)
            # index out of range ... there is a bug
            else:
                import debug
                debug.g("Index out of range when choosing first parent")
                0/0

        if iter_father > 1:
            while iter_father <= len(male) :
                male[iter_father - 1].die()
                iter_father += 1

        if parameters.sexual_mode and iter_mother > 1:
            while iter_mother <= len(female) :
                female[iter_mother - 1].die()
                iter_mother += 1

#        if to_create > 0:
#            correction = 0.0
#            for plant in plants.values():
#                correction += plant.fitness()
##            correction /= float(to_create)
#
#            if correction == 0.0:
#                self.fallback.reproduce(plants)
#                return
#            for plant in plants.values():
#                pf = plant.fitness()
#                f = pf / correction
#                reps = distributions.rpois(f)
#                if reps == 0:
#                    plant.die()
#                else:
#                    for i in xrange(reps-1):
#                        plant.copy()


class ReproducerRandom:
    def reproduce(self, plants):
	from saveableparams import parameters
	to_create = max(0, parameters.niche_size - len(plants))
	create_eval = float(to_create)/float(len(plants))
	for plant in plants.values():
	    for i in xrange(distributions.rpois(create_eval)):
		plant.copy()

class ReproducerEveryone:
    def __init__(self):
      self.gen=0
    def reproduce(self, plants):
      from saveableparams import parameters
      import debug
      pl = len(plants.values())
      offsprings=0
      for p in plants.values():
        offspring = distributions.rbinom(parameters.offspring_size, p.fitness())
        for _ in xrange(offspring): p.copy()
        p.die()
        offsprings+=offspring
      self.gen+=1
      debug.g("%d, %d+%d" % (self.gen, pl, offsprings))

      #debug.g("%d, %d+%d" % (self.gen, len(plants), len(map(
      #  lambda p: p.copy(), 
      #  filter(
      #    #lambda p: distributions.happened((p.fitness())*parameters.birth_factor), 
      #    lambda p: distributions.happened(p.fitness()), 
      #    plants.values())))))

#########################
## Sexual reproduction ##
#########################

## 1)
## During reproduction each plant produces some number of gametes according to it's phenotype
## After production of gametes, they are paired in a random way.
## Each pair of gametes creates new Plant.
class ReproducerEveryoneSexual:
    def __init__(self):
      self.gen=0
    def reproduce(self, plants):
      from saveableparams import parameters
      import debug
      import random
      pl = len(plants.values())
      offsprings=0
      from sets import Set
      gametes = []
      for plant in plants.values():
        offspring = distributions.rbinom(parameters.offspring_size, plant.fitness())
        for _ in xrange(offspring): 
          gametes.append(plant.getGamete())  
        plant.die()
        offsprings+=offspring
      random.shuffle(gametes); 
      i = 0;
      while i + 1 < len(gametes) :
        g1 = gametes[i]
        g2 = gametes[i+1]
        g1.crossbreed(g2) #tak jak p.copy()
        i += 2
      self.gen+=1




class KillerRandom:
    def __init__(self, _intensity = None):
	self.parameter = _intensity
    def eliminate(self, plants):
	from saveableparams import parameters
	prob = parameters.random_pressure
	if self.parameter != None:
	    prob = self.parameter
	ret = 0
	for plant in plants:
	    if distributions.happened(prob):
		plant.die()
		ret += 1
	return ret



class KillerFitBasedStochastic:
    def __init__(self, _intensity = None, env = None):
	self.parameter = _intensity
	self.environment = env
	self.fallback = KillerRandom()
    def eliminate(self, plants):
	from saveableparams import parameters
#	global fitness_pressure
	prob = parameters.fitness_pressure
	if self.parameter != None:
	    prob = self.parameter
	avg_fitval = self.environment.default.average_fitness()
	maxfit = -1e100
	correction = 0.0
	for plant in plants:
	    maxfit = max(plant.fitness(), maxfit)
	for plant in plants:
	    correction += maxfit - plant.fitness()
	
	if correction == 0.0:
	    self.fallback.eliminate(plants)
	    return
	
	correction /= float(len(plants))*prob
	ret = 0
#	print "correction:", correction
	for plant in plants:
	    if distributions.happened((maxfit - plant.fitness()) / correction):
		plant.die()
		ret += 1
	return ret
		

class KillerIndependentFitBased:
    def __init__(self, _intensity):
	self.parameter = _intensity
    def eliminate(self, plants):
	ret = 0
	for plant in plants:
#	    print 1.0/(1.0-self.parameter*plant.fitness())
	    if distributions.happened(1.0/(1.0-self.parameter*plant.fitness())):
		plant.die()
		ret += 1
	return ret




class KillerIndependentFitBasedFlat:
    def eliminate(self, plants):
	from saveableparams import parameters
	ret = 0
	for plant in plants:
	    if not distributions.happened((-plant.fitness()/parameters.min_survival_fitness)+1.0):
		plant.die()
		ret += 1
	return ret


class KillerFitnessBased01:
# for cases where fitness: plants -> [0, 1]
# and defines the probability of surivival
    def eliminate(self, plants):
	ret = 0
	for plant in plants:
	    if not distributions.happened(plant.fitness()):
		plant.die()
		ret += 1
	return ret

class KillerNull:
    def eliminate(self, plants):
        return 0


def getSelectors():
    from saveableparams import parameters
    killer = None
    reproducer = None
    if parameters.killer == 'fitness_based_01':
	killer = KillerFitnessBased01()
    elif parameters.killer == 'null':
	killer = KillerNull()
    else:
	raise Exception("Invalid killer " + str(parameters.killer))
    
    if parameters.reproducer == 'fitness_based_default':
	reproducer = ReproducerFitnessBasedDefault()
    elif parameters.reproducer == 'fitness_based_merged':
	reproducer = ReproducerFitnessBasedMerged()
    elif parameters.reproducer == 'fitness_based_01':
	reproducer = ReproducerFitnessBased01()
    elif parameters.reproducer ==  'fitness_based_01_merged':
	reproducer = ReproducerFitnessBased01Merged()
    elif parameters.reproducer == 'random':
	reproducer = ReproducerRandom()
    elif parameters.reproducer == 'fitness_based_merged_unscaled':
	reproducer = ReproducerFitnessBasedMergedUnscaled()
    elif parameters.reproducer == 'everyone':
	reproducer = ReproducerEveryone()
    elif parameters.reproducer == 'everyone_sexual':
	reproducer = ReproducerEveryoneSexual()
    elif parameters.reproducer == 'location_mode_off':
	reproducer = ReproducerLocationModeOff()
    elif parameters.reproducer == 'everyone_sexual':
	reproducer = ReproducerEveryoneSexual()

    else:
	raise Exception("Invalid reproducer " + str(parameters.reproducer))


    return (killer, reproducer)
