# Make a plot of the mandelbrot set
import ctypes

_mandel = ctypes.cdll.LoadLibrary("./_mandel.so")
in_mandelbrot = _mandel.in_mandelbrot
in_mandelbrot.argtypes=(ctypes.c_double, ctypes.c_double, ctypes.c_int)
in_mandelbrot.restype = ctypes.c_int

# Generate a range of floating point numbers 
def frange(fmin,fmax,divisions):
    delta = (fmax - fmin)/divisions
    x = fmin
    for i in xrange(divisions):
        yield x
        x += delta

# Generate all of the pixels of the mandelbrot set.  The output of
# this function is a sequence of rows.  Each row is a sequence of
# True/False values indicating whether or not a point is a member
# of the set or not. Note: This is using generators and generator
# expressions to produce all of the pixels without ever allocating
# a huge array of pixels in memory. 

def generate_mandel(xmin,ymin,width,height,pixels,n):
    for y in frange(ymin,ymin+height,pixels):
        yield (in_mandelbrot(x,y,n) for x in frange(xmin,xmin+width,pixels))


# Make a plot and write it as a PNG image.   
# Change these parameters to experiment with the image

xmin   = -2.0
ymin   = -1.5
width  = 3.0
height = 3.0
pixels = 512
n      = 400

import png
import time

start = time.time()
f = open("mandel.png","wb")
w = png.Writer(pixels,pixels,greyscale=True,bitdepth=1)
w.write(f,generate_mandel(xmin,ymin,width,height,pixels,n))
f.close()
end = time.time()

print "Wrote mandel.png"
print end-start, "seconds"
