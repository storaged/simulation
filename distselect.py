import distributions
try: 
    import numpypy
except ImportError:
    pass
import random
try:
    import numpy
except ImportError:
    try:
	import numpypy
	import numpy
    except ImportError:
	pass
from datetime import datetime as dt
from datetime import timedelta as td
from math import exp
import sys
import pickle
import os

#choices = {}

def rpois_numpy(l):
    return numpy.random.poisson(l)

def rpois_r(l):
    return int(r.rpois(1, l)[0])

def rpois_py(l):
#Normal approximation for large lambda
    if l > 20:
	return int(max(0.0, distributions.rnorm(l, l))+0.5)
#Knuth's algorithm for small ones
    if l == 0:
	return 0
    L = 2.71828182845 ** (-l)
    k = -1
    p = 1
    keeprunning = True
    while keeprunning:
	k = k+1
	p = p*distributions.runif(0.0, 1.0)
	if p < L:
	    keeprunning = False
    return k


def rbinom_numpy(size, prob):
    if size == 0:
	return 0
    else:
	return numpy.random.binomial(size, prob)

def rbinom_r(size, prob):
    return int(r.rbinom(1, size, prob)[0])

def rbinom_py(size, prob):
    if prob == 0.0:
	return 0
    # Normal approximation where reasonable
    if size * prob > 5.0 and size * (1.0-prob) > 5.0:
	norm = distributions.rnorm(size*prob, size*prob*(1.0-prob))
	return int(max(min(norm, size), 0.0))
    successes = 0
    tries = 0
    while tries < size:
        tries += 1
	if distributions.happened(prob):
	    successes += 1
    return successes

def runif_numpy(lower_bound, upper_bound):
#    ##KG ogolnie to co ponizej nie dziala, bo wyglada na to ze .uniform jest 
#       niezaimplementowane - SICK. Piszemy cos recznie
#    return numpy.random.uniform(lower_bound, upper_bound)
    return numpy.random.random() * abs(upper_bound - lower_bound) + lower_bound
def runif_py(lower_bound, upper_bound):
#    j/w
#    return random.uniform(lower_bound, upper_bound)
    return numpy.random.random() * abs(upper_bound - lower_bound) + lower_bound

def rnorm_numpy(mean, variance):
    return numpy.random.normal(mean, variance)

def rnorm_py(mean, variance):
    return random.gauss(mean, variance)

def rnorm_r(mean, variance):
    return float(r.rnorm(1, mean, variance)[0])

def pnorm_r(x, mean, variance):
    return float(r.pnorm(x, mean, variance)[0])



def erfcc(x):
    """Complementary error function."""
    z = abs(x)
    t = 1. / (1. + 0.5*z)
    r = t * exp(-z*z-1.26551223+t*(1.00002368+t*(.37409196+
        t*(.09678418+t*(-.18628806+t*(.27886807+
        t*(-1.13520398+t*(1.48851587+t*(-.82215223+
        t*.17087277)))))))))
    if (x >= 0.):
        return r
    else:
        return 2. - r

def pnorm_py(x, mean, stdev):
    return 1. - 0.5*erfcc(((x-mean)/stdev)/(2**0.5))

def runifint_numpy(start, end):
    return numpy.random.random_integers(start, end)

def runifint_py(start, end):
    return random.randint(start, end)

def rtnorm(start, end, mean, variance):
    ret = start - 1
    while ret < start or ret > end:
	ret = rnorm(mean, variance)
    return ret

def happened(likelihood):
    return runif(0,1) < likelihood


def seed_with(seed):
    random.seed(seed)
    numpy.random.seed(seed)
#    r['set.seed'](3)

def seed_with_default():
    seed_with(3)


def time_exec(fun, times, *args):
    start = dt.now()
    for i in xrange(times):
	x = fun(*args)
    end = dt.now()
    return end - start

def pick_fastest(fname, funs, times, *args):
    chosen = None
    fastest = td(10000000)
    print "Timing:"
    for fun in funs:
	print fun.__name__,
    print ""
    print "repetitions:", times

    for fun in funs:
      try:
	newtime = time_exec(fun, times, *args)
	print fun.__name__, "	", newtime
	if newtime < fastest:
	    chosen = fun
	    fastest = newtime
      except AttributeError, NameError:
          pass
#    globals()[target] = chosen
#    choices[target] = chosen.__name__
    if chosen == None:
	raise Exception("No working implementation found! None of: %s works" % str(funs))
    print "Chosen:", chosen.__name__
    distributions.__dict__[fname] = globals()[chosen.__name__]
    return chosen.__name__
    


def setup_with_choices(choices_set):
    def setup_fun(name):
	distributions.__dict__[name] = globals()[choices_set[name]]
    funs = ['rpois', 'rbinom', 'runif', 'rnorm', 'pnorm', 'runifint']
    for fun in funs:
	setup_fun(fun)
    random.seed(choices_set['random_seed'])
    try:
	numpy.random.seed(choices_set['random_seed_numpy'])
    except:
	pass
#    r['set.seed'](choices_set['random_seed_r'])

    
    

	
def get_fresh_choices():
    ch = {}
    ch['runif']    = pick_fastest('runif', [runif_py, runif_numpy], 1000, 0.0, 1.0)
    ch['rnorm']    = pick_fastest('rnorm', [rnorm_py, rnorm_numpy], 1000, 0.0, 1.0)
    ch['rpois']    = pick_fastest('rpois', [rpois_py, rpois_numpy], 1000, 5.0)
    ch['rbinom']   = pick_fastest('rbinom', [rbinom_py, rbinom_numpy], 1000, 20, 0.3)
#    ch['rnorm']    = pick_fastest('rnorm', [rnorm_py, rnorm_numpy], 1000, 0.0, 1.0)
    ch['pnorm']    = pick_fastest('pnorm', [pnorm_py], 1000, 1.0, 0.0, 1.0)
    ch['runifint'] = pick_fastest('runifint', [runifint_py, runifint_numpy], 1000, 0, 20)
    seed_upper_bound = min(2147483646, sys.maxint)
    ch['random_seed'] 		= random.randint(0, seed_upper_bound)
    ch['random_seed_numpy']	= random.randint(0, seed_upper_bound)
#    ch['random_seed_r']		= random.randint(0, seed_upper_bound)
    return ch

def get_default_choices():
    ch = {}
    ch['rpois']    = 'rpois_py'
    ch['rbinom']   = 'rbinom_py'
    ch['runif']    = 'runif_py'
    ch['rnorm']    = 'rnorm_py'
    ch['pnorm']    = 'pnorm_py'
    ch['runifint'] = 'runifint_py'
    ch['random_seed']           = 42
    ch['random_seed_numpy']     = 42
#    ch['random_seed_r']         = 42
    return ch



def load_run(filename):
    f = open(filename, "r")
    ch = pickle.load(f)
    f.close()
    return ch

c = get_default_choices()

def distr_init(filename = None, fast = False):
    global c
    if filename != None:
        c = load_run(filename)
    elif not fast:
	c = get_fresh_choices()

    setup_with_choices(c)

def save_run(filename):
    f = open(filename, "w")
    pickle.dump(c, f)
    f.flush()
    f.close()




