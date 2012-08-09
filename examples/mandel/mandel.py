# Make a plot of the mandelbrot set
import bitey

# Test a given x,y coordinate to see if it's a member of the set
def in_mandelbrot(x0,y0,n):
    x = 0
    y = 0
    while n > 0:
        xtemp = x*x - y*y + x0
        y = 2*x*y + y0
        x = xtemp
        n -= 1
        if x*x + y*y > 4: return False
    return True

# Attempt to load the C compiled version
try:
    from _mandel import in_mandelbrot
except ImportError:
    pass

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
