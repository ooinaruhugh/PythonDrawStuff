from PIL import Image, ImageDraw, ImageColor
import math 
from itertools import tee, repeat, takewhile, count
from colour import Color


height = 900
width = 900
max_t = 2*math.pi

amplitude = 400
x_max = width * 0.45
y_max = height * 0.45


freq_x = 3
freq_y = 4

phase_0 = math.pi
d_phase = math.pi/16

def value(t, frequency, amplitude, phase):
    """ This is basically just a sine function. """
    return amplitude * math.sin(frequency * t + phase)

def coordinates(freq_x, x_max, x_phase, freq_y, y_max, y_phase, width, height):
    """ 
    Creates an iterator that returns a tuple of before and after xy-pairs each grouped together in a tuple. 
    """
    def pairwise(iterable):
        """ Makes an iterator that returns a tuple of current and next sequence value """
        a, b = tee(iterable)
        next(b)
        return zip(a, b)

    def ordinate(frequency, amplitude, phase):
        """ Calculates the values for x and y. """
        t = takewhile(lambda x : x < 2 * math.pi, count(0, 0.02))
        coords = map(value, t, repeat(frequency), repeat(amplitude), repeat(phase))
        return map(lambda x : x + width / 2, coords)

    x = ordinate(freq_x, x_max, x_phase)
    y = ordinate(freq_y, y_max, y_phase)
    return pairwise(zip(x, y))


def init():
    return Image.new("RGB", (width, height), "white")

def draw(canvas, x, y, t):
    print((x,y))
    new_x = value(t + 0.02, freq_x, x_max, phase_0)
    new_y = value(t + 0.02, freq_y, y_max, phase_0)
    print((new_x,new_y))
    canvas.line([(x + width/2, y + height/2), (new_x + width/2, new_y + height/2)], "black", 3)
    if not t > max_t:
        draw(canvas, new_x, new_y, t + 0.02)

def colors():
    """ Makes a 0-255 ranged RGB color from a HSL one. """
    for i in count(0, 0.02):
        r, g, b = Color(hue=i, saturation=1, luminance=0.5).rgb
        yield (int(255*r), int(255*g), int(255*b))

if __name__ == "__main__":
    
    im = Image.new("RGB", (width, height), "black")
    canvas = ImageDraw.Draw(im)    

    color = colors()
    coords = coordinates(freq_x, x_max, phase_0, freq_y, y_max, phase_0 + d_phase, width, height)
    for old, new in coords:
        canvas.line([old, new], next(color), 1)

    im.save("lissajous.png")
