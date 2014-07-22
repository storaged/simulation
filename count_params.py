import sys

def count_params(filename = "parameters.py"):
    from saveableparams import Parameters
    p = Parameters()

    fname = "parameters.py"
    if len(sys.argv)>1:
        fname = sys.argv[1]

    names = p.load_from_file(fname)

    count = 1

    for name in names:
        if isinstance(p.__dict__[name], list):
	    count *= len(p.__dict__[name])

    return count
