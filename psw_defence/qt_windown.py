import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from psw_defence_GUI import Ui_mainWindow


class QT_MainWindow(QMainWindow, Ui_mainWindow):

    def __init__(self, parent=None):
        super(QT_MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())


app = QtWidgets.QApplication(sys.argv)
window = QT_MainWindow()
window.show()
app.exec_()
