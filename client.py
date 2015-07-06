from vncdotool import api
from reader import *
import time
from threading import Thread
from solver import *
from grid import *

client = api.connect('localhost:1', 'vnc')

f = 'working.png'
tl = get_grid(f)
b = get_box(f)[0]

def translate(x, y):
    x = (b//2) + (b * x)
    y = (b//2) + (b * y)
    x = x + tl[0]
    y = y + tl[1]
    return x, y

def mouseDrag2(client, start, dest, step):
    """ Move the mouse point to position (x, y) in increments of step
    """
    sx, sy = start
    x, y = dest
    if x < sx:
        xsteps = [sx - i for i in xrange(step, sx - x + 1, step)]
    else:
        xsteps = xrange(sx, x, step)

    if y < sy:
        ysteps = [sy - i for i in xrange(step, sy - y + 1, step)]
    else:
        ysteps = xrange(sy, y, step)

    for ypos in ysteps:
        #time.sleep(.001)
        client.mouseMove(sx, ypos)

    for xpos in xsteps:
        #time.sleep(.001)
        client.mouseMove(xpos, sy)

    client.mouseMove(x, y)

def threadDrag(client, start, dest, step=1):
    thread = Thread(target=mouseDrag2, args=(client, start, dest, step))
    thread.start()
    thread.join()

def do_moves(client, moves):
    start = moves[0]
    pos = translate(*start)
    client.mouseMove(*pos)
    client.mouseDown(1)
    for move in moves:
        dest = translate(*move)
        threadDrag(client, pos, dest, 2)
        pos = dest
    client.mouseUp(1)

def solve_and_move(client):
    client.captureScreen(f)


    g = graph(parse_image(f))
    if None in g:
        print("Bad Graph")
    else:
        moves = brute_force(7, g)
        #moves = [(1, 2), (2, 2), (2, 3), (3, 3), (4, 3)]

        do_moves(client, moves)

solve_and_move(client)
