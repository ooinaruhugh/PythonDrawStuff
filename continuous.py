from PIL import Image, ImageDraw, ImageColor
from itertools import tee, repeat, count
from colour import Color


def pairwise(iterable):
    """ Makes an iterator that returns a tuple of current and next sequence value """
    a, b = tee(iterable)
    next(b)
    return zip(a, b)

def hsl_gradient():
    """ Makes a 0-255 ranged RGB color from a HSL one. """
    for i in count(0, 0.02):
        r, g, b = Color(hue=i, saturation=1, luminance=0.5).rgb
        yield (int(255*r), int(255*g), int(255*b))

def solid_color(color):
    r, g, b = Color(color).rgb
    while True:
        yield (int(255*r), int(255*g), int(255*b))

def drawcontinuous(canvas, coordinates, color, line_width):
    old = next(coordinates)
    for new in coordinates:
        canvas.line([old, new], next(color), line_width)
        old = new
