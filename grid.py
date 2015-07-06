from __future__ import print_function
from colorama import Fore, Back, Style
from colorama import init

init()
DEBUG = False

def print_wood():
    print(Back.GREEN + 'G', end='')

def print_fire():
    print(Back.RED + 'R', end='')

def print_water():
    print(Back.BLUE + 'B', end='')

def print_dark():
    print(Back.MAGENTA + 'D', end='')

def print_light():
    print(Back.YELLOW + 'L', end='')

def print_heart():
    print(Back.WHITE + 'H', end='')
    
def print_blank():
    print(Back.BLACK + ' ', end='')


def print_orb(color):
    print_dict = {
        'g': print_wood,
        'r': print_fire,
        'b': print_water,
        'd': print_dark,
        'l': print_light,
        'h': print_heart,
        None: print_blank,
            }
    print_dict[color]()
    
def graph(grid):
    d = {'wood':'g',
        'fire':'r',
        'water':'b',
        'dark':'d',
        'light':'l',
        'heart':'h',
        None: None
        }
    graph = []
    for g in grid:
        graph.append(d[g])
    if(DEBUG):
        print(graph)
    return graph

def print_grid(grid):
    print(Fore.BLACK)
    for i, orb  in enumerate(grid):
        if i % 6 == 0:
            print()
        print_orb(orb)
    print(Fore.RESET + Back.RESET, end='')
    print()

def get_orb(grid, x, y):
    return grid[pos_to_index(x, y)]

def pos_to_index((x, y)):
    return (y*6) + x

def swap(grid, pos1, pos2):
    apos = pos_to_index(pos1) 
    bpos = pos_to_index(pos2)
    grid[apos], grid[bpos] = grid[bpos], grid[apos]
    return grid

def find_matches(grid):
    matched_pos = set()
    combo = []
    for i, orb in enumerate(grid):
        if up(i) and orb == grid[up(i)] and down(i) and orb == grid[down(i)] and orb:
            if i not in matched_pos and up(i) not in matched_pos and down(i) not in matched_pos:
                combo.append(match(grid, i))
                matched_pos = matched_pos.union(combo[-1])
        elif left(i) and orb == grid[left(i)] and right(i) and orb == grid[right(i)] and orb:
            if i not in matched_pos and left(i) not in matched_pos and right(i) not in matched_pos:
                combo.append(match(grid, i))
                matched_pos = matched_pos.union(combo[-1])
    return combo, matched_pos

def full_move(grid):
    combo = []
    comboing = True
    while comboing:
        if DEBUG:
            print_grid(grid)
        new_combo, matched_pos = find_matches(grid)
        combo += new_combo
        comboing = matched_pos
        for i in matched_pos:
            grid[i] = None
        if DEBUG:
            print_grid(grid)
        grid = fall(grid)

    combo_num = len(combo)
    orbs_matched = sum([len(x) for x in combo])
    if DEBUG:
        print("{} Combos, {} Orbs Matched".format(combo_num, orbs_matched))
    return (combo_num, orbs_matched)


def fall(grid):
    falling = True
    while falling:
        falling = False
        for i, orb in enumerate(grid):
            if orb is None:
                d = up(i)
                if d and grid[d] is not None:
                    falling = True
                    grid[i] = grid[d]
                    grid[d] = None
    return grid


def up(pos):
    if pos - 6 < 0:
        return None
    return pos - 6

def down(pos):
    if pos + 6 >= 30:
        return None
    return pos + 6

def left(pos):
    if pos % 6 == 0:
        return None
    return pos - 1

def right(pos):
    if pos % 6 == 5:
        return None
    return pos + 1

def match(grid, start):
    solid_match = set()
    checked = set()
    plausible = set()
    plausible.add(start)

    while plausible:
        pos = plausible.pop()
        checked.add(pos)
        # add plausible neighbors
        if up(pos) and grid[pos] == grid[up(pos)] and up(pos) not in checked:
            plausible.add(up(pos))
        if down(pos) and grid[pos] == grid[down(pos)] and down(pos) not in checked:
            plausible.add(down(pos))
        if left(pos) and grid[pos] == grid[left(pos)] and left(pos) not in checked:
            plausible.add(left(pos))
        if right(pos) and grid[pos] == grid[right(pos)] and right(pos) not in checked:
            plausible.add(right(pos))

        # check for actual matches
        if up(pos) and down(pos) and grid[pos] == grid[up(pos)] and grid[pos] == grid[down(pos)]:
            solid_match.add(pos)
            solid_match.add(up(pos))
            solid_match.add(down(pos))

        if left(pos) and right(pos) and grid[pos] == grid[left(pos)] and grid[pos] == grid[right(pos)]:
            solid_match.add(pos)
            solid_match.add(left(pos))
            solid_match.add(right(pos))

    return solid_match
