from __future__ import print_function
from colorama import Fore, Back, Style
from colorama import init

init()

class Orb:
    def __init__(self, color, enhanced):
        self.color = color
        self.enhanced = enhanced

    def print_wood(self):
        print(Back.GREEN + 'G', end='')

    def print_fire(self):
        print(Back.RED + 'R', end='')

    def print_water(self):
        print(Back.BLUE + 'B', end='')

    def print_dark(self):
        print(Back.MAGENTA + 'D', end='')

    def print_light(self):
        print(Back.YELLOW + 'L', end='')

    def print_heart(self):
        print(Back.WHITE + 'H', end='')
        
    def print_blank(self):
        print(Back.BLACK + ' ', end='')

    print_dict = {
        'wood': print_wood,
        'fire': print_fire,
        'water': print_water,
        'dark': print_dark,
        'light': print_light,
        'heart': print_heart,
        None: print_blank,
            }

    def print_orb(self):
        self.print_dict[self.color](self)

    def __repr__(self):
        return str(self.color)

    def match(self, orb):
        if orb is None:
            return False
        if orb.color is None or self.color is None:
            return False
        return self.color == orb.color


class Grid:
    def __init__(self):
        self.grid = [[None] * 6 for i in range(5)]

    def add_orb(self, x, y, orb):
        self.grid[y][x] = orb

    def print_grid(self):
        print(Fore.BLACK)
        for row in self.grid:
            for orb in row:
                orb.print_orb()
            print()
        print(Fore.RESET + Back.RESET)

    def get_orb(self, x, y):
        return self.grid[y][x]

    def get_pos(self, orb):
        for y, row in enumerate(self.grid):
            for x, o in enumerate(row):
                if orb == o:
                    return (x, y)
        return None
    
    def destroy_orb(self, orb):
        for y, row in enumerate(self.grid):
            for x, o in enumerate(row):
                if orb == o:
                   self.grid[y][x] = Orb(None, False) 

    def find_matches(self):
        matched_orbs = set()
        for row in self.grid:
            for orb in row:
                if orb.match(self.up(orb)) and orb.match(self.down(orb)):
                    if orb not in matched_orbs and self.up(orb) not in matched_orbs and self.down(orb) not in matched_orbs:
                        m = Match(orb)
                        m.expand(self)
                        self.combo.append(m)
                        matched_orbs = matched_orbs.union(m.orbs)
                elif orb.match(self.left(orb)) and orb.match(self.right(orb)):
                    if orb not in matched_orbs and self.left(orb) not in matched_orbs and self.right(orb) not in matched_orbs:
                        m = Match(orb)
                        m.expand(self)
                        self.combo.append(m)
                        matched_orbs = matched_orbs.union(m.orbs)
        return matched_orbs

    def full_move(self):
        self.combo = []
        comboing = True
        while comboing:
            self.print_grid()
            eliminated = self.find_matches()
            comboing = eliminated
            for orb in eliminated:
                self.destroy_orb(orb)
            self.fall()
            self.print_grid()
        print("{} Combos, {} Orbs Matched".format(len(self.combo), 0))


    def fall(self):
        for row in reversed(self.grid):
            for orb in row:
                if orb.color is None:
                    up = self.up(orb)
                    print(up)
                    orb = up
                    up = Orb(None, False)


    def up(self, orb):
        for y, row in enumerate(self.grid):
            for x, o in enumerate(row):
                if orb == o:
                    if y > 0:
                        return self.grid[y-1][x]
        return Orb(None, False)

    def down(self, orb):
        for y, row in enumerate(self.grid):
            for x, o in enumerate(row):
                if orb == o:
                    if y < 4:
                        return self.grid[y+1][x]
        return Orb(None, False)

    def left(self, orb):
        for y, row in enumerate(self.grid):
            for x, o in enumerate(row):
                if orb == o:
                    if x > 0:
                        return self.grid[y][x-1]
        return Orb(None, False)

    def right(self, orb):
        for y, row in enumerate(self.grid):
            for x, o in enumerate(row):
                if orb == o:
                    if x < 5:
                        return self.grid[y][x+1]
        return Orb(None, False)

    def __repr__(self):
        return str(self.grid)


class Match:
    def __init__(self, start):
        self.start = start
        self.orbs = [start]

    def expand(self, grid):
        solid_match = set()
        checked = set()
        plausible = set()
        plausible.add(self.start)

        while plausible:
            orb = plausible.pop()
            checked.add(orb)
            # add plausible neighbors
            if orb.match(grid.up(orb)) and grid.up(orb) not in checked:
                plausible.add(grid.up(orb))
            if orb.match(grid.down(orb)) and grid.up(orb) not in checked:
                plausible.add(grid.down(orb))
            if orb.match(grid.left(orb)) and grid.left(orb) not in checked:
                plausible.add(grid.left(orb))
            if orb.match(grid.right(orb)) and grid.right(orb) not in checked:
                plausible.add(grid.right(orb))

            # check for actual matches
            if orb.match(grid.up(orb)) and orb.match(grid.down(orb)):
                solid_match.add(orb)
                solid_match.add(grid.up(orb))
                solid_match.add(grid.down(orb))

            if orb.match(grid.left(orb)) and orb.match(grid.right(orb)):
                solid_match.add(orb)
                solid_match.add(grid.left(orb))
                solid_match.add(grid.right(orb))

        self.orbs = solid_match
