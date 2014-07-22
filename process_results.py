import array, sys, debug


def process_results(source, destination, description = None, trim_percentile = 0.0):
    closesource = False
    closedst = False
    closedesc = False
    if type(source) == type(str()):
	source = open(source, 'rb')
	closesource = True
    if type(description) == type(str()):
	description = open(description, 'w')
	closedesc = True
    elif description == None and type(destination) == type(str()):
	description = open(destination + ".desc", 'w')
	closedesc = True
    if type(destination) == type(str()):
	destination = open(destination, 'w')
	closedst = True
	
	
    data_type = source.read(1)
    eof = False

    #data = {}

    argmax = -10000000000

    gen = 0


    while not eof:
      gen += 1
      try:
	lenarr = array.array('L')
	lenarr.fromfile(source, 1)
	dataarr = array.array(data_type)
	dataarr.fromfile(source, lenarr[0])
	for i in xrange(len(dataarr)):
	    argmax = max(argmax, dataarr[i])
      except EOFError:
	eof = True

    if argmax == 0:
        argmax = 1

    if trim_percentile > 0.0:

	boxes = [0] * 10001

	source.seek(1)
	data_counter = 0
	eof = False

	while not eof:
	  try:
	      lenarr = array.array('L')
	      lenarr.fromfile(source, 1)
	      dataarr = array.array(data_type)
	      dataarr.fromfile(source, lenarr[0])
	      data_counter += len(dataarr)
	      for i in xrange(len(dataarr)):
		  boxes[int(dataarr[i]*10000.0/argmax)] += 1
	  except EOFError:
	      eof = True

	outliers_to_eliminate = int(data_counter*trim_percentile)
	
	i = len(boxes)-1
	
	while outliers_to_eliminate > 0:
	  outliers_to_eliminate -= boxes[i]
	  i -= 1
	  
	argmax = argmax * float(i+1) / 10000.0
	argmax *= 1.2


    if data_type == 'f':
	argmax = 1.0
    else:
	argmax += 20

    source.seek(1)

    pixels = 1000
    if argmax < 3000.0:
	pixels = int(argmax + 0.9) 

    if data_type == 'f':
	pixels = 1000

    description.write(str(argmax) + '\n')
    description.flush()
    if closedesc:
	description.close()


    def position(arg):
	return int(arg*pixels/argmax)



    gen = 0
    eof = False

    while not eof:
      try:
	gen += 1
	pixeldata = [0]*int(pixels+0.99)

	lenarr = array.array('L')
	lenarr.fromfile(source, 1)
	dataarr = array.array(data_type)
	dataarr.fromfile(source, lenarr[0])
	for i in xrange(len(dataarr)):
	  if dataarr[i] <= argmax:
	    pixeldata[position(dataarr[i])] += 1
	    """except: 
	    	debug.g("gg")
	    	debug.g(i)
	    	debug.g(dataarr[i])
	    	debug.g(position(dataarr[i]))
	    	debug.g(argmax)
	    	debug.g(data_type)
	    	debug.g(len(pixeldata))
	    	debug.g(pixeldata[position(dataarr[i])])"""
	destination.write(' '.join([str(pixel) for pixel in pixeldata]))
	destination.write('\n')
      except EOFError:
	eof = True

    destination.flush()
    if closedst:
	destination.close()
    
    if closesource:
	source.close()
	

    
if __name__ == "__main__":
    tp = 0.0
    if len(sys.argv) > 2:
	tp = float(sys.argv[2])
    process_results(sys.argv[1], sys.argv[1] + '.Rdata', trim_percentile = tp)
