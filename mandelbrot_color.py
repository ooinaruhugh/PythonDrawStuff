from typing import Tuple
from itertools import tee, product
from math import atan2
import argparse
from functools import partial

from colorsys import hls_to_rgb

from pointplot import linspace

from PIL import Image, ImageDraw
from tqdm import tqdm
from colour import Color

def mandelbrot(c: complex, idepth: int, sup=2) -> complex:
    ''' 
        Tests whether a given point c is in the Mandelbrot set,
        i.e. whether (or how fast) the sequence x_n=x²_(n-1)+c diverges
        
        Returns z if c is in the set 
        and 0 if not
    '''

    z = 0+0j

    for i in range(0, idepth):
        z = z**2 + c
        if abs(z) > sup:
            return 0+0j
    return z

def altMandelbrot(c: Tuple[int, int], idepth: int, sup=2) -> Tuple[int, int]:
    ''' 
        Tests whether a given point c is in the Mandelbrot set,
        i.e. whether (or how fast) the sequence x_n=x²_(n-1)+c diverges
        
        Returns z if c is in the set 
        and 0 if not
    '''

    cx, cy = c
    zx, zy = (0,0)

    for i in range(0, idepth):
        zx, zy = (zx*zx - zy*zy + cx, 2*zx*zy+cy)
        if zx*zx+zy*zy > sup*sup:
            return (0, 0)
    return (zx, zy)

def computePicture(X, Y, f):
    for (i, x),(j, y) in tqdm(product(enumerate(X),enumerate(Y))):
        yield (f((x, y)), i, j)
        # yield (f(x+y*1j), i, j)

def mandelColor(pixel):
    x, y = pixel

    h = atan2(y, x)
    s = 1
    l = 0.5*(not x+y == 0)

    r,g,b = hls_to_rgb(h, l, s)

    return int(r*255), int(g*255), int(b*255)

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

    xMin = args.xMin
    xMax = args.xMax
    yMin = args.yMin
    yMax = args.yMax

    # Discretize domain into pixels
    X = linspace(xMin, xMax, width) 
    Y = linspace(yMin, yMax, height)

    im = Image.new("RGB", (width, height), "black")
    canvas = ImageDraw.Draw(im)

    domain = computePicture(list(X),list(Y),partial(altMandelbrot, idepth=iteration_depth))

    coloring = [(mandelColor(z),x,y) for z,x,y in domain]

    for result, x, y in tqdm(coloring):
        # print(x,y)
        im.putpixel((x,y), result)

    im.save("newTest.png")