from itertools import product

def linspace(start, stop, res):
    for k in range(res):
        yield start + (stop - start) / (res - 1) * k

def plane(width, height):
    return product(range(width), range(height))

def translate_2d(coordinate, dx, dy):
    return (coordinate[0] + dx, coordinate[1] + dy)

def scale(coordinate, l):
    return tuple([l * x for x in coordinate])
