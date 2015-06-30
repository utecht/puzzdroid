from __future__ import print_function
from colorama import Fore, Back, Style
from colorama import init
from grid import Grid, Orb

init()

grid = ['p', 'r', 'g', 'y', 'b', 'h',
        'r', 'y', 'h', 'r', 'b', 'g',
        'g', 'p', 'y', 'p', 'y', 'p',
        'b', 'h', 'h', 'p', 'h', 'y',
        'h', 'y', 'r', 'g', 'h', 'h']

solved_grid = [ 'p', 'g', 'h', 'y', 'b', 'h',
                'r', 'r', 'r', 'b', 'y', 'g',
                'g', 'p', 'y', 'p', 'p', 'p',
                'b', 'h', 'h', 'h', 'y', 'y',
                'h', 'y', 'r', 'g', 'y', 'h']

hard_grid = [ 'p', 'g', 'h', 'y', 'b', 'h',
              'r', 'r', 'r', 'b', 'y', 'g',
              'g', 'r', 'p', 'p', 'p', 'p',
              'b', 'r', 'h', 'h', 'y', 'y',
              'h', 'y', 'r', 'g', 'y', 'h']

colors = {
        'p': 'dark',
        'y': 'light',
        'h': 'heart',
        'r': 'fire',
        'b': 'water',
        'g': 'wood'
        }

def create_grid(grid):
    g = Grid()
    for i, orb in enumerate(grid):
        x = i % 6
        y = i // 6
        g.add_orb(x, y, Orb(colors[orb], False))
    return g

g = create_grid(grid)
gs = create_grid(solved_grid)
hg = create_grid(hard_grid)

g.print_grid()
gs.print_grid()
hg.print_grid()

gs.full_move()
hg.full_move()
