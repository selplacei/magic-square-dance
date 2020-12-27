from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Qt, QRectF, QTimer, Signal, QSize
from PySide2.QtGui import QPainter, QBrush, QPen, QColor

import board


class AztecDiamondRenderer(QWidget):
    BORDER = QColor(200, 80, 20)

    square_colors = {
        (board.BLACK, board.NO_COLOR): QColor(0x101010),
        (board.WHITE, board.NO_COLOR): QColor(0x101010)
    }
    for color, value in {
        board.GRAY: (120, 120, 120),
        board.RED: (190, 90, 90),
        board.YELLOW: (190, 190, 90),
        board.GREEN: (90, 190, 90),
        board.BLUE: (90, 90, 190),
    }.items():
        square_colors[board.BLACK, color] = QColor(*map(lambda n: max(0, n - 20), value))
        square_colors[board.WHITE, color] = QColor(*map(lambda n: min(255, n + 20), value))

    boardChanged = Signal(QSize)

    def __init__(self, board_data=None, parent=None):
        super().__init__(parent=parent)
        self.board = board.Board(2)
        self.holes = []
        self.square_size = 20
        self.boardChanged.connect(self.recalculate_holes)
        self.adjust_minimum_size()
        self.boardChanged.emit(self.minimumSize())

    def recalculate_holes(self):
        self.holes = self.board.get_holes()

    def advance_magic(self):
        self.board.advance_magic()
        self.adjust_minimum_size()
        self.boardChanged.emit(self.minimumSize())
        self.repaint()

    def adjust_minimum_size(self):
        board_radius = len(self.board.data) // 2
        self.setMinimumSize(board_radius * 2 * self.square_size, board_radius * 2 * self.square_size)

    def paintEvent(self, event):
        if not self.board:
            return
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        board_radius = len(self.board.data) // 2
        for y in range(-board_radius, board_radius):
            for x in range(-board_radius, board_radius):
                if x == 0 and y == 0:
                    painter.setBrush(QBrush(QColor(255, 255, 255)))
                else:
                    painter.setBrush(QBrush(
                        self.square_colors[self.board.get_square_parity(x, y), self.board.get_square_color(x, y)]
                    ))
                painter.drawRect(QRectF(
                    (x + board_radius) * self.square_size, (y + board_radius) * self.square_size,
                    self.square_size, self.square_size
                ))
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QBrush(self.BORDER), self.square_size / 10))
        for x, y in self.holes:
            painter.drawRect(QRectF(
                (x + board_radius) * self.square_size, (y + board_radius) * self.square_size,
                self.square_size * 2, self.square_size * 2
            ))
