from PySide2.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy
from PySide2.QtCore import Qt
from .board_render import AztecDiamondRenderer


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle('Magic Square Dance')
        layout = QHBoxLayout()
        right_widget = QWidget()
        right_widget.setLayout(QVBoxLayout())
        self.next_step_button = QPushButton('Next step\n(move then fill)')
        self.advance_magic_button = QPushButton('Move dominoes\n(expand the board)')
        self.fill_holes_button = QPushButton('Fill or re-roll holes')
        self.next_step_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.advance_magic_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.fill_holes_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.renderer = AztecDiamondRenderer()
        layout.addWidget(self.renderer, Qt.AlignVCenter)
        right_widget.layout().addWidget(self.next_step_button)
        right_widget.layout().addWidget(self.advance_magic_button)
        right_widget.layout().addWidget(self.fill_holes_button)
        layout.addWidget(right_widget)
        self.setLayout(layout)
        self.next_step_button.clicked.connect(lambda: (self.renderer.advance_magic(), self.renderer.fill_holes()))
        self.advance_magic_button.clicked.connect(self.renderer.advance_magic)
        self.fill_holes_button.clicked.connect(self.renderer.fill_holes)
        self.advance_magic_button.clicked.connect(lambda: self.next_step_button.setEnabled(False))
        self.advance_magic_button.clicked.connect(lambda: self.advance_magic_button.setEnabled(False))
        self.fill_holes_button.clicked.connect(lambda: self.next_step_button.setEnabled(True))
        self.fill_holes_button.clicked.connect(lambda: self.advance_magic_button.setEnabled(True))
        self.renderer.boardChanged.connect(self.adjustSize())
