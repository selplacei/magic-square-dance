from collections import OrderedDict
from math import ceil, floor
from typing import Dict, List, NewType, Optional, Tuple


SquareParity = NewType('SquareParity', int)
SquareColor = NewType('SquareColor', int)
FillStrategy = NewType('FillStrategy', int)

BLACK = SquareParity(0)
WHITE = SquareParity(1)

NO_COLOR = SquareColor(-1)
GRAY = SquareColor(0)
RED = SquareColor(1)
YELLOW = SquareColor(2)
GREEN = SquareColor(3)
BLUE = SquareColor(4)

ALL_GRAY = FillStrategy(0)
HORIZONTAL = FillStrategy(1)
VERTICAL = FillStrategy(2)


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
        self.data: Dict[int, Dict[int, SquareColor]]
        self.polarity = 1
        if init_data:
            self.data = self.generate_data(height, fill_strategy=HORIZONTAL)
        else:
            self.data = OrderedDict()

    @staticmethod
    def generate_data(height, fill_strategy=ALL_GRAY) -> Dict[int, Dict[int, SquareColor]]:
        data = OrderedDict()
        colors = {
            ALL_GRAY: (GRAY, GRAY),
            HORIZONTAL: (GREEN, BLUE) if height % 4 == 0 else (BLUE, GREEN),
            VERTICAL: NotImplemented
        }[fill_strategy]
        offset = -1
        for i in range(-height // 2, height // 2):
            data[i] = OrderedDict()
            for j in range(offset, offset * -1):
                if (j + i) % 2 == 0:
                    data[i][j] = colors[0] if i < 0 else colors[1]
            if len(data) < height / 2:
                offset -= 1
            elif len(data) > height / 2:
                offset += 1
        return data

    @staticmethod
    def get_square_parity(x, y) -> SquareParity:
        return (x + y) % 2  # 0 = BLACK, 1 = WHITE

    def get_square_color(self, x, y) -> SquareColor:
        if self.get_square_parity(x, y) == BLACK:
            radius = len(self.data) // 2
            if -radius <= y < radius and x in self.data[y]:
                return self.data[y][x]
            return NO_COLOR
        elif len(self.data) == 2:
            neighbor = self.get_square_neighbor(x, y)
            if neighbor:
                return self.get_square_color(*neighbor)
            return GRAY
        else:
            orientation = 1 if len(self.data) % 4 == 0 else -1
            neighbor = self.get_square_neighbor(x, y)
            if neighbor:
                return self.get_square_color(*neighbor)
            elif (
                self.get_square_color(x + orientation, y) != NO_COLOR and self.get_square_color(x, y + 1) != NO_COLOR
            ) or (
                self.get_square_color(x, y - 1) != NO_COLOR and self.get_square_color(x - orientation, y) != NO_COLOR
            ):
                return GRAY
            return NO_COLOR

    def get_square_neighbor(self, x, y) -> Optional[Tuple[int, int]]:
        """Returns None if the square is gray or invalid. Always returns valid coordinates otherwise."""
        parity = self.get_square_parity(x, y)
        if parity == BLACK:
            color = self.get_square_color(x, y)
            if color == RED:
                return x, y - self.polarity
            elif color == YELLOW:
                return x, y + self.polarity
            elif color == GREEN:
                return x - self.polarity, y
            elif color == BLUE:
                return x + self.polarity, y
            return None
        else:
            for x2, y2, target_color in (
                (x, y - self.polarity, YELLOW),
                (x, y + self.polarity, RED),
                (x - self.polarity, y, BLUE),
                (x + self.polarity, y, GREEN)
            ):
                if self.get_square_color(x2, y2) == target_color:
                    return x2, y2
            return None

    def get_holes(self) -> List[Tuple[int, int]]:
        """Returns all 2x2 areas of gray squares as coordinates of their top left corner. Assumes a valid board.
        Return values for invalid boards are undefined."""
        # In self.data, a hole corresponds to two gray squares that are immediately diagonal of each other.
        corners = []
        current_row = 0
        rows, unvisited = map(list, zip(*(
            (i, list(filter(lambda k: self.data[i][k] == GRAY, r.keys()))) for i, r in self.data.items()
        )))
        while unvisited:
            while unvisited[0]:
                if unvisited[0][0] - 1 in unvisited[1]:
                    corners.append((unvisited[0][0] - 1, rows[current_row]))
                    unvisited[1].remove(unvisited[0][0] - 1)
                else:
                    corners.append((unvisited[0][0], rows[current_row]))
                    unvisited[1].remove(unvisited[0][0] + 1)
                unvisited[0].pop(0)
            unvisited.pop(0)
            current_row += 1
        return corners

    def fill_holes(self, holes: List[Tuple[int, int]]):
        """Fills holes at coordinates returned by ``get_holes()`` with a random arrangement of dominoes."""
        pass

    def advance_magic(self):
        """Performs necessary movement and deletion of dominoes according to current data and changes the board size.
        ``fill_holes()`` will not be called by this method."""
        new_data = self.generate_data(len(self.data) + 2)
        color_delta = {
            RED: (1, -self.polarity),
            YELLOW: (-1, self.polarity),
            BLUE: (self.polarity, -1),
            GREEN: (-self.polarity, 1),
            GRAY: (0, 0)
        }
        for y, row in self.data.items():
            for x, color in row.items():
                new_x = x + color_delta[color][0]
                new_y = y + color_delta[color][1]
                if new_data[new_y][new_x] == GRAY:
                    new_data[new_y][new_x] = color
                else:
                    new_data[new_y][new_x] = GRAY
        self.data = new_data
        self.polarity *= -1
