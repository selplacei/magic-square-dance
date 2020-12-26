import sys
from PySide2.QtWidgets import QApplication
import gui

if __name__ == '__main__':
    app = QApplication()
    window = gui.MainWindow()
    window.show()
    sys.exit(app.exec_())
