from __future__ import print_function
from PIL import Image
import sys

DEBUG = True

colors = {
        'dark':(144, 90, 145),
        'wood':(102, 143, 107),
        'heart':(165, 83, 122),
        'water':(109, 136, 163),
        'fire':(176, 99, 89),
        'light':(164, 153, 95),
        'dark+':(177, 132, 171)
        }

def top_left_grid((width, height)):
    x = int(round(width * .0055))
    y = int(round(height * .4269))
    return (x, y)

def box_size((width, height)):
    x = int(round(width * .1638))
    y = int(round(height * .0888))
    return (x, y)

def find_sizes(image, search_row, height):
    dark_brown = (38, 25, 25)
    darker_brown = (39, 24, 22)
    light_brown = (87, 53, 41)
    top = None
    for y in range(height):
        if colors_close(dark_brown, image[search_row, y], 10):
            top = y
            break
    left = None
    if top:
        for x in reversed(range(search_row)):
            if not colors_close(darker_brown, image[x, top], 5):
                left = x + 1
                break
    if left:
        box = None
        for y in range(top, height):
            if colors_close(light_brown, image[left + 1, y], 10):
                box = y - top, y - top
                break
    return (left, top), box

def colors_close(a, b, dist=15):
    return close(a[0], b[0], dist) and close(a[1], b[1], dist) and close(a[2], b[2], dist)

def close(a, b, dist):
    return a > b - dist and a < b + dist 

def average_color(pixels):
    r, g, b = 0, 0, 0
    for p in pixels:
        r += p[0]
        g += p[1]
        b += p[2]
    return r//len(pixels), g//len(pixels), b//len(pixels)

def average_square(image, center, height):
    pixels = []
    for x in range(center[0] - height//2, height + (center[0] - height//2)):
        for y in range(center[1] - height//2, height + (center[1] - height//2)):
            pixels.append(image[x, y])
    return average_color(pixels)

def match_colors(orbs):
    ret = []
    for orb in orbs:
        c = None
        for color in colors.keys():
            key = colors[color]
            if colors_close(key, orb):
                c = color
        ret.append(c)
    return ret

def parse_image(file_name):
    im = Image.open(file_name)
    p = im.load()

    top_left = top_left_grid(im.size)
    box = box_size(im.size)
    #top_left, box = find_sizes(p, top_left_grid(im.size)[0] + 2, im.size[1])

    if DEBUG:
        print("top_left {}, box {}".format(top_left, box))

    cursor = top_left[0] + box[0] // 2, top_left[1] + box[1] //2
    left_column = cursor[0]
    cursor = cursor[0] - box[0], cursor[1] - box[1]

    orb_colors = []

    for i in range(30):
        if i % 6 == 0:
            cursor = left_column, cursor[1] + box[1]
            if DEBUG:
                print()
        else:
            cursor = cursor[0] + box[0], cursor[1]
        #orb_colors.append(p[cursor[0], cursor[1]])
        orb_colors.append(average_square(p, (cursor[0], cursor[1]), box[0]))
        if DEBUG:
            print(cursor, end=' ')
    if DEBUG:
        print()
    if DEBUG:
        for i, c in enumerate(orb_colors):
            if i % 6 == 0:
                print()
            print(c, end=' ')
        print()
    ret = match_colors(orb_colors)
    if DEBUG:
        for i, c in enumerate(ret):
            if i % 6 == 0:
                print()
            print(c, end=' ')
        print()
    return ret


if __name__ == "__main__":
    if len(sys.argv) > 1:
        parse_image(sys.argv[1])
    else:
        parse_image('test.png')
