from random import choice, randint
from typing import List

from color import HSV
from dudek.HelperFunctions import gradient_wheel, maxColor, turn_right, turn_left, randColor, randColorRange
from dudek.triangle import get_ring, tri_in_direction, all_corners, all_centers
from grid.cell import Coordinate
from .showbase import ShowBase


class Gear:
    def __init__(self, grid, pos):
        self.grid = grid
        self.size = choice([1, 2, 3])
        self.dir = 3
        self.turn = self.size % 2
        self.pos = pos
        self.colorchurn = randint(25, 100)

    def draw_gear(self, color, clock):
        color += (self.size * 100)
        wc = gradient_wheel(color)
        try:
            self.grid.set(Coordinate(*self.pos), HSV(*wc))  # Draw the center
        except Exception:
            pass
        # Draw the rest of the rings
        for r in range(self.size):
            col = (color + (r * self.colorchurn)) % maxColor
            for coord in get_ring(self.pos, r):
                wh = gradient_wheel(col)
                try:
                    self.grid.set(Coordinate(*coord), HSV(*wh))
                except Exception:
                    pass
        # Draw the outside gear
        ring_cells = get_ring(self.pos, self.size)
        num_cells = len(ring_cells)
        for i in range(num_cells):
            col = (color + (self.size * self.colorchurn)) % maxColor
            if (i + clock) % 2 == 0:
                wh = gradient_wheel(col)
                for c in ring_cells[i]:
                    try:
                        self.grid.set(Coordinate(*c), HSV(*wh))
                    except Exception:
                        pass

    def move_gear(self):
        self.pos = tri_in_direction(self.pos, self.dir, 2)
        self.dir = turn_right(self.dir) if self.turn == 1 else turn_left(self.dir)


class Gears(ShowBase):
    def __init__(self, grid, frame_delay=0.25):
        self.frame_delay = frame_delay
        self.grid = grid
        self.gears: List[Gear] = []
        self.clock = 10000
        self.color = randColor()

    def next_frame(self):

        self.gears.extend([Gear(grid=self.grid, pos=coord) for coord in all_corners() + all_centers()])

        while True:
            self.grid.clear()

            for g in self.gears:
                g.draw_gear(self.color, self.clock)
                g.move_gear()

            self.clock += 1

            self.color = randColorRange(self.color, 30)

            yield self.frame_delay
