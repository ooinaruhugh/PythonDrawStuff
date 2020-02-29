from typing import Tuple
from PIL import Image, ImageDraw
from itertools import tee, repeat
from pointplot import linspace
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

def generateMandelbrot(xMin, xMax, yMin, yMax, xRes, yRes):
    X = linspace(xMin, xMax, xRes)
    Y = linspace(yMin, yMax, yRes)

    for j, y in enumerate(Y):
        for i, x in enumerate(linspace(xMin, xMax, xRes)):
            yield (mandelbrot((x, y), iteration_depth), i, j)

iteration_depth = 50
width = 1200
height = 1400

def normalize(plane, width, height):
    """
        Takes a pixel canvas where x is in [0, width] and y is in [0, height]
        and returns a pixel canvas where x is in [-1, 1] and y is in [-1, 1]
    """
    return map(lambda v: ((v[0]-0.5*width)/(0.5*width), (v[1]-0.5*height)/(0.5*height)), plane)

def normalizePoint(point: Tuple[int, int], xMax, yMax):
    return ((point[0]-0.5*xMax)/(0.5*xMax), (point[1]-0.5*yMax)/(0.5*yMax))


if __name__ == "__main__":
    im = Image.new("RGB", (width, height), "black")
    canvas = ImageDraw.Draw(im)

    for pixel, x, y in generateMandelbrot(-2.5, 1.5, -2.5, 1, width, height):
        grayscaleValue = 255 // (pixel if pixel else 1)
        im.putpixel((x,y), (grayscaleValue, grayscaleValue, grayscaleValue))

    im.save("mandelbrot.png")
