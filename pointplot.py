from itertools import product

def plane(width, height):
    return product(range(0, width), range(0, height))

def translate(coordinates, dx, dy):
    return map(lambda v : (v[0] + dx, v[1] + dy), coordinates)
