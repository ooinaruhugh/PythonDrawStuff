from PIL import Image, ImageDraw
import pointplot


canvas_size = 500
circle_size = int(canvas_size * 0.9)


def coordinates(plane):
    translated_plane = pointplot.translate(plane, int(circle_size*-0.5), int(circle_size*-0.5))
    circle = filter(lambda v : (v[0] ** 2) + (v[1] ** 2) == circle_size, translated_plane)
    return pointplot.translate(circle, int(circle_size*0.55), int(circle_size*0.55))


if __name__ == "__main__":
    im = Image.new("RGB", (canvas_size, canvas_size), "black")
    canvas = ImageDraw.Draw(im)

    plane = pointplot.plane(circle_size, circle_size)
    circle = coordinates(plane)

    for v in circle:
        im.putpixel(v, (255,255,255))

    im.save("circle.png")
