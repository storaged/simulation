from PIL import Image
import array, sys


if len(sys.argv)<2: raise Exception("no image to process") 

name = sys.argv[1]
try:
	file = Image.open(name)
	#file.show()
except: 
	raise Exception("error while loading \"%s\"" % name)

with open(name+".tmp", 'w') as f: 
  arr = array.array('B')
  def app(pixel):
    x,y,z=pixel[0],pixel[1],pixel[2]
    arr.append(x)
    arr.append(y)
    arr.append(z)
    
  for y in xrange(file.size[1]-1, -1, -1):
    for x in xrange(file.size[0]):
      app(file.getpixel((x,y)))
  arr.tofile(f)

with open(name+".info.tmp", 'w') as f:
  arrinfo = array.array('L')
  arrinfo.append(file.size[0])
  arrinfo.append(file.size[1])
  arrinfo.tofile(f)
