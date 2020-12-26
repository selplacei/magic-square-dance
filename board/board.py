from collections import OrderedDict
from math import ceil, floor
from typing import Dict, List, NewType, Optional, Tuple


SquareParity = NewType('SquareKind', int)
SquareColor = NewType('SquareColor', int)

BLACK = SquareParity(0)
WHITE = SquareParity(1)

NO_COLOR = SquareColor(-1)
GRAY = SquareColor(0)
RED = SquareColor(1)
YELLOW = SquareColor(2)
GREEN = SquareColor(3)
BLUE = SquareColor(4)


class Board:
    """
    Data representation of an Aztec Diamond board.

    The board, stored in the ``data`` field, is as a list of dicts, where each dict represents a row. Only black
    squares are stored. The keys represent the absolute X coordinate of their square.

    Every square has a parity of either black or white. A square is black if the sum of its X and Y coordinates is even;
    in other words, there is a checkerboard pattern starting with a black square at (0, 0).
    It's valid to use the coordinates of a white square anywhere that coordinates are expected.

    Every square has a color, which it shares with the other part of its domino if it has one.
    If the coordinates are outside of the board, the reported color is NO_COLOR.
    If a square is not part of a domino, its color is GRAY.
    If the domino is vertical and the top square is black, its color is YELLOW; otherwise, it's RED.
    If the domino is horizontal and the left square is black, its color is BLUE; otherwise, it's GREEN.
    """
    def __init__(self, height, init_data=True):
        if height % 2 != 0 or height <= 1:
            raise ValueError('The height of an Aztec Diamond board must be an even number greater than 1.')
        self.data: List[Dict[int, SquareColor]] = []
        if init_data:
            if height == 2:
                self.data = [{0: GRAY, 1: GRAY}, {0: GRAY, 1: GRAY}]
            else:
                offset = height // 2 - 1
                for i in range(height):
                    self.data.append(OrderedDict())
                    for j in range(offset, height - offset, 1):
                        self.data[i][j] = GREEN if i < height / 2 and height % 2 == 0 else BLUE
                    if len(self.data) < height / 2:
                        offset -= 1
                    elif len(self.data) > height / 2:
                        offset += 1

    @staticmethod
    def get_square_parity(x, y) -> SquareParity:
        return (x + y) % 2  # 0 = BLACK, 1 = WHITE

    def get_square_color(self, x, y) -> SquareColor:
        if self.get_square_parity(x, y) == BLACK:
            if 0 <= y < len(self.data) and x in self.data[y]:
                return self.data[y][x]
            return NO_COLOR
        else:
            neighbor = self.get_square_neighbor(x, y)
            if neighbor:
                return self.get_square_color(*neighbor)
            elif all(self.get_square_color(x + x2, y + y2) != NO_COLOR for x2, y2 in ((0, -1), (0, 1), (-1, 0), (1, 0))):
                return GRAY
            return NO_COLOR

    def get_square_neighbor(self, x, y) -> Optional[Tuple[int, int]]:
        """Returns None if the square is gray or invalid. Always returns valid coordinates otherwise."""
        parity = self.get_square_parity(x, y)
        if parity == BLACK:
            color = self.get_square_color(x, y)
            if color == RED:
                return x, y + (1 if parity == WHITE else -1)
            elif color == YELLOW:
                return x, y + (1 if parity == BLACK else -1)
            elif color == GREEN:
                return x + (1 if parity == WHITE else -1), y
            elif color == BLUE:
                return x + (1 if parity == BLACK else -1), y
            return None
        else:
            for x2, y2, target_color in ((x, y - 1, YELLOW), (x, y + 1, RED), (x - 1, y, BLUE), (x + 1, y, GREEN)):
                if self.get_square_color(x2, y2) == target_color:
                    return x2, y2
            return None

    def get_holes(self) -> List[Tuple[int, int]]:
        """Returns all 2x2 areas of gray squares as the self.data indices of their top black square, X first."""
        # A 2x2 hole is represented in self.data by either two consecutive gray squares within a dict
        # or by two gray squares in consecutive dicts whose indices are consecutive, and the index
        # corresponding to the upper row is odd.
        corners = []
        current_row = 0
        unvisited = [list(filter(lambda k: self.data[i][k] == GRAY, r.keys())) for i, r in enumerate(self.data)]
        while unvisited:
            for x in list(filter(lambda n: n % 2 == 0, unvisited[0])):
                other = x - 1 if x - 1 in unvisited[0] else x + 1
                corners.append((x, current_row))
                unvisited[0].remove(x)
                unvisited[0].remove(other)
            while unvisited[0]:
                # Elements of unvisited[0] are guaranteed to be odd at this point
                x = unvisited[0].pop(0)
                other = x - 1 if x - 1 in unvisited[1] else x + 1
                corners.append((x, current_row))
                unvisited[1].remove(other)
            unvisited.pop(0)
            current_row += 1
        return corners

    def fill_holes(self, holes: List[Tuple[int, int]]):
        """Fills holes at indices returned by ``get_holes()`` with a random arrangement of dominoes."""
        pass

    def next_board(self) -> 'Board':
        """Performs necessary movement and deletion of dominoes according to current data and returns a new
        instance of Board. ``fill_holes()`` will not be called by this method."""
        pass
