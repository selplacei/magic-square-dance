import sys
from PySide2.QtWidgets import QApplication
import rendering

if __name__ == '__main__':
    app = QApplication()
    renderer = rendering.AztecDiamondRenderer()
    renderer.show()
    sys.exit(app.exec_())
