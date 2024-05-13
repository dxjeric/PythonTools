import sys
from PyQt5 import QtWidgets, QtCore
# from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from psw_defence_GUI import Ui_mainWindow
from psw_data_mgr import PassWordRandom, EnCryptData


class QT_MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):

    def __init__(self, parent=None):
        super(QT_MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.randomPW = PassWordRandom()
        self.encryptData = EnCryptData()
        self.PushButton_SelPWFile.clicked.connect(self.selectEcryptFile)

    def selectEcryptFile(self):
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setText("就是这个!")
        msg_box.setWindowTitle("密码盾")
        msg_box.setStyleSheet("QLabel{min-width: 150px;min-height: 50px;}")
        msg_box.show()


app = QtWidgets.QApplication(sys.argv)
window = QT_MainWindow()
window.show()
app.exec_()
