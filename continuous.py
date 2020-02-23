from PIL import Image, ImageDraw, ImageColor
from itertools import tee, repeat, count, chain
from colour import Color


def pairwise(iterable):
    """ Makes an iterator that returns a tuple of current and next sequence value """
    a, b = tee(iterable)
    first = next(b)
    return zip(a, b)

def pairwiseClosedCircle(iterable):
    """ 
        Makes an iterator that returns a tuple of current and next sequence value.
        The last pair is (lastValue, firstValue)
    """
    a, b = tee(iterable)
    first = next(b)
    return zip(a, chain(b, [first]))

def hslGradient(step=0.02):
    """ 
        Iterator that goes around the HSL color circle
        Makes a 0-255 ranged RGB color from a HSL one. 
    """
    for i in count(0, step):
        r, g, b = Color(hue=i, saturation=1, luminance=0.5).rgb
        yield (int(255*r), int(255*g), int(255*b))

def solidColor(color):
    r, g, b = Color(color).rgb
    while True:
        yield (int(255*r), int(255*g), int(255*b))

def drawContinuous(canvas, coordinates, color, line_width):
    """
        Draws a (crudely) interpolated continuous line plot from an 
    """
    for old, new in pairwiseClosedCircle(coordinates):
        canvas.line([old, new], next(color), line_width)
