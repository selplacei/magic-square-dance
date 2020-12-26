from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QPainter, QBrush, QPen, QColor

import board


class AztecDiamondRenderer(QWidget):
    BORDER = QColor(20, 20, 20)

    square_colors = {
        (board.BLACK, board.NO_COLOR): QColor(0x101010),
        (board.WHITE, board.NO_COLOR): QColor(0x101010)
    }
    for color, value in {
        board.GRAY: (120, 120, 120),
        board.RED: (255, 0, 0),
        board.YELLOW: (255, 255, 0),
        board.GREEN: (0, 255, 0),
        board.BLUE: (0, 0, 255),
    }.items():
        square_colors[board.BLACK, color] = QColor(*map(lambda n: max(0, n - 20), value))
        square_colors[board.WHITE, color] = QColor(*map(lambda n: min(255, n + 20), value))

    def __init__(self, board_data=None, parent=None):
        super().__init__(parent=parent)
        self.board = board_data or board.Board(90)

    def paintEvent(self, event):
        square_size = 10
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        board_height = len(self.board.data)
        for y in range(board_height):
            for x in range(board_height):
                painter.setBrush(QBrush(
                    self.square_colors[self.board.get_square_parity(x, y), self.board.get_square_color(x, y)]
                ))
                painter.drawRect(QRectF(x * square_size, y * square_size, square_size, square_size))
