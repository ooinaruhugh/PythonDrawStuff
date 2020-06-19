from typing import Tuple
from itertools import tee, product
from math import atan2
import argparse

from pointplot import linspace

from PIL import Image, ImageDraw
from tqdm import tqdm
from colour import Color



def technicolorMandelbrot(c: Tuple[int, int], idepth: int, sup=2):
    ''' 
        Tests whether a given point c is in the Mandelbrot set,
        i.e. whether (or how fast) the sequence x_n=x²_(n-1)+c diverges
        
        Returns 1 and the argument of z if c is in the set 
        and 0 if not
    '''
    cx, cy = c
    zx, zy = (0,0)

    for i in range(0, idepth):
        zx, zy = (zx*zx - zy*zy + cx, 2*zx*zy+cy)
        if zx*zx+zy*zy > sup*sup:
            return 0, 0
    return 1, atan2(zy, zx)

def computePicture(X, Y, f): 
    for j, y in enumerate(Y):
        for i, x in enumerate(X):
            yield (f(x, y), i, j)

def generateMandelbrot(xMin, xMax, yMin, yMax, xRes, yRes):
    X = linspace(xMin, xMax, xRes) # Move this outside and pass this here
    Y = linspace(yMin, yMax, yRes) # This too

    for j, y in enumerate(Y):
        for i, x in enumerate(X):
            yield (technicolorMandelbrot((x, y), iteration_depth), i, j)

def rgbPixel(rgb: Color):
    r = int(rgb.get_red() * 255)
    g = int(rgb.get_green() * 255)
    b = int(rgb.get_blue() * 255)

    return r,g,b

iteration_depth = 50
width = 2500
height = 2500

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates a colorized Mandelbrot image")
    parser.add_argument("--width", default=2500, type=int)
    parser.add_argument("--height", default=2500, type=int)
    parser.add_argument("--iDepth", default=50, type=int,
        help="Maximum number of iterations for one point")
    parser.add_argument("--xMin", default=-2.5, type=float)
    parser.add_argument("--xMax", default=1.25, type=float)
    parser.add_argument("--yMin", default=-1.75, type=float)
    parser.add_argument("--yMax", default=1.75, type=float)

    args = parser.parse_args()

    iteration_depth = args.iDepth
    width = args.width
    height = args.height

    im = Image.new("RGB", (width, height), "black")
    canvas = ImageDraw.Draw(im)

    for pixel, x, y in tqdm(generateMandelbrot(-2.5, 1.25, -1.75, 1.75, width, height), total=width*height):
        isMandelbrot, argument = pixel
        im.putpixel((x,y), rgbPixel(Color(hue=argument, saturation=1, luminance=0.5*isMandelbrot)))

    im.save("technicolorMandelbrot.png")