import misc
from saveableparams import parameters

def history_plot(e):
    e.history.plot(params = ["avg aut transposons", "avg nonaut transposons", "avg inactive transp", "avg fitness", "avg transpositions", "avg distance between plants", "max fitness"])

def history_plot2(e):
    e.history.plot(params = ["avg fitness", "avg distance between plants", "max fitness", "avg prob of beneficial mutation from TE insertion"])



def parameter_density_plot(e, param_nr):
    caption = "Parameter density plot, parameter: " + str(param_nr)
    vals = map(lambda plant: plant.phenotype.properties[param_nr], e.plants.values())
    rvals = robjects.FloatVector(vals)
    r.plot(r.density(rvals), main=caption, xlim=r.c(-5, 5), ylim=r.c(0,1))
    r.abline(v=e.optimal_phenotype.properties[param_nr], col="yellow")

def scatter_plot(e, param_nr1, param_nr2):
    caption = "Scatter plot, parameters: " + str(param_nr1) + ", " + str(param_nr2)
    vals1 = map(lambda plant: plant.phenotype.properties[param_nr1], e.plants.values())
    vals2 = map(lambda plant: plant.phenotype.properties[param_nr2], e.plants.values())
    transps = map(lambda plant: float(plant.aut_transposons), e.plants.values())
    transpmax = float(reduce(lambda x, y: max(x, y), transps, 0) + 1)
    def clip(x):
        return max(0.0, min(1.0, x))
    collist_red = robjects.FloatVector(map(lambda trnum: clip(trnum/transpmax), transps))
    collist_blue = robjects.FloatVector(map(lambda trnum: clip((transpmax - trnum)/transpmax), transps))
    colours = r.rgb(collist_red, 0, collist_blue)
    rvals1 = robjects.FloatVector(vals1)
    rvals2 = robjects.FloatVector(vals2)
    r.plot(rvals1, rvals2, main=caption, xlim=r.c(-10, 10), ylim=r.c(-10,10), xlab="", ylab="", col = colours)
    r.points(e.optimal_phenotype.properties[param_nr1], e.optimal_phenotype.properties[param_nr2], col="yellow", pch=16)


def outlier_value(hd, perc = 0.05):
    l = []
    for y in xrange(hd.ydim):
	for x in xrange(hd.xdim):
	    if hd[x, y] > 0:
		l.append(hd[x, y])
    l.sort()
    if len(l) == 0:
	return hd[0,0]
    return l[ int(float(len(l)-1) * (1.0-perc)) ]

def cutoff_value(hd, perc = 0.05, mul = 5):
     ov = outlier_value(hd, perc)
     maxl = 1
     ov = ov*mul
     for y in xrange(hd.ydim):
         for x in xrange(hd.xdim):
	     if hd[x, y] <= ov:
	         maxl = max(maxl, hd[x, y])
     return maxl



def heatmap_plot(e, param_name):
    hd = e.history.heatmaps[param_name]
    hd.prepare_for_drawing()
    v = []
    outval = cutoff_value(hd)
    for y in xrange(hd.ydim):
	for x in xrange(hd.xdim):
	    v.append(min(outval, hd[x, y]))
#    rprint = r['print']
    m = r.matrix(robjects.FloatVector(v), hd.xdim, hd.ydim)
    c = r('c("white", rev(rainbow(100000)[1:80000]))')
    iv = r('1:'+str(hd.xdim+1))#robjects.IntVector(range(1, hd.xdim+1))
    ivv = robjects.IntVector(range(1, hd.ydim+1))
    hd.done_drawing()
    r['image.plot'](iv, ivv, m, col=c, main=hd.title, xlab=" ", ylab=" ")


def histogram_plot(e, param_name):
    hd = e.history.heatmaps[param_name]
    hd.prepare_for_drawing()
    xvals = []
    yvals = []
    mmax = -100000000000000000000000
    mmin = 1000000000000000000000000
    outval = cutoff_value(hd)
    for y in xrange(hd.ydim):
	for x in xrange(hd.xdim):
	    if outval >= hd[x, y] >= 0:
		xvals.append(x)
		yvals.append(hd[x, y])
		mmax = max(mmax, hd[x, y])
		mmin = min(mmin, hd[x, y])
    hd.done_drawing()
    rx = robjects.FloatVector(xvals)
    norm = lambda y: (float(y)-float(mmin))*float(mmax-mmin+1)/float(mmax-mmin)+float(mmin)
#    norm = float(mmax-mmin+1)/float(mmax-mmin)
    ry = robjects.FloatVector([norm(y) for y in yvals])
    def riv(x):
       return robjects.IntVector(x)

    bins = riv([hd.xdim, int(mmax)-int(mmin)+1])

    r['hist2d'](rx, ry, nbins=bins, col=r('c("white", rev(rainbow(100000)[1:80000]))'))


def histogram_plot2(e, param_name, nbins = 1000):
    hd = e.history.heatmaps[param_name]
    hd.prepare_for_drawing()
    outval = cutoff_value(hd)
    outval += 10
    overlimit = False
    if outval > nbins:
	overlimit = True
    else:
	nbins = int(outval)
    fnbins = float(nbins)
#    print "oval: ", outval
    M = [[0 for col in xrange(nbins+1)] for row in xrange(hd.xdim)]
    for y in xrange(hd.ydim):
        for x in xrange(hd.xdim):
	    if hd[x, y] >= 0:
	        if hd[x, y] >= outval:
#		    M[x][outval] += 1
		    pass
		else:
