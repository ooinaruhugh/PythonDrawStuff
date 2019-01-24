from PIL import Image
from itertools import *

width = 100
height = 100
pixelcount = width * height

def sampleimage():
    high = repeat(255)
    low = repeat(0)
    reds = list(islice(high, pixelcount//2)) + list(islice(low, pixelcount//2))
    blue = list(islice(low, pixelcount//2)) + list(islice(high, pixelcount//2))
    green = repeat(0, pixelcount)
    return zip(reds, green, blue)

if __name__ == "__main__":
    #draw = ImageDraw.Draw(im) # This might be used to create a canvas :)

    im = Image.new("RGB", (width, height), "white");

    for coords, pixel in zip(product(range(width), range(height)), sampleimage()):
        im.putpixel(coords, pixel)
    im.save("test.png")
