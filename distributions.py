
def happened(likelihood):
    return runif(0,1) < likelihood


	
def n_indist_balls_into_k_bins(n, k):
#returns a vector of k integers: amounts of indistinguishable balls that got randomly thrown into each distinct bin
    if k < 1:
        return []
    l = []
    for _unused in xrange(k-1):
        l.append(runifint(0, n))
    l.sort()
    result = []
    last = 0
    for now in l:
        result.append(now - last)
        last = now
    result.append(n - last)
    return result

def n_balls_into_k_bins(n, k):
    if k < 1:
        return []
    result = []
    for filled in xrange(k-1):
        x = rbinom(n, 1.0/float(k-filled))
        result.append(x)
        n = n-x
    result.append(n)
    return result