#		    print "x: ",x, "	y: ",y, "	hd[x,y]: ", hd[x, y], "	len(M): ", len(M), "	len(M[0]): ", len(M[0])
	            M[x][int(float(hd[x, y])*nbins/outval)] += 1
    FlatM = []
    hd.done_drawing()
    for y in xrange(len(M[0])):
        for x in xrange(len(M)):
	    FlatM.append(M[x][y])
    RM = r.matrix(robjects.FloatVector(FlatM), len(M), len(M[0]))

    iv = r('1:'+str(len(M)+1))
    ivv = r('0:'+str(nbins)+'*'+str(outval/nbins))
    robjects.FloatVector(range(0, nbins+1))
    c = r('c("white", rev(rainbow(100000)[1:80000]))')
    r['image.plot'](iv, ivv, RM, col=c, main=hd.title, xlab=" ", ylab=" ")



def histogram_plot_fitness(e, param_name):
    hd = e.history.heatmaps[param_name]
    hd.prepare_for_drawing()
    lower = float(parameters.min_survival_fitness)
    M = [[0 for col in xrange(100)] for row in xrange(hd.xdim)]
    for y in xrange(hd.ydim):
	for x in xrange(hd.xdim):
	    item = hd.__getitem__((x, y), None)
	    if item != None and item > lower:
		M[x][int(item*100.0)] += 1
#		print x, item, int(item/lower*100.0)
    hd.done_drawing()
    FlatM = []
    for y in xrange(len(M[0])):
	for x in xrange(len(M)):
	    FlatM.append(M[x][y])
    RM = r.matrix(robjects.FloatVector(FlatM), len(M), len(M[0]))

    iv = r('1:'+str(len(M)+1))
    ivv = robjects.FloatVector([float(x)/float(len(M[0])) for x in range(0, len(M[0]))])
#    ivv = robjects.IntVector(range(0, len(M[0])))
    c = r('c("white", rev(rainbow(100000)[1:80000]))')
    r['image.plot'](iv, ivv, RM, col=c, main=hd.title, xlab=" ", ylab=" ")




class Plot:
    allplots = []
    def __init__(self, plotfun, interval = None):
	if interval == None:
	     from saveableparams import parameters
	     interval = parameters.plotting_frequency
	self.plotfun = plotfun
	self.interval = interval
	Plot.allplots.append(self)
    def plot(self, env):
	raise Exception("Obsolete method called")

    def interval_plot(self, env):
	if self.interval > 0 and env.generation % self.interval == 0:
	    self.plot(env)

    def save(self, env, filename = "plot.pdf"):
        raise Exception("Obsolete method called")

    @staticmethod
    def plot_all(env):
	raise Exception("Obsoletemethod called")

    @staticmethod
    def interval_plot_all(env):
	for p in Plot.allplots:
	    p.interval_plot(env)

    @staticmethod
    def save_all(env, filename = "plots.pdf"):
	raise Exception("Obsolete method called")

    @staticmethod
    def save_png(env, filename_base = "plot"):
	raise Exception("Obsolete method called")
	

first_param_plot_type = lambda env: parameter_density_plot(env, 0)
history_plot_type = lambda env: history_plot(env)
history_plot2_type = lambda env: history_plot2(env)
scatter_plot_type = lambda env: scatter_plot(env, 0, 1)
heatmap_aut_transp_plot_type = lambda env: heatmap_plot(env, 'aut_transposons')
heatmap_nonaut_transp_plot_type = lambda env: heatmap_plot(env, 'nonaut_transposons')
heatmap_transp_inactive_plot_type = lambda env: heatmap_plot(env, 'inactive_transposons')
heatmap_transp_activ = lambda env: heatmap_plot(env, 'transp_activ')
heatmap_fitness = lambda env: heatmap_plot(env, 'fitness')
histogram_aut_transp_plot_type = lambda env: histogram_plot2(env, 'aut_transposons')
histogram_nonaut_transp_plot_type = lambda env: histogram_plot2(env, 'nonaut_transposons')
histogram_fitness = lambda env: histogram_plot_fitness(env, 'fitness')
histogram_transpositions = lambda env: histogram_plot2(env, 'transpositions')


current_plot_type = first_param_plot_type

plot_interval = 1


def loop_plot(env):
    if parameters.plots_enabled:
	rinterface.process_revents()
	Plot.interval_plot_all(env)

def setup_plots():
    if not parameters.plots_enabled:
	return None

    if parameters.final_plots_only:
        if not parameters.heatmaps_enabled:
	    raise Exception("Can't make final plots if heatmaps aren't enabled!")
	Plot(histogram_aut_transp_plot_type)
	Plot(histogram_nonaut_transp_plot_type)
	Plot(histogram_fitness)
	return None

    Plot(history_plot_type)
    Plot(history_plot2_type)
#    Plot(first_param_plot_type, 10)
    Plot(scatter_plot_type)
    if parameters.heatmaps_enabled:
	Plot(heatmap_aut_transp_plot_type)
	Plot(heatmap_nonaut_transp_plot_type)
	Plot(heatmap_transp_inactive_plot_type)
	Plot(heatmap_transp_activ)
	Plot(histogram_aut_transp_plot_type)
	Plot(histogram_nonaut_transp_plot_type)
	Plot(histogram_fitness)
	Plot(histogram_transpositions)

def save_all(env, filename = "plots.pdf"):
    Plot.save_all(env, filename)

def save_png(env, filename = "plot"):
    Plot.save_png(env, filename)
