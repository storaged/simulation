import sys, inspect, os
def g(x):
	sys.stderr.write("%s%s\n" % ("="*20, x))
def d(x):
	g("%s\n%s" % (x, inspect.stack()))
def v(x):
	g(x)
	return x
def terminate(x):
	g(x)
	os._exit(1)
