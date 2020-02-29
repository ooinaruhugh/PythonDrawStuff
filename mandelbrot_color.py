from pointplot import linspace
from PIL import Image, ImageDraw
from itertools import tee, product
from math import atan2

from tqdm import tqdm
from colour import Color

from typing import Tuple


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

def generateMandelbrot(xMin, xMax, yMin, yMax, xRes, yRes):
    X = linspace(xMin, xMax, xRes)
    Y = linspace(yMin, yMax, yRes)

    for j, y in enumerate(Y):
        for i, x in enumerate(linspace(xMin, xMax, xRes)):
            yield (technicolorMandelbrot((x, y), iteration_depth), i, j)

def rgbPixel(rgb: Color):
    r = int(rgb.get_red() * 255)
    g = int(rgb.get_green() * 255)
    b = int(rgb.get_blue() * 255)

    return r,g,b

iteration_depth = 50
width = 10
height = 10

if __name__ == "__main__":
    im = Image.new("RGB", (width, height), "black")
    canvas = ImageDraw.Draw(im)

    for pixel, x, y in tqdm(generateMandelbrot(-.85, -.75, 0.1, 0.3, width, height), total=width*height):
        iteration, argument = pixel
        im.putpixel((x,y), rgbPixel(Color(hue=argument, saturation=1, luminance=0.5*iteration)))

    im.save("neuMandelbrot_clored.png")