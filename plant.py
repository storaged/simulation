import distributions, debug
import random
from saveableparams import parameters as p
from table_util import table
from phenotype import Phenotype
from environment import Environment
from transposone import Transposone
import math
import pdb
    
##sample with replacement
def sample_wr2(population, k):
        n = len(population)
        _random, _int = random.random, int
        result = [None] * k
        for i in xrange(k):
            j = _int(_random() * n)
            result[i] = population[j]
        return result

def sample_wr(population, k):
    if len(population) > 0 :
        result = []
        for i in range(k):
            result.append(random.choice(population))
        return result
    return []
#----------------------------------------------------------------------------------------------------
class Plant:
    counter = 0
    order_cnt = 0

    @staticmethod
    def scale(x): 
        return int((x+1.)*Environment.default.mesh_size/2.)
    def scalex(self):
        return Plant.scale(self.location[0])
    def scaley(self):
        return Plant.scale(self.location[1])
    
    
    def __init__(self, no_transp = None, transp_activity = None):
        #debug.g("tworzenie nowej rosliny c.d. __init__()" )#, plant.fitness()))
        self.aut_transposons = no_transp
        if no_transp == None:
            self.aut_transposons = p.starting_transposons()
        self.nonaut_transposons = 0

        ##KG--begin
        ##sexual_mode reproduction
        ##initializing a list of transposons in a new plant
   
        if p.sexual_mode : 
            self.sex = 1 if random.random() > 0.5 else 0
            self.nonaut_transposons_list = []
            self.aut_transposons_list = []
            for i in range(self.aut_transposons):
                te = Transposone(True)
                self.aut_transposons_list.append(te) 
        else :
            # asexual all plants have sex=0
            self.sex = 0
        ##KG--end
        
        self.phenotype = Phenotype.new()
        self.id = self.__class__.counter
        #Environment.default.register_new_plant(self.id, self) replaced to new()
        self.environment = Environment.default
        self.dead = False
        self.__class__.counter += 1
        self.transposase_activity = transp_activity
        if transp_activity == None:
            self.transposase_activity = p.starting_transposase_activity(self.aut_transposons)
        self.inactive_transposons = 0
        self.transpositions = 0
        self.total_mutations = 0
        self.random_mutations = 0
        self.ord_counter = self.__class__.order_cnt
        self.__class__.order_cnt += 1
    
    @staticmethod
    def new(parent_location, no_transp = None, activity = None):
        #debug.g("tworzenie nowej rosliny new()")
        plant = Plant()
        if no_transp == None:
            no_transp = p.starting_transposons()
        if activity == None:
            activity = p.starting_transposase_activity(no_transp)
        plant.aut_transposons = no_transp
        #plant.transposase_activity = activity
        plant.transposase_activity = no_transp

        #===============
        #=======LOCATION
        #debug.g("%d" % (p.location_mode))#, plant.fitness()))
        if p.location_mode:
            x_parent = parent_location[0]
            y_parent = parent_location[1]
            while(True):
                r_new = abs(distributions.rnorm(0., p.birth_range))
                angle_new =  distributions.runif(0.,math.pi*2)
                x_new = x_parent+r_new*math.cos(angle_new)
                y_new = y_parent+r_new*math.sin(angle_new)

                f = lambda x, bound: (-bound<x and x<bound)
                if f(x_new, p.x_bound(p.maps)) and f(y_new, p.y_bound(p.maps)):
                    plant.location = (x_new, y_new)
                    Environment.default.register_new_plant(plant.id, plant)
                    break
                else: 
                    if p.sow_seed_type == 'island':
                        plant.die(False) #seed out of space
                        break
                    elif p.sow_seed_type == 'valley': pass
                    elif p.sow_seed_type == 'settlers1': 
                        def g(v):
                            if  v<-1: return g(v+2)
                            elif v>1: return g(v-2)
                            else: return v
                        plant.location = (g(x_new), g(y_new))
                        Environment.default.register_new_plant(plant.id, plant)
                        break
        #===============
        #===============
        else :
            Environment.default.register_new_plant(plant.id, plant)

        return plant

    def die(self, unregister=True):
        self.dead = True
        #debug.g("id to be removed = %d " % self.id)
        if(unregister): Environment.default.unregister_plant(self.id)


    #######################################################
    #                                                     #
    # Main function of Plant class describing TE activity #
    #                                                     #
    #######################################################
    def evolve(self):
    #   global inactivation_probability
    #   global transposition_probability
    #   global random_mutation_rate
    #   global transposon_creation_probability

        self.transpositions = 0

    # Autonomous transposon activity

        if self.aut_transposons > 1000000 or self.nonaut_transposons > 1000000:
        # this plant definitely wouldn't survive anyway, but causes technical problems and crashes if we let her pass this point...
            self.die()
            return

        # tranpozony ktore ulegly deautonomizacji
        # tj okreslamy liczbe transpozonow, ktore staly sie nieautonomiczne
        no_aut_decayed = distributions.rbinom(self.aut_transposons, p.deauton_probability)

        
        ##KG: I assume the following meaning of variables
        ##no_aut_decayed - no. autonomous TEs that became non-autonomous
        ##  thus are moved to list on non-aut TEs 
        ##no_aut_fixed - no. autonomous TEs that lost their functionality 
        ##  thus are deleted permanently  
        ##KG: changes is the lists of TEs
        ##I choose no_aut_decayed TEs randomly from aut_list and move them

        new_nonaut_list = []

        if p.sexual_mode:
            # wybieramy ktore staja sie nieautonomiczne
            which_aut_decayed = random.sample(range(self.aut_transposons), no_aut_decayed)
        
            # jezeli jest cokolwiek do zrobienia
            if len(which_aut_decayed) > 0 :

                #new_nonaut_list = []
                tmp_aut_list = []
                idx_decayed, idx_aut = 0, 0
                
                # sortujemy indeksy ktore nalezy przeniesc
                which_aut_decayed.sort()
                
                # sprawdzamy kolejno wszystkie transpozony i przenosimy te ktore sa pod indeksami z which_aut_decayde
                for x in range(self.aut_transposons) :
                    
                    # do przeniesienia
                    if idx_decayed < len(which_aut_decayed) and idx_aut == which_aut_decayed[idx_decayed] :
                        new_nonaut_list.append(self.aut_transposons_list[idx_aut])
                        idx_decayed += 1
                    else : 
                        tmp_aut_list.append(self.aut_transposons_list[idx_aut])
                    idx_aut += 1

                # zapisujemy nowy stan listy
                self.aut_transposons_list = tmp_aut_list
      
        # obecnie mamy tmp_aut_te TE autonomicznych na liscie
        tmp_aut_te = self.aut_transposons - no_aut_decayed


        # wybieramy ile transpozonow ulega calkowitej dezaktywacji, tzn zanikaja z systemu a ich wklad fenotypowy
        # na stale modyfikuje fenotyp hosta 
        no_aut_fixed = distributions.rbinom(tmp_aut_te, p.inactivation_probability)
       
        ##KG
        ##I choose no_aut_fixed TEs randomly to remove them from list
        ##which_aut_fixed = random.sample(range(tmp_aut_te), no_aut_fixed).sort()
        if p.sexual_mode :

            try:
                if tmp_aut_te != len(self.aut_transposons_list):
                    import sys
                    debug.g("length of list does not equal to variable value")
                    raise AssertionError("aut_list len != no_aut")
                    sys.exit(1)
                else:

                    # if there is anything to do
                    if no_aut_fixed > 0 :

                        which_aut_fixed = random.sample(range(tmp_aut_te), no_aut_fixed)
                        idx_aut, fixed_idx = 0, 0
                        tmp_aut_list2 = []
                        
                        which_aut_fixed.sort()

                        # przegladamy liste wszystkich transpozonow
                        while fixed_idx < len(which_aut_fixed) and idx_aut < tmp_aut_te :
                            
                            # jezeli trafiamy na numer ktory ulega dezaktywacji
                            if idx_aut == which_aut_fixed[fixed_idx]:
                                
                                # zapamietujemy transpozon i zapisujemy jego zmiane na stale
                                te_to_fix = self.aut_transposons_list[idx_aut]
                                if p.multidim_changes:
                                    pass#TODO
                                else:
                                    #add the change from TE to the base phenotype
                                    self.phenotype[te_to_fix.trait_no] += te_to_fix.mutation_rate
                                    fixed_idx += 1
                            else :
                                tmp_aut_list2.append(self.aut_transposons_list[idx_aut])
                            idx_aut += 1

                        self.aut_transposons_list = tmp_aut_list2

                #self.aut_transposons_list = random.sample(self.aut_transposons_list, self.aut_transposons - no_aut_decayed - no_aut_fixed)
                
                #self.aut_transposons_list.sort()
            except ValueError:
                import sys
                debug.g('SHIT FUCK, HOW ?!')
                debug.g(self.aut_transposons_list)
                numbb =  self.aut_transposons - no_aut_decayed - no_aut_fixed
                debug.d("choose = %d" % numbb)
                sys.exit(0)
        
        ###### len(aut) = self.aut.te - decayed - fixed

        no_aut_deleted = no_aut_fixed + no_aut_decayed

        #print "po usunieciach aut"
        #print "aut list dlug. > " + str(len(self.aut_transposons_list))
        #print "aut ile > " + str(self.aut_transposons)

        no_new = None
        if p.autonomous_transp_dynamics == 'linear':
            no_new = distributions.rpois(p.transposon_creation_rate + (self.aut_transposons - no_aut_deleted) * p.transposition_rate)
        elif p.autonomous_transp_dynamics == 'square':
            no_new = distributions.rpois(p.transposon_creation_rate + (self.aut_transposons - no_aut_deleted) * p.transposition_rate * (self.aut_transposons - no_aut_deleted))
        elif p.autonomous_transp_dynamics == 'old':
            no_new = distributions.rpois(p.transposon_creation_rate + (self.aut_transposons - no_aut_deleted) * p.transposition_rate * self.transposase_activity)
        else: 
            raise Exception("autonomous_transp_dynamics parameter must be one of: 'linear', 'square', 'old', and not: " + str(p.autonomous_transp_dynamics))

        self.transpositions += no_new
        non_duplicative = 0
        if p.duplicative_transposition_probability != 1.0:
            non_duplicative = distributions.rbinom(no_new, 1.0 - p.duplicative_transposition_probability)
            no_aut_deleted += non_duplicative


        ##KG: 
        ##we append no_new - non_duplicative TEs that has appeared

        ### THIS IS PROBABLY THE SHITTEST CODE EVER PRODUCED BY HUMAN... I will improve it one day
        if p.sexual_mode: 
            
            which_to_copy = sample_wr(range(self.aut_transposons - no_aut_fixed - no_aut_decayed), no_new - non_duplicative)
                
            # powstaly nowe TE narodzone z niczego
            if no_new - non_duplicative > 0 and (self.aut_transposons - no_aut_fixed - no_aut_decayed) == 0 :
                for i in range(no_new - non_duplicative):
                    te = Transposone(True)
                    #self.phenotype.TE_driven_mutation(te.mutation_rate)
                    self.aut_transposons_list.append(te)

            # powstaly TE zarowno przez kopiowanie jak i nowonarodzone
            elif no_new - non_duplicative > 0 and (self.aut_transposons - no_aut_fixed - no_aut_decayed) > 0 :
                tmp_no_new = distributions.rpois(p.transposon_creation_rate)
                # ilosc nowo powstalych
                if tmp_no_new > 0 : 
                    tmp_no_new = min(tmp_no_new, no_new - non_duplicative)
                    for i in range(tmp_no_new):
                        te = Transposone(True)
                        #self.phenotype.TE_driven_mutation(te.mutation_rate)
                        self.aut_transposons_list.append(te)
                    for i in range(no_new - non_duplicative - tmp_no_new):
                        parent_id = self.aut_transposons_list[which_to_copy[i]].id
                        #parent_mut = self.aut_transposons_list[i].mutation_rate
                        #self.phenotype.TE_driven_mutation(parent_mut)
                        te = Transposone(True, parent_id)
                        self.aut_transposons_list.append(te)
                # kopiowane
                else:
                    for i in which_to_copy:
                        parent_id = self.aut_transposons_list[i].id
                        #parent_mut = self.aut_transposons_list[i].mutation_rate
                        #self.phenotype.TE_driven_mutation(parent_mut)
                        te = Transposone(True, parent_id)
                        self.aut_transposons_list.append(te)

    
        #self.transposase_activity = p.get_transposase_change(self.transposase_activity, no_new, no_deleted, self.aut_transposons)
        self.transposase_activity = self.aut_transposons
        
        # OSTATECZNA liczba transpozonow autonomicznych         
        self.aut_transposons +=  no_new - no_aut_deleted
        if p.sexual_mode:
            if self.aut_transposons != len(self.aut_transposons_list) :
                kur  = len(self.aut_transposons_list)
                debug.g("number = %d" % self.aut_transposons)
                debug.g("while list size = %d" % kur)
                raise AssertionError("aut_list len != no_aut")
 

        #
        # OBLUSGA NIEAUTONOMICZNYCH
        #
        # liczba nowych transpozonow nieautonomicznych, ktore powstaly z autonomicznych
        new_nonautonomous = no_aut_decayed

        # Non-autonomous transposon activity
        #t = self.nonaut_transposons
        no_deleted = distributions.rbinom(self.nonaut_transposons, p.inactivation_probability) 
        no_deleted_tmp = no_deleted
        ##KG
        ##I choose no_deleted nonaut TEs randomly to remove them from list
        if p.sexual_mode:
            #o ile cokolwiek jest do zrobienia
            if no_deleted > 0 :
                
                which_nonaut_deleted = random.sample(range(self.nonaut_transposons), no_deleted)
                idx_nonaut, deleted_idx = 0, 0
                tmp_nonaut_list2 = []
                which_nonaut_deleted.sort()

                # looking through all transposons
                while deleted_idx < len(which_nonaut_deleted) and idx_nonaut < self.nonaut_transposons :

                    # transpozon do usuniecia. Zmieniamy baze fenotypu i przesuwamy sie do nastepnej pozycji
                    if idx_nonaut == which_nonaut_deleted[deleted_idx]:

                        te_to_delete = self.aut_transposons_list[idx_nonaut]
                        if p.multidim_changes:
                            pass    #TODO
                        else:
                            #add the change from TE to the base phenotype
                            self.phenotype[te_to_delete.trait_no] += te_to_fix.mutation_rate
                        deleted_idx += 1

                    # nieciekawy przypadek, przenosimy te na nowa liste
                    else:
                        # transpozon zostaje w miejscu
                        tmp_nonaut_list2.append(self.nonaut_transposons_list[idx_nonaut])
                    # przesuniecie po kazdym przypadku na liscie nonaut
                    idx_nonaut += 1

                #zapisujemy nowowybrane nonaut
                self.nonaut_transposons_list = tmp_nonaut_list2

            #self.nonaut_transposons_list = random.sample(self.nonaut_transposons_list, self.nonaut_transposons - no_deleted)

        # liczba nowych nieautonomicznych zalezna od ilosci autonmicznych
        no_new = distributions.rpois((self.nonaut_transposons - no_deleted) * p.transposition_rate * self.transposase_activity)
        self.transpositions += no_new
        if p.duplicative_transposition_probability != 1.0:
            non_duplicative = distributions.rbinom(no_new, 1.0 - p.duplicative_transposition_probability)
            no_deleted += non_duplicative

        ##KG: 
        ##we append no_new - non_duplicative nonaut TEs that has appeared
        if p.sexual_mode:
           
            # watpliwe miejsce - na poczatku przeciez i tak nie mamy nieautonomicznych chyba
            which_to_copy_2 = sample_wr(range(self.nonaut_transposons - no_deleted_tmp), no_new - non_duplicative) 
            if self.nonaut_transposons == 0 :
                for i in which_to_copy_2 :
                    te = Transposone(False)
                    self.nonaut_tranposons_list.append(te)

            else :
                for i in which_to_copy_2 :
                    parent_id = self.nonaut_transposons_list[i].id
                    #parent_mut = self.nonaut_transposons_list[i].mutation_rate
                    #self.phenotype.TE_driven_mutation(parent_mut)

                    te = Transposone(False, parent_id)
                    #POST-transposition change
                    #self.phenotype.TE_driven_mutation(te.mutation_rate)
                    self.nonaut_transposons_list.append(te)
            
                ##append TEs that became nonaut in this round
            self.nonaut_transposons_list += new_nonaut_list
        ######

        self.nonaut_transposons = self.nonaut_transposons + no_new - no_deleted + new_nonautonomous
        new_inactive = no_deleted

        # Inactive transposon accumulation and decay
        self.inactive_transposons += new_inactive
        self.inactive_transposons -= distributions.rbinom(self.inactive_transposons, p.deletion_probability)
    

        # Impact of transpositions on plant
        # self.transposase_activity = p.get_transposase_change(self.transposase_activity, no_new, no_deleted, self.aut_transposons)

        #Environment.default.transpositions_in_this_generation += transpositions
        #############################
        ## PHENOTYPE CHANGES BLOCK ##
        #############################
        survival_likelihood = p.nonlethal_transposition_likelihood**self.transpositions
        if(not distributions.happened(survival_likelihood)):
            self.die()
        else:
            #self.phenotype.mutate(self.transpositions, stdev = p.transposition_mutation_stdev)
            tmp_mut = distributions.rpois(p.random_mutation_rate)
            self.phenotype.mutate(tmp_mut, stdev = p.non_transposition_mutation_stdev)
            self.total_mutations = tmp_mut + self.transpositions
            self.random_mutations = tmp_mut

    
    def perform_horizontal_transfer(self, destination):
        if self.aut_transposons == 0 and self.nonaut_transposons == 0:
            return
        print("horizontal transfer ?")
        which_te = distributions.runifint(0, self.aut_transposons+self.nonaut_transposons-1)
        if which_te < self.aut_transposons:
            print("horizontal transfer ?")
            self.aut_transposons -= 1
            destination.aut_transposons += 1
        else:
            print("horizontal transfer ?")
            self.nonaut_transposons -= 1
            destination.nonaut_transposons += 1

    def perform_horizontal_transfers(self):
        how_many = distributions.rpois(p.expected_horiz_transfers)
        pl = len(self.environment.allplantslist)
        for _ in xrange(how_many):
            to_whom = self.environment.allplantslist[distributions.runifint(0, pl-1)]
            self.perform_horizontal_transfer(to_whom)
   
    # SEXUAL REPRODUCTION BASE
    def getGamete(self):
        from gamete import Gamete
        i = 0;
        aut_TE = [];
        while i < len(self.aut_transposons_list) : 
            if (i+1) < len(self.aut_transposons_list) and self.aut_transposons_list[i] == self.aut_transposons_list[i+1] :
                aut_TE.append(self.aut_transposons_list[i])
                i += 1
            elif random.random() > 0.5 :
                aut_TE.append(self.aut_transposons_list[i])
            i += 1
        
        i = 0;
        nonaut_TE = [];
        while i < len(self.nonaut_transposons_list) : 
            if (i+1) < len(self.nonaut_transposons_list) and self.nonaut_transposons_list[i] == self.nonaut_transposons_list[i+1] :
                nonaut_TE.append(self.nonaut_transposons_list[i])
                i += 1
            elif random.random() > 0.5 :
                nonaut_TE.append(self.nonaut_transposons_list[i])
            i += 1

        return Gamete(aut_TE, nonaut_TE, self)

    def copy(self):
        if p.location_mode: 
            pl = Plant.new(self.location, self.aut_transposons, self.transposase_activity)
        else:
            pl = Plant.new((0,0), self.aut_transposons, self.transposase_activity)
        pl.inactive_transposons = self.inactive_transposons
        pl.phenotype = self.phenotype.copy()
        pl.ord_counter = self.ord_counter
    
        ##KG 
        ##we need to copy lists of transposons
        ## version 1.
        ## asexual_mode
        ##p.aut_transposons = self.aut_transposons
        ##p.nonaut_transposons = self.nonaut_transposons
        ##p.aut_transposons_list = self.aut_transposons_list[:]
        ##p.nonaut_transposons_list = self.nonaut_transposons_list[:]
        if p.sexual_mode:
            ## coin toss for each transposone
            tmp_aut = []
            for te in self.aut_transposons_list :
                if random.random() > 0.5 : 
                    tmp_aut.append(te)
                if random.random() > 0.5 : 
                    tmp_aut.append(te)
    
            pl.aut_transposons_list = tmp_aut[:]
            pl.aut_transposons = len(p.aut_transposons_list)
            
            tmp_nonaut = []
            for te in self.nonaut_transposons_list :
                if random.random() > 0.5 : 
                    tmp_nonaut.append(te)
                if random.random() > 0.5 : 
                    tmp_nonaut.append(te)
     
            pl.nonaut_transposons_list = tmp_nonaut[:]
            pl.nonaut_transposons = len(p.nonaut_transposons_list)
    
            return pl
        else:
            pl.aut_transposons = self.aut_transposons
            pl.nonaut_transposons = self.nonaut_transposons
            return pl
 

    def fitness(self):
        #optimal_ph = 1410
        #if p.location_mode:
        #    optimal_ph = Environment.default.optimal_phenotype_on_map(self.location)
        #else: 
        #    optimal_ph = self.optimal_global_phenotype.get_phenotype_without_map()
        #return p.fitness_function(Phenotype.distance(self.phenotype, optimal_ph))
        return p.fitness_function(self.distance_to_opt())

    def distance_to_opt(self):
        #magic trick by @MKitlas
        optimal_ph = 1410
        plant_ph = self.phenotype

        if p.location_mode:
            optimal_ph = Environment.default.optimal_phenotype_on_map(self.location)
        else:
            optimal_ph = Environment.default.optimal_phenotype_without_map()
        
        # TODO sum up TEs effect.
        for t in self.aut_transposons_list:
            if p.multidim_changes:
                plant_ph = Phenotype.add(plant_ph, t.mutation_rate)
            else:
                plant_ph[t.trait_no] += t.mutation_rate

        for t in self.nonaut_transposons_list:
            if p.multidim_changes:
                plant_ph = Phenotype.add(self.phenotype, t.mutation_rate)
            else:
                plant_ph[t.trait_no] += t.mutation_rate

        return Phenotype.distance(plant_ph, optimal_ph)
        #TODO to powinno inaczej dzialac dla modeli przestrzennych
        #return Phenotype.distance(self.phenotype, self.environment.optimal_phenotype_on_map(self.location))

    def total_transposons(self):
        return self.inactive_transposons + self.aut_transposons + self.nonaut_transposons



