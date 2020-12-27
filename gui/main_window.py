from PySide2.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from .board_render import AztecDiamondRenderer


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QHBoxLayout()
        right_widget = QWidget()
        right_widget.setLayout(QVBoxLayout())
        self.advance_magic_button = QPushButton('Advance board')
        self.fill_holes_button = QPushButton('Fill holes')
        self.renderer = AztecDiamondRenderer()
        layout.addWidget(self.renderer)
        right_widget.layout().addWidget(self.advance_magic_button)
        right_widget.layout().addWidget(self.fill_holes_button)
        layout.addWidget(right_widget)
        self.setLayout(layout)
        self.advance_magic_button.clicked.connect(self.renderer.advance_magic)
        self.fill_holes_button.clicked.connect(self.renderer.fill_holes)
        self.renderer.boardChanged.connect(self.adjustSize())
