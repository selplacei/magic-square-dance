from PySide2.QtWidgets import QWidget, QSizePolicy
from PySide2.QtCore import Qt, QRectF, QTimer, Signal, QSize, Slot
from PySide2.QtGui import QPainter, QBrush, QPen, QColor

import board


class AztecDiamondRenderer(QWidget):
    BORDER = QColor(255, 255, 255)

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
        square_colors[board.BLACK, color] = QColor(*map(lambda n: max(0, n - 10), value))
        square_colors[board.WHITE, color] = QColor(*map(lambda n: min(255, n + 10), value))

    boardChanged = Signal(QSize)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.board = board.Board(2)
        self.holes = []
        self.base_square_size = 500
        self.hole_borders_enabled = True
        self.domino_arrows_enabled = True
        self.checkerboard_enabled = True
        self.setMinimumSize(self.base_square_size, self.base_square_size)
        policy = self.sizePolicy()
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)
        self.boardChanged.connect(self.recalculate_holes)
        self.boardChanged.emit(self.minimumSize())

    def recalculate_holes(self):
        self.holes = self.board.get_holes()

    def advance_magic(self):
        self.board.advance_magic()
        self.boardChanged.emit(self.minimumSize())
        self.repaint()

    def fill_holes(self):
        self.board.fill_holes(self.holes)
        self.repaint()

    def paintEvent(self, event):
        if not self.board:
            return
        self.base_square_size = min(self.size().width(), self.size().height())
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        board_radius = len(self.board.data) // 2
        square_size = self.base_square_size / board_radius / 2
        offset_x = self.size().width() // 2
        offset_y = self.size().height() // 2
        for y in range(-board_radius, board_radius):
            for x in range(-board_radius, board_radius):
                if (color := self.board.get_square_color(x, y)) != board.NO_COLOR:
                    painter.setBrush(QBrush(
                        self.square_colors[self.board.get_square_parity(x, y), color]
                    ))
                    painter.drawRect(QRectF(
                        x * square_size + offset_x, y * square_size + offset_y,
                        square_size, square_size
                    ))
        if self.hole_borders_enabled:
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(QBrush(self.BORDER), square_size / 10))
            for x, y in self.holes:
                painter.drawRect(QRectF(
                    x * square_size + offset_x, y * square_size + offset_y,
                    square_size * 2, square_size * 2
                ))

    @Slot(bool)
    def setHoleBordersEnabled(self, value):
        self.hole_borders_enabled = value
        self.repaint()
