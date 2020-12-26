from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QPainter, QBrush, QPen, QColor

import adboard


class AztecDiamondRenderer(QWidget):
    BORDER = QColor(20, 20, 20)

    square_colors = {
        (adboard.BLACK, adboard.NO_COLOR): QColor(0x101010),
        (adboard.WHITE, adboard.NO_COLOR): QColor(0x101010)
    }
    for color, value in {
        adboard.GRAY: (120, 120, 120),
        adboard.RED: (255, 0, 0),
        adboard.YELLOW: (255, 255, 0),
        adboard.GREEN: (0, 255, 0),
        adboard.BLUE: (0, 0, 255),
    }.items():
        square_colors[adboard.BLACK, color] = QColor(*map(lambda n: max(0, n - 20), value))
        square_colors[adboard.WHITE, color] = QColor(*map(lambda n: min(255, n + 20), value))

    def __init__(self, board=None, parent=None):
        super().__init__(parent=parent)
        self.board = board or adboard.Board(32)
        board_height = len(self.board.data) * 2
        print('\n'.join(map(str, self.board.data)))

    def paintEvent(self, event):
        square_size = 10
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        board_height = len(self.board.data) * 2
        for y in range(board_height):
            for x in range(board_height):
                painter.setBrush(QBrush(
                    self.square_colors[self.board.get_square_parity(x, y), self.board.get_square_color(x, y)]
                ))
                painter.drawRect(QRectF(x * square_size, y * square_size, square_size, square_size))
