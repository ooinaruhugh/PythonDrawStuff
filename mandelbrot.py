from typing import Tuple
from PIL import Image, ImageDraw
from itertools import tee, repeat
import pointplot
import math

def mandelbrot(c: Tuple[int, int], idepth: int, sup=2):
    ''' 
        Tests whether a given point c is in the Mandelbrot set,
        i.e. whether (or how fast) the sequence x_n=x²_(n-1)+c diverges
        
        Returns 1 if c is in the set and 1-i if not where i is the number of iterations
    '''
    cx, cy = c
    zx, zy = (0,0)

    for i in range(0, idepth):
        zx, zy = (zx*zx - zy*zy + cx, 2*zx*zy+cy)
        if zx*zx+zy*zy > sup*sup:
            return idepth-i
    return 1

iteration_depth = 50
canvas_size = 5000

def normalize(plane, width, height):
    """
        Takes a pixel canvas where x is in [0, width] and y is in [0, height]
        and returns a pixel canvas where x is in [-1, 1] and y is in [-1, 1]
    """
    return map(lambda v: ((v[0]-0.5*width)/(0.5*width), (v[1]-0.5*height)/(0.5*height)), plane)

def normalizePoint(point: Tuple[int, int], xMax, yMax):
    return ((point[0]-0.5*xMax)/(0.5*xMax), (point[1]-0.5*yMax)/(0.5*yMax))


if __name__ == "__main__":
    im = Image.new("RGB", (canvas_size, canvas_size), "black")
    canvas = ImageDraw.Draw(im)

    # A grid of coordinates (as integer values)
    plane = pointplot.plane(canvas_size, canvas_size)

    for z in plane:
        # circle doesn't consist of integer values anymore, so we need to convert them
        result = mandelbrot(normalizePoint(z, canvas_size, canvas_size), iteration_depth)
        grayscale_value = 255 // (result if result else 1)
        im.putpixel(z, (grayscale_value, grayscale_value, grayscale_value))

    im.save("mandelbrot.png")
