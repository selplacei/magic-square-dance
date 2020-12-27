from PySide2.QtWidgets import QWidget, QSizePolicy, QOpenGLWidget
from PySide2.QtCore import Qt, QRectF, QTimer, Signal, QSize, Slot, QPointF
from PySide2.QtGui import QPainter, QBrush, QPen, QColor

import board


class AztecDiamondRenderer(QOpenGLWidget):
    HOLE_BORDER = QColor(210, 210, 210)
    DOMINO_BORDER = QColor(30, 30, 30)
    ARROWS = QColor(140, 140, 140)

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
    skipaheadProgress = Signal(int)
    skipaheadComplete = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.board = board.Board(2)
        self.holes = []
        self.base_square_size = 500
        self.hole_borders_enabled = True
        self.domino_borders_enabled = True
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

    def advance_magic(self, repaint=True):
        self.board.advance_magic()
        self.boardChanged.emit(self.minimumSize())
        if repaint:
            self.repaint()

    def skip_ahead(self, n):
        for i in range(n):
            self.board.advance_magic()
            self.recalculate_holes()
            self.board.fill_holes(self.holes)
            self.skipaheadProgress.emit(i)
        self.skipaheadComplete.emit()
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
        painter.setBrush(self.palette().color(self.backgroundRole()))
        painter.drawRect(self.rect())
        board_radius = len(self.board.data) // 2
        square_size = self.base_square_size / board_radius / 2
        offset_x = self.size().width() // 2
        offset_y = self.size().height() // 2
        for y in range(-board_radius, board_radius):
            for x in range(-board_radius, board_radius):
                if (color := self.board.get_square_color(x, y)) != board.NO_COLOR:
                    painter.setBrush(QBrush(self.square_colors[
                        self.board.get_square_parity(x, y) if self.checkerboard_enabled else board.BLACK, color
                    ]))
                    painter.drawRect(QRectF(
                        x * square_size + offset_x, y * square_size + offset_y,
                        square_size + 0.5, square_size + 0.5
                    ))
        if self.domino_borders_enabled:
            painter.setPen(QPen(QBrush(self.DOMINO_BORDER), max(1, int(square_size / 20))))
            painter.setBrush(Qt.NoBrush)
            for y in range(-board_radius, board_radius):
                for x in range(-board_radius, board_radius):
                    if self.board.get_square_parity(x, y) == board.BLACK and (other := self.board.get_square_neighbor(x, y)):
                        painter.drawRect(QRectF(
                            min(x, other[0]) * square_size + offset_x, min(y, other[1]) * square_size + offset_y,
                            max(other[0] - x + 1, x - other[0] + 1) * square_size,
                            max(other[1] - y + 1, y - other[1] + 1) * square_size
                        ))
        if self.hole_borders_enabled:
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(QBrush(self.HOLE_BORDER), square_size / 10))
            for x, y in self.holes:
                painter.drawRect(QRectF(
                    x * square_size + offset_x, y * square_size + offset_y,
                    square_size * 2, square_size * 2
                ))
        if self.domino_arrows_enabled:
            painter.setBrush(QBrush(self.ARROWS))
            painter.setPen(Qt.NoPen)
            for y in range(-board_radius, board_radius):
                for x in range(-board_radius, board_radius):
                    if self.board.get_square_parity(x, y) == board.BLACK:
                        color = self.board.get_square_color(x, y)
                        radius = square_size / 6
                        if color == board.BLUE:
                            center_x = (self.board.polarity + 1) * square_size / 2 + x * square_size + offset_x
                            center_y = y * square_size + square_size / 2 + offset_y
                            painter.drawConvexPolygon([
                                QPointF(center_x - radius, center_y + radius),
                                QPointF(center_x, center_y - radius),
                                QPointF(center_x + radius, center_y + radius)
                            ])
                        elif color == board.GREEN:
                            center_x = (self.board.polarity * -1 + 1) * square_size / 2 + x * square_size + offset_x
                            center_y = y * square_size + square_size / 2 + offset_y
                            painter.drawConvexPolygon([
                                QPointF(center_x - radius, center_y - radius),
                                QPointF(center_x, center_y + radius),
                                QPointF(center_x + radius, center_y - radius)
                            ])
                        elif color == board.YELLOW:
                            center_y = (self.board.polarity + 1) * square_size / 2 + y * square_size + offset_y
                            center_x = x * square_size + square_size / 2 + offset_x
                            painter.drawConvexPolygon([
                                QPointF(center_x + radius, center_y + radius),
                                QPointF(center_x - radius, center_y),
                                QPointF(center_x + radius, center_y - radius)
                            ])
                        elif color == board.RED:
                            center_y = (self.board.polarity * -1 + 1) * square_size / 2 + y * square_size + offset_y
                            center_x = x * square_size + square_size / 2 + offset_x
                            painter.drawConvexPolygon([
                                QPointF(center_x - radius, center_y - radius),
                                QPointF(center_x + radius, center_y),
                                QPointF(center_x - radius, center_y + radius)
                            ])

    @Slot(bool)
    def setHoleBordersEnabled(self, value):
        self.hole_borders_enabled = value
        self.repaint()

    @Slot(bool)
    def setDominoBordersEnabled(self, value):
        self.domino_borders_enabled = value
        self.repaint()

    @Slot(bool)
    def setCheckeboardEnabled(self, value):
        self.checkerboard_enabled = value
        self.repaint()

    @Slot(bool)
    def setDominoArrowsEnabled(self, value):
        self.domino_arrows_enabled = value
        self.repaint()
