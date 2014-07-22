#from selectors import *
#from random import randint
#import plots
#import preparam
import distributions

# Parameters controlling transposition

# Probability that a given autonomous transposon will loose its ability to produce transposition
# machinery, and thus, will become nonautonomous.
# Valid values: [0.0, 1.0]
deauton_probability = 0.001

# Probability that a given nonautonomous transposon will become inactive ("fixed") during the 
# time of 1 generation. 
# Valid values: [0.0, 1.0]
inactivation_probability = 0.001

# Rate at which every active transposon will copy itself, assuming 1 unit 
# of transposing machinery is present in a given plant.
# Actual number of transposon copies 1 active transposon will produce is
# sampled from Poisson distribution: Pois(transposition_rate * transposition_machinery_available)
# Valid values: non-negative real numbers
transposition_rate = 0.001


# Rate at which new transposons invade genomes of plants.
# For each plant, during each generation the actual number of new transposons is sampled from Poisson 
# distribution: Pois(transposon_creation_rate)
# Valid values: non-negative real numbers
transposon_creation_rate = 0.0 #0.01

# Probability that a given transposition in plant's genome will NOT be lethal to host.
# Valid values: (0.0, 1.0]
nonlethal_transposition_likelihood = 1.0 #0.9999

# Probability that a given inactive transposon will be deleted from host genome during 1 generation.
# Valid values: [0.0, 1.0]
deletion_probability = 0.00001


# Probability that a transposition will result in duplication of a transposon
# Valid values: [0.0, 1.0]
duplicative_transposition_probability = 1.0


# Parameters controlling evolution process


# Number of phenotype properties each plant (and environment) has.
# Valid values: integers greater than 1
no_phenotype_properties = 10

# Expected value of fraction of plants eliminated randomly (due to events unrealted to fitness)
# in each generation
# Valid values: [0.0, 1.0)
random_pressure = 0.0


# Whether to use relative fitness function. If True, then only a fixed percentage of plants
# will be eliminated during each generation (and so, it will be harder for a plant with given fitness
# to survive in a well-adapted population than in a badly adapted one). If False, then the survival
# of plant is dependant only on its fitness function.
fitness_use_relative = False

# Expected value of fraction of plants eliminated during fitness-based selection process
# Valid values: [0.0, 1.0)
# Used only if fitness_use_relative is set to True
fitness_pressure = 0.9

# Fitness value at which a plant will have 0% chance of surival
# Used only if fitness_use_relative is set to False
min_survival_fitness = -20.0

# Rate at which random (non-transposition-related) mutations occur in plants.
# For each plant, in each generation, the actual number of mutations in is sampled 
# from Poisson distribution: Pois(random_mutation_rate)
# Valid values: non-negative real numbers
random_mutation_rate = 0.0


# Size of the environment: during each generation plants will multiply to fill it
# Valid values: positive integers
niche_size = 5000




# Parameters controlling optimal phenotype drift

# These actions will be performed IN ADDITION to any actions defined below, in env_changes
# function

# Number of initial generations during which the environment will stay stable (no mutations of 
# optimal phenotype will happen before that generation):
stability_period = 0

# After the stability period passes, number of mutations performed on optimal phenotype
# (a single mutation changes one parameter of optimal phenotype) during each generation:
# These will be cumulative and cause optimal phenotype to drift
number_of_mutations = 0

# Expected change of a parameter during a mutation
expected_mutation_shift = 0.0

# Controls whether the drift of optimal phenotype will be directed or purely random
# Valid values: True, False
is_drift_directed = True

# Controls the magnitude of non-cumulative fluctuations of optimal phenotype in each generation
fluctuations_magnitude = 0.0



# Parameters contolling initial population



# Function returning number of transposons a plant in a random population will have.
# Can be a fixed number, or a random integer.
# Must return a non-negative integer.
def starting_transposons():
    return 1 # Each plant will have 20 transposons
# Other examples:
#    return distributions.rpois(20) # random sample from Poisson distribution with rate parameter = 20



# Amount of transposon machinery in a plant in initial population. Takes as an 
# argument the number of transposons that plant has.
# Given a non-negative integer must return a non-negative real number.
def starting_transposase_activity(number_of_transposons):
    return number_of_transposons # Each plant will have its transposon machinery linearly dependent on starting number of transposons
# Other examples:
#    return runif(0.0, 5.0) # Each plant will have a random amount of transposition machinery, between 0.0 and 5.0
#    return runif(0.0, 0.5) * number_of_transposons



# Standard deviation of plant's initial phenotype parameter values. The higher, the more scattered the plants will be 
# around the optimal phenotype. Choose 0.0 for a starting population of ideally-adapted plants.
initial_phenotype_stdev = 0.1



# Parameters controlling transpositiom machinery


# Change in transposition machinery activity in one plant during one generation:
# Arguments are:
# previous_transp_activ - activity of transposon machinery in plant before change, a non-negtive real number
# no_new_transp - number of new transposon insertions in this generation, a non-negative integer
# no_transp_deleted - number of deactivated active transposons in this generation, a non-negative integer
# no_transp_remaining - number of remaining transposons after insertions and deactivations in a plant
# Given those arguments must return a non-negative integer
def get_transposase_change(previous_transp_activ, no_new_transp, no_transp_deleted, no_transp_remaining):
     return no_transp_remaining #previous_transp_activ  + 0.3*(no_new_transp - no_transp_deleted)
