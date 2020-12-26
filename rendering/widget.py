from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Qt, QRectF, QTimer
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
        board.RED: (190, 90, 90),
        board.YELLOW: (255, 255, 90),
        board.GREEN: (90, 190, 90),
        board.BLUE: (90, 90, 190),
    }.items():
        square_colors[board.BLACK, color] = QColor(*map(lambda n: max(0, n - 20), value))
        square_colors[board.WHITE, color] = QColor(*map(lambda n: min(255, n + 20), value))

    def __init__(self, board_data=None, parent=None):
        super().__init__(parent=parent)
        self.board = None
        # self.board = board_data or board.Board(20)
        self.board_size = 2
        self.change_board()

    def change_board(self):
        self.board = board.Board(self.board_size)
        self.repaint()
        self.board_size += 2

    def paintEvent(self, event):
        if not self.board:
            return
        square_size = 20
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        board_radius = len(self.board.data) // 2
        for y in range(-board_radius, board_radius):
            for x in range(-board_radius, board_radius):
                painter.setBrush(QBrush(
                    self.square_colors[self.board.get_square_parity(x, y), self.board.get_square_color(x, y)]
                ))
                painter.drawRect(QRectF(
                    (x + board_radius) * square_size, (y + board_radius) * square_size, square_size, square_size
                ))
