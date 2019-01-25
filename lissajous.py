from PIL import Image, ImageDraw
import math 

height = 900
width = 900
max_t = 2*math.pi

amplitude = 400
x_max = amplitude
y_max = amplitude

freq_x = 3
freq_y = 4

phase_0 = math.pi
d_phase = math.pi/16

def value(t, frequency, amplitude, phase):
    return amplitude * math.sin(frequency * t + phase)

def init():
    return Image.new("RGB", (width, height), "white")

def draw(canvas, x, y, t):
    new_x = value(t + 0.02, freq_x, x_max, phase_0)
    new_y = value(t + 0.02, freq_y, y_max, phase_0)
    canvas.line([(x + width//2, y + height//2), (new_x + width//2, new_y + height//2)], "black", 3)
    if not t > max_t:
        draw(canvas, new_x, new_y, t + 0.02)

if __name__ == "__main__":
    im = Image.new("RGB", (width, height), "white")
    canvas = ImageDraw.Draw(im)
    draw(canvas, value(0, freq_x, x_max, phase_0) + width//2, value(0, freq_y, y_max, phase_0 + d_phase) + height//2, 0)
    im.save("lissajous.png")