#    return previous_transp_activ * runif(0.5, 1.3) + 0.3*no_new_transp # unaffected by transposition or deletion events; just multiplied by random number from between 0.5 and 1.3



# Other parameters

# This function describes the mutation of phenotypes due to transposon insertion events and random mutations.
# For each such event one phenotype parameter is chosen, and a random number generated from normal distribution with standard deviation
# given below is added to it.
mutation_stdev = 0.1


# Fitness function. Diven distance of a plant from optimal phenotype (a non-negative real number) must return the value of such plant's fitness.
# The function must be deterministic (that is, repeated calls with the same argument must yield the same value, thus, random distributions should not
# be used in it). It should also be monotonically non-increasing.
def fitness_function(distance):
#     return max(0.0, -distance + 10.0)
#     return 1.0/(1.0+distance)
     return -distance



# Disregard that...
reproducer = ReproducerDefault()


model = ['meteor', 'globalwarmingnum', "globalwarmingint", 'fluctuations', 'domestication', 'twometeors', 'threemeteors', 'cdomesticationnum', 'cdomesticationint']
pint = [0, 1, 2, 3, 4, 5]
run_no = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# This function is called after every generation.
# Parmeters are: i - number of generation
# env - Environment object which can be modified
# should not return a value
def env_changes(i, env):
    from saveableparams import parameters
    def meteorhit(intensity):
	for pos in range(len(env.optimal_phenotype.properties)):
	    env.optimal_phenotype[pos] += float(intensity)
# Examples:
#-------------------------------
# # Do nothing
    if i == 1:
	if parameters.model == 'meteor' or parameters.model == 'threemeteors' or parameters.model == 'twometeors':
	    meteorhit(float(parameters.pint)*0.4)
	elif parameters.model == 'globalwarmingnum':
	    parameters.number_of_mutations = parameters.pint * 2
	    parameters.expected_mutation_shift = 0.002
	elif parameters.model == 'globalwarmingint':
	    parameters.number_of_mutations = 2
	    parameters.expected_mutation_shift = 0.002 * float(parameters.pint)
	elif parameters.model == 'fluctuations':
	    parameters.fluctuations_magnitude = float(parameters.pint)*0.2
	elif parameters.model == 'noselection':
	    parameters.min_survival_fitness = -100000000000
	elif parameters.model == 'stable':
	    pass
	elif parameters.model == 'domestication':
	    parameters.fitness_use_relative = True
	    meteorhit(float(parameters.pint)*0.4)
	elif parameters.model == 'cdomesticationnum':
	    parameters.fitness_use_relative = True
	    parameters.number_of_mutations = parameters.pint * 2
	    parameters.expected_mutation_shift = 0.002
	elif parameters.model == 'cdomesticationint':
	    parameters.fitness_use_relative = True
	    parameters.number_of_mutations = 2
	    parameters.expected_mutation_shift = 0.002 * float(parameters.pint)
    if i == 2000 and parameters.model == 'twometeors':
        meteorhit(float(parameters.pint)*0.4)
    if (i == 1000 or i == 2000) and parameters.model == 'threemeteors':
        meteorhit(float(parameters.pint)*0.4)

# -------------------------------
# # Perform slight perturbations of optimal phenotype in each generation
#    position = randint(0, no_phenotype_properties-1) # Pick a random integer between 0 and no_phenotype_properties-1, it will be the number of property to be modified
#    env.optimal_phenotype[position] += distributions.rnorm(0.0, 0.1) # Modify ith property of optimal phenotype by adding 
#                                                       # a random number drawn from normal distibution with mean = 0.0 and stdev = 0.1 to it
#--------------------------------
# # In 2000th generation drastically alter the environment by adding 5.0 to first 10 parameters of optimal phenotype
# # Note: it will cause the program to crash if no_phenotype_properties < 10
#    if i == 2000:
#	for position in range(0, 9):
#	    env.optimal_phenotype[position] += 5.0
#--------------------------------
# # In 400th generation save all current plots to a file named: plots.pdf
#     if i == 400:
#	plots.save_all(env, "plots.pdf")
#--------------------------------
# In every tenth generation insert 10 plants with number of transposons and transposase activity equal to
# chosen above initial values
#    if i % 10 == 0:
#	for _unused in range(1,10):
#	    plants.Plant()
#--------------------------------
# In 100th generation add 20 active transposons to every plant:
#     for plant in env.plants.values():
#	plant.active_transposons += 20




#----------------------------------------------------------------------------------------------------------------------
# The following parameters don't affect the model in any way


# Controls how often plots will be redrawn 
# If set to 1 then plots will be redrawn every 1 generation (VERY slow!)
# If set to 100 then plots will be redrawn every 100 generations (resonable)
# A special value of 0 means that plots will not be drawn at all unless requested from command line
plotting_frequency = 0


#---------------------------------------
# Controls whether we will use headless (not requiring X11 display) mode.
headless_mode = True

# Controls whether the data necessary for plotting heatmaps will be collected
# Beware, it's quite a memory hog!
heatmaps_enabled = False


draw_legends = False

import postparam

