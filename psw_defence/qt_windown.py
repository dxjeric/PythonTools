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
        self.randomPW = PassWordRandom()  # 随机新密码
        self.encryptData = EnCryptData()  # 加密处理
        self.PushButton_SelPWFile.clicked.connect(self.onSelectEcryptFile)
        self.RadioButton_ShowPW.clicked.connect(self.OnChangeShowPassWord)
        self.PushButton_Random_New.clicked.connect(self.OnRandomNewPassWord)

    def OnChangeShowPassWord(self, selected):
        if selected:
            self.LineEditPassWord.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.LineEditPassWord.setEchoMode(QtWidgets.QLineEdit.Password)

    def onSelectEcryptFile(self):
        fileDialog = QtWidgets.QFileDialog.getOpenFileName(
            self, "选择文件", "./", "All File(*);;EnCrypt File(*.ecdb)")
        self.TextEdit_PWFile.setText(fileDialog[0])

    def OnRandomNewPassWord(self):
        b_n = self.CheckBox_Num.isChecked()
        b_o = self.CheckBox_Other.isChecked()
        psw_len = int(self.SpinBox_PSWLen.text())
        new_pw = self.randomPW.randomPassword(psw_len, b_n, b_o)
        self.LineEdit_PassWord_New.setText(new_pw)


# self.LineEditPassWord.setText("1231231231")
# self.TextEdit_PWFile.setText("1231231231")
# tmp_data = self.TextEdit_PWFile.toPlainText()
# tmp_data = self.LineEditPassWord.text()
# print("tmp_data", tmp_data)
# msg_box = QtWidgets.QMessageBox(self)
# msg_box.setText("就是这个!")
# msg_box.setWindowTitle("密码盾")
# msg_box.setStyleSheet("QLabel{min-width: 150px;min-height: 50px;}")
# msg_box.show()

app = QtWidgets.QApplication(sys.argv)
window = QT_MainWindow()
window.show()
app.exec_()
