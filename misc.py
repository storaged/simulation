

def flatten(list):
    ret = []
    for sublist in list:
	for elem in sublist:
	    ret.append(elem)
    return ret


class SetDict(dict):
    def set_insert(self, key, val):
        try:
	    self[key].add(val)
	except KeyError:
	    self[key] = set([val])
    def set_get(self, key):
        return self.basedict.get(key, set())



class ListDict(dict):
    def list_insert(self, key, val):
        try:
	    self[key].append(val)
	except KeyError:
	    self[key] = [val]
    def list_get(self, key):
        return self.basedict.get(key, [])


