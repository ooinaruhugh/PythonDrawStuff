from PIL import Image, ImageDraw
import math 
from itertools import repeat, takewhile, count
import continuous


height = 2000
width = 2000
max_t = 2*math.pi

amplitude = 400
x_max = width * 0.45
y_max = height * 0.45

line_width = int(math.log10(height))

freq_x = 11
freq_y = 6

phase_0 = math.pi
d_phase = math.pi/16

def value(t, frequency, amplitude, phase):
    """ This is basically just a sine function. """
    return amplitude * math.sin(frequency * t + phase)

def coordinates(freq_x, x_max, x_phase, freq_y, y_max, y_phase, width, height):
    """ 
    Creates an iterator that returns some xy-Coordinates. 
    """

    def ordinate(frequency, amplitude, phase):
        """ Calculates the values for x and y. """
        t = takewhile(lambda x : x <= 2 * math.pi, count(0, 0.02))
        coords = map(value, t, repeat(frequency), repeat(amplitude), repeat(phase))
        return map(lambda x : x + width / 2, coords)

    x = ordinate(freq_x, x_max, x_phase)
    y = ordinate(freq_y, y_max, y_phase)
    return zip(x, y)


def init():
    return Image.new("RGB", (width, height), "white")

if __name__ == "__main__":
    
    im = Image.new("RGB", (width, height), "black")
    canvas = ImageDraw.Draw(im)    

    coords = coordinates(freq_x, x_max, phase_0, freq_y, y_max, phase_0 + d_phase, width, height)
    continuous.drawContinuous(canvas, coords, continuous.hslGradient(), line_width)

    im.save("lissajous.png")
