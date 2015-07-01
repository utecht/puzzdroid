from __future__ import print_function
from colorama import Fore, Back, Style
from colorama import init
from grid import Grid, Orb
import copy
import cProfile

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

def create_initial_grid():
    grid = []
    for x in range(6):
        for y in range(5):
            grid.append([(x,y)])
    return grid

def all_possible_moves(move):
    last_move = move[-1]
    new_moves = []
    # up
    if last_move[1] > 0:
        new_moves.append(move + [(last_move[0], last_move[1] - 1)])
    # down
    if last_move[1] < 4:
        new_moves.append(move + [(last_move[0], last_move[1] + 1)])
    # left
    if last_move[0] > 0:
        new_moves.append(move + [(last_move[0] - 1, last_move[1])])
    # right
    if last_move[0] < 5:
        new_moves.append(move + [(last_move[0] + 1, last_move[1])])
    return new_moves

def brute_generate(depth):
    moves = create_initial_grid()
    for i in range(depth):
        new_level = []
        for move in moves:
            new_level.extend(all_possible_moves(move))
        if i == 0:
            moves = new_level
        else:
            moves.extend(new_level)
    return moves

def solve(grid, move):
    for i, m in enumerate(move):
        if i > 0:
            grid.swap(move[i - 1], m)
    return grid.full_move()

def brute_force(depth):
    best_combo = -1
    best_orb = -1
    best_move = None
    for move in brute_generate(depth):
        combo, orbs = solve(copy.deepcopy(g), move)
        if combo > best_combo:
            best_move = move
            best_combo = combo
            best_orb = orbs
        elif combo == best_combo and orbs > best_orb:
            best_move = move
            best_combo = combo
            best_orb = orbs

    print("{} combo, {} orbs".format(best_combo, best_orb))
    print(best_move)

cProfile.run("brute_force(5)")
