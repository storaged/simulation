

def fill_to(n, st):
    if(len(st) < n):
	return st + ((n-len(st))*' ')
    return st

class table:
    def __init__(self):
	self.columns = []
	self.datarows = []
    def add_column(self, colname, length = None):
	if length == None:
	    length = len(colname) + 6
	self.columns.append((colname, length))
    
    def column_names(self):
	return map(lambda x: x[0], self.columns)

    def header(self):
	ret = ""
	for colname, length in self.columns:
	    ret += fill_to(length, colname)
	ret += '\n'
	for _, length in self.columns:
	    ret += length * '='
	return ret

    def row(self, data = None):
	if data == None:
	    data = self.datarows[-1]
	ret = ""
	for i in xrange(len(data)):
	    ret += fill_to(self.columns[i][1], str(data[i]))
	return ret

    def add_row(self, data):
	self.datarows.append(data)

    def get_colnr_by_id(self, idd):
	colnr = 0
	if idd.__class__.__name__ == "int":
	    colnr = idd
	else:
	    for nr in xrange(len(self.columns)):
		name, _ = self.columns[nr]
		if name == idd:
		    colnr = nr
	return colnr

    def sort_by_column(self, colid, func = lambda x, y: -1 if (x<y) else 1 if (x>y) else 0, reverse = False):
	colnr = self.get_colnr_by_id(colid)
	sort_func = lambda x, y: func(x[colnr], y[colnr])
	self.sort_by(sort_func, reverse)

    def sort_by(self, func, reverse = False):
	self.datarows.sort(func, reverse=reverse)

    def get_data_as_str(self):
	ret = ""
	for trow in self.datarows:
	    ret += self.row(trow) + "\n"
	return ret

    def __str__(self):
	return self.header() + self.get_data_as_str()

    def plot(self, colnames = None, colours = None, scales = None, draw_legend = True):
	if colnames == None:
	    colnames = self.column_names()

	columnsset = {}
	for i in xrange(len(colnames)):
	    columnsset[i] = []

	maxval = -1e1000
	minval = 1e1000

	usescales = scales

	if usescales == None:
	    usescales = []
	    for i in xrange(len(colnames)):
		usescales.append(1.0)

	
	for row in self.datarows:
	    for i in xrange(len(colnames)):
		val = float(row[self.get_colnr_by_id(colnames[i])])*usescales[i]
		maxval = max(maxval, val)
		minval = min(minval, val)
		columnsset[i].append(val)
	
	if colours == None:
	    colours = r.rainbow(len(colnames))
	
	r.frame()
	r['plot.window'](xlim=r.c(0, len(columnsset[0])-1), ylim = r.c(minval, maxval))
	r.axis(1)
	r.axis(2)
	r.box()
	r.title(main = " ", xlab = " ")
	r.abline(h=0, lty=2)
	

	for i in xrange(len(columnsset)):
	    r.lines(range(len(columnsset[i])), columnsset[i], col = colours[i])

	


# Legend drawing - broken
#	r('par(xpd = TRUE, mar=par("mar")+c(0,0,0,40))')
#	a = len(columnsset[0])+5
#	print a
#	cmdstr = "legend('bottomright'," + list_to_c(colnames) + ")"
#	print cmdstr
#	#r.legend(a, colnames, col = colours)
#	r(cmdstr)
#	r('par(xpd = FALSE, mar=par("mar")+c(0,0,0,-40))')
	
	def scale_to_str(sc):
	    if sc == 1.0:
		return ""
	    elif sc < 1.0:
		return " * 1/" + str(1/sc)
	    else:
		return " * " + str(sc)

	newcolnames = []
	if scales != None:
	    for i in xrange(len(colnames)):
		newcolnames.append(colnames[i] + scale_to_str(scales[i]))
	else:
	    newcolnames = colnames
	
	if draw_legend:
	    r.legend(x = "bottomright", legend = newcolnames, fill=colours, inset = 0.02)
