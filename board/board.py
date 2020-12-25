from typing import Dict, List, NewType, Optional, Tuple


SquareParity = NewType('SquareKind', int)
SquareColor = NewType('SquareColor', int)
ArrowDirection = NewType('ArrowDirection', int)

BLACK = SquareParity(0)
WHITE = SquareParity(1)

NO_COLOR = SquareColor(-1)
GRAY = SquareColor(0)
RED = SquareColor(1)
YELLOW = SquareColor(2)
GREEN = SquareColor(3)
BLUE = SquareColor(4)

ARROW_UP = ArrowDirection(0)
ARROW_RIGHT = ArrowDirection(1)
ARROW_DOWN = ArrowDirection(2)
ARROW_LEFT = ArrowDirection(3)


class Board:
    """
    Data representation of an Aztec Board.

    The board, stored in the `data` field, is as a list of dicts, where each dict represents two rows and each element
    of a dict is the X coordinate of a valid black square mapped to a tuple of the square's color and arrow direction.
    The first dict corresponds to Y coordinates 0 and 1. Y increases downwards.

    Every square has a parity of either black or white. A square is black if the sum of its X and Y coordinates is even;
    in other words, there is a checkerboard pattern starting with a black square at (0, 0). White squares are not stored
    to avoid redundancy, but it's valid to use the coordinates of a white square anywhere that coordinates are expected.

    Every square has a color, which it shares with the other part of its domino if it has one.
    If the coordinates are outside of the board, its color is NO_COLOR.
    If a valid square is not part of a domino, its color is GRAY.
    If the domino is vertical and the top square is black, its color is YELLOW; otherwise, it's RED.
    If the domino is horizontal and the left square is black, its color is BLUE; otherwise, it's GREEN.

    Every valid non-gray square has an arrow direction, which indicates where the domino moves for the next board.
    """
    def __init__(self, width):
        self.data: List[Dict[int, Tuple[SquareColor, Optional[ArrowDirection]]]] = []

    @staticmethod
    def get_square_parity(x, y) -> SquareParity:
        return (x + y) % 2  # 0 = BLACK, 1 = WHITE

    def get_square_color(self, x, y) -> SquareColor:
        if not (0 <= y // 2 < len(self.data) and x in self.data[y // 2]):
            return NO_COLOR
        elif self.get_square_parity(x, y) == BLACK:
            return self.data[y // 2][x][0]
        else:
            neighbor = self.get_square_neighbor(x, y)
            return self.data[neighbor[1] // 2][neighbor[0]][0]

    def get_square_neighbor(self, x, y) -> Optional[Tuple[int, int]]:
        """Returns None if the square is gray or invalid. Always returns valid coordinates otherwise."""
        color = self.get_square_color(x, y)
        parity = self.get_square_parity(x, y)
        if color == RED:
            return x, y + (1 if parity == WHITE else -1)
        elif color == YELLOW:
            return x, y + (1 if parity == BLACK else -1)
        elif color == GREEN:
            return x + (1 if parity == WHITE else -1), y
        elif color == BLUE:
            return x + (1 if parity == BLACK else -1), y
        return None

    def get_arrow_direction(self, x, y) -> Optional[ArrowDirection]:
        """Returns None if the square is gray or invalid."""
        if self.get_square_color(x, y) in {NO_COLOR, GRAY}:
            return None
        elif self.get_square_parity(x, y) == BLACK:
            return self.data[y // 2][x][1]
        else:
            neighbor = self.get_square_neighbor(x, y)
            return self.data[neighbor[1] // 2][neighbor[0]][1]

    def fill_holes(self):
        """Fills all 2x2 areas of gray squares with new dominoes and gives them arrow directions."""
        pass

    def next_board(self) -> 'Board':
        """Performs necessary movement and deletion of dominoes according to current data and returns a new
        instance of Board. ill_holes() will not be called by this method."""
        pass
