from typing import List, NewType, Optional, Tuple


SquareParity = NewType('SquareKind', int)
SquareColor = NewType('SquareColor', int)
ArrowDirection = NewType('ArrowDirection', int)

BLACK = SquareParity(0)
WHITE = SquareParity(1)

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

    The board is represented as a 2-dimensional list whose rows represent rows of the board, from top to bottom.
    The first row has width 2. X increases to the right, and Y increases downwards. All rows start at X = 0.

    Every square is either black or white; this is defined as the square's parity.
    The board is in a checkerboard pattern: a square is black if its X coordinate is even.

    Every domino is one of red, yellow, green, or blue. A vertical domino is yellow if its top square is black,
    and is red otherwise. A horizontal domino is blue if its left square is black, and is green otherwise.
    The kind of domino that a square belongs to is defined as the square's color. If it's unfilled, the square is gray.

    Every non-gray has an arrow direction, which indicates where the corresponding domino should go when the board is
    expanded. The arrows are guaranteed to be valid according to domino color, but may face each other. New directions
    are generated when fill_holes() is called.
    """

    def __init__(self, width):
        self.data: List[List[SquareColor]] = []
        self.arrows: List[List[ArrowDirection]] = []  # To avoid redundancy, only stores values of black squares

    def get_square_parity(self, x, y) -> SquareParity:
        pass

    def get_square_color(self, x, y) -> SquareColor:
        pass

    def get_square_neighbor(self, x, y) -> Optional[Tuple[int, int]]:
        """Returns None if the square is gray."""
        pass

    def get_arrow_direction(self, x, y) -> Optional[ArrowDirection]:
        """Returns None if the square is gray."""
        pass

    def fill_holes(self):
        """Fills all 2x2 areas of gray squares with new dominoes and gives them arrow directions."""
        pass

    def next_board(self) -> 'Board':
        """Performs necessary movement and deletion of dominoes according to current data and returns a new
        instance of Board. Its fill_holes() will not be called by this method."""
        pass
