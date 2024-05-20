import sys, hashlib
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
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
        self.PushButton_Save_New.clicked.connect(self.OnSavePassWord)

        self.LineEditPassWord.textChanged.connect(self.OnSecretkeyChanged)
        self.TextEdit_PWFile.textChanged.connect(self.OnEncrypteFileChanged)

    # def keyPressEvent(self, event):
    #     print("key", event.key(), event.text())
    #     if event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier:
    #         sender = self.sender()
    #         sender.undo()
    #         print("sender name: ", sender.text(), sender.getObjectName())
    #         pass

    # 秘钥修改
    def OnSecretkeyChanged(self):
        self.encryptData.changeSecretkey(self.LineEditPassWord.text().encode())
        # print("OnSecretkeyChanged", self.LineEditPassWord.text(), md5_str)

    def OnEncrypteFileChanged(self):
        self.encryptData.changeEncrypteFile(self.TextEdit_PWFile.toPlainText())
        # print("finish", self.TextEdit_PWFile.toPlainText())

    # 是否显示明文密码
    def OnChangeShowPassWord(self, selected):
        if selected:
            self.LineEditPassWord.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.LineEditPassWord.setEchoMode(QtWidgets.QLineEdit.Password)

    # 选择加密文件
    def onSelectEcryptFile(self):
        fileDialog = QtWidgets.QFileDialog.getOpenFileName(
            self, "选择文件", "./", "EnCrypt File(*.ecdb);;All File(*)")
        self.TextEdit_PWFile.setText(fileDialog[0])
        self.encryptData.changeEncrypteFile(fileDialog[0])

    # 随机密码
    def OnRandomNewPassWord(self):
        b_n = self.CheckBox_Num.isChecked()
        b_o = self.CheckBox_Other.isChecked()
        psw_len = int(self.SpinBox_PSWLen.text())
        new_pw = self.randomPW.randomPassword(psw_len, b_n, b_o)
        self.LineEdit_PassWord_New.setText(new_pw)

    # 修改或者新增密码
    def OnSavePassWord(self):
        addr_str = self.LineEdit_Addr_New.text()
        account_str = self.LineEdit_Account_New.text()
        password_str = self.LineEdit_PassWord_New.text()
        other_str = self.TextEdit_Other.toPlainText()
        print(addr_str, account_str, password_str, other_str)


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
