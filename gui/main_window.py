from PySide2.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy, QCheckBox, QLabel, QSpinBox, QProgressBar
)
from PySide2.QtCore import Qt
from .board_render import AztecDiamondRenderer


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle('Magic Square Dance')

        self.hole_borders_toggle = QCheckBox('Show 2x2 hole borders')
        self.domino_borders_toggle = QCheckBox('Show domino borders')
        self.arrows_toggle = QCheckBox('Show domino arrows')
        self.checkerboard_toggle = QCheckBox('Show checkerboard pattern')
        self.skip_ahead_label = QLabel('Skip ahead by:')
        self.skip_ahead_spinbox = QSpinBox()
        self.skip_ahead_button = QPushButton('Go')
        self.skip_ahead_progressbar = QProgressBar()
        self.next_step_button = QPushButton('Next step\n(move then fill)')
        self.advance_magic_button = QPushButton('Move dominoes\n(expand the board)')
        self.fill_holes_button = QPushButton('Fill or re-roll holes\n(press as many\ntimes as you like)')
        self.renderer = AztecDiamondRenderer()

        for checkbox in (
            self.hole_borders_toggle, self.domino_borders_toggle, self.arrows_toggle, self.checkerboard_toggle
        ):
            checkbox.setChecked(True)
        self.skip_ahead_label.setBuddy(self.skip_ahead_spinbox)
        self.next_step_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.advance_magic_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.fill_holes_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QHBoxLayout()
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        skipahead_widget = QWidget()
        skipahead_layout = QHBoxLayout()
        layout.addWidget(self.renderer, Qt.AlignVCenter)
        right_layout.addWidget(self.hole_borders_toggle)
        right_layout.addWidget(self.domino_borders_toggle)
        right_layout.addWidget(self.arrows_toggle)
        right_layout.addWidget(self.checkerboard_toggle)
        skipahead_layout.setContentsMargins(0, 0, 0, 0)
        skipahead_layout.addWidget(self.skip_ahead_label)
        skipahead_layout.addWidget(self.skip_ahead_spinbox)
        skipahead_layout.addWidget(self.skip_ahead_button)
        skipahead_widget.setLayout(skipahead_layout)
        skipahead_wrapper = QWidget()
        skipahead_wrapper.setLayout(QVBoxLayout())
        skipahead_wrapper.layout().setContentsMargins(0, 0, 0, 0)
        skipahead_wrapper.layout().addWidget(skipahead_widget)
        skipahead_wrapper.layout().addWidget(self.skip_ahead_progressbar)
        right_layout.addWidget(skipahead_wrapper)
        right_layout.addWidget(self.next_step_button)
        right_layout.addWidget(self.advance_magic_button)
        right_layout.addWidget(self.fill_holes_button)
        right_widget.setLayout(right_layout)
        layout.addWidget(right_widget)
        self.setLayout(layout)

        self.hole_borders_toggle.stateChanged.connect(self.renderer.setHoleBordersEnabled)
        self.domino_borders_toggle.stateChanged.connect(self.renderer.setDominoBordersEnabled)
        self.checkerboard_toggle.stateChanged.connect(self.renderer.setCheckeboardEnabled)
        self.next_step_button.clicked.connect(
            lambda: (self.renderer.advance_magic(repaint=False), self.renderer.fill_holes())
        )
        self.advance_magic_button.clicked.connect(self.renderer.advance_magic)
        self.fill_holes_button.clicked.connect(self.renderer.fill_holes)
        self.skip_ahead_button.clicked.connect(lambda: self.renderer.skip_ahead(self.skip_ahead_spinbox.value()))
        self.skip_ahead_button.clicked.connect(
            lambda: self.skip_ahead_progressbar.setMaximum(self.skip_ahead_spinbox.value() - 1)
        )
        self.renderer.skipaheadProgress.connect(self.skip_ahead_progressbar.setValue)
        self.renderer.skipaheadComplete.connect(self.skip_ahead_progressbar.reset)
        self.advance_magic_button.clicked.connect(lambda: self.next_step_button.setEnabled(False))
        self.advance_magic_button.clicked.connect(lambda: self.advance_magic_button.setEnabled(False))
        self.advance_magic_button.clicked.connect(lambda: self.skip_ahead_button.setEnabled(False))
        self.fill_holes_button.clicked.connect(lambda: self.next_step_button.setEnabled(True))
        self.fill_holes_button.clicked.connect(lambda: self.advance_magic_button.setEnabled(True))
        self.fill_holes_button.clicked.connect(lambda: self.skip_ahead_button.setEnabled(False))
        self.renderer.boardChanged.connect(self.adjustSize())
