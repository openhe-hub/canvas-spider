import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from src.ui.test import Ui_Form


class CustomUI(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(CustomUI, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cutomUI = CustomUI()
    cutomUI.show()
    sys.exit(app.exec_())
