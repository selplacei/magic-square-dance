from PySide2.QtWidgets import QWidget, QPushButton, QHBoxLayout
from .board_render import AztecDiamondRenderer


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QHBoxLayout()
        self.advance_magic_button = QPushButton('Advance board')
        self.renderer = AztecDiamondRenderer()
        layout.addWidget(self.renderer)
        layout.addWidget(self.advance_magic_button)
        self.setLayout(layout)
        self.advance_magic_button.clicked.connect(self.renderer.advance_magic)
        self.renderer.boardChanged.connect(self.adjustSize())
