# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'psw_defence.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.setEnabled(True)
        mainWindow.resize(556, 615)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        mainWindow.setFont(font)
        mainWindow.setStatusTip("")
        mainWindow.setWhatsThis("")
        mainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.GroupBox_Config = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.GroupBox_Config.setFont(font)
        self.GroupBox_Config.setObjectName("GroupBox_Config")
        self.gridLayout = QtWidgets.QGridLayout(self.GroupBox_Config)
        self.gridLayout.setObjectName("gridLayout")
        self.Label_pw = QtWidgets.QLabel(self.GroupBox_Config)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.Label_pw.setFont(font)
        self.Label_pw.setObjectName("Label_pw")
        self.gridLayout.addWidget(self.Label_pw, 0, 0, 1, 1)
        self.LineEditPassWord = QtWidgets.QLineEdit(self.GroupBox_Config)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.LineEditPassWord.setFont(font)
        self.LineEditPassWord.setToolTip("")
        self.LineEditPassWord.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LineEditPassWord.setObjectName("LineEditPassWord")
        self.gridLayout.addWidget(self.LineEditPassWord, 0, 1, 1, 1)
        self.RadioButton_ShowPW = QtWidgets.QRadioButton(self.GroupBox_Config)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.RadioButton_ShowPW.setFont(font)
        self.RadioButton_ShowPW.setObjectName("RadioButton_ShowPW")
        self.gridLayout.addWidget(self.RadioButton_ShowPW, 0, 2, 1, 1)
        self.Lable_PWFile = QtWidgets.QLabel(self.GroupBox_Config)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.Lable_PWFile.setFont(font)
        self.Lable_PWFile.setObjectName("Lable_PWFile")
        self.gridLayout.addWidget(self.Lable_PWFile, 1, 0, 1, 1)
        self.LineEdit_PWFile = QtWidgets.QLineEdit(self.GroupBox_Config)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.LineEdit_PWFile.setFont(font)
        self.LineEdit_PWFile.setToolTip("")
        self.LineEdit_PWFile.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LineEdit_PWFile.setObjectName("LineEdit_PWFile")
        self.gridLayout.addWidget(self.LineEdit_PWFile, 1, 1, 1, 1)
        self.PushButton_SelPWFile = QtWidgets.QPushButton(self.GroupBox_Config)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.PushButton_SelPWFile.setFont(font)
        self.PushButton_SelPWFile.setCheckable(False)
        self.PushButton_SelPWFile.setAutoDefault(False)
        self.PushButton_SelPWFile.setObjectName("PushButton_SelPWFile")
        self.gridLayout.addWidget(self.PushButton_SelPWFile, 1, 2, 1, 1)
        self.gridLayout_3.addWidget(self.GroupBox_Config, 0, 0, 1, 1)
        self.GroupBox_New = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.GroupBox_New.setFont(font)
        self.GroupBox_New.setObjectName("GroupBox_New")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.GroupBox_New)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Label_Addr = QtWidgets.QLabel(self.GroupBox_New)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.Label_Addr.setFont(font)
        self.Label_Addr.setObjectName("Label_Addr")
        self.gridLayout_2.addWidget(self.Label_Addr, 0, 0, 1, 1)
        self.LineEdit_Addr_New = QtWidgets.QLineEdit(self.GroupBox_New)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(13)
        self.LineEdit_Addr_New.setFont(font)
        self.LineEdit_Addr_New.setAcceptDrops(False)
        self.LineEdit_Addr_New.setToolTip("")
        self.LineEdit_Addr_New.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LineEdit_Addr_New.setObjectName("LineEdit_Addr_New")
        self.gridLayout_2.addWidget(self.LineEdit_Addr_New, 0, 1, 1, 1)
        self.CheckBox_Num = QtWidgets.QCheckBox(self.GroupBox_New)
        self.CheckBox_Num.setChecked(True)
        self.CheckBox_Num.setObjectName("CheckBox_Num")
        self.gridLayout_2.addWidget(self.CheckBox_Num, 0, 2, 1, 1)
        self.Label_Account = QtWidgets.QLabel(self.GroupBox_New)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.Label_Account.setFont(font)
        self.Label_Account.setObjectName("Label_Account")
        self.gridLayout_2.addWidget(self.Label_Account, 1, 0, 2, 1)
        self.LineEdit_Account_New = QtWidgets.QLineEdit(self.GroupBox_New)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(13)
        self.LineEdit_Account_New.setFont(font)
        self.LineEdit_Account_New.setAcceptDrops(False)
        self.LineEdit_Account_New.setToolTip("")
        self.LineEdit_Account_New.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LineEdit_Account_New.setObjectName("LineEdit_Account_New")
        self.gridLayout_2.addWidget(self.LineEdit_Account_New, 1, 1, 2, 1)
        self.CheckBox_Char = QtWidgets.QCheckBox(self.GroupBox_New)
        self.CheckBox_Char.setChecked(True)
        self.CheckBox_Char.setObjectName("CheckBox_Char")
        self.gridLayout_2.addWidget(self.CheckBox_Char, 1, 2, 1, 1)
        self.CheckBox_Other = QtWidgets.QCheckBox(self.GroupBox_New)
        self.CheckBox_Other.setChecked(True)
        self.CheckBox_Other.setObjectName("CheckBox_Other")
        self.gridLayout_2.addWidget(self.CheckBox_Other, 2, 2, 1, 1)
        self.Label_PW = QtWidgets.QLabel(self.GroupBox_New)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.Label_PW.setFont(font)
        self.Label_PW.setObjectName("Label_PW")
        self.gridLayout_2.addWidget(self.Label_PW, 3, 0, 1, 1)
        self.LineEdit_PassWord_New = QtWidgets.QLineEdit(self.GroupBox_New)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.LineEdit_PassWord_New.setFont(font)
        self.LineEdit_PassWord_New.setAcceptDrops(False)
        self.LineEdit_PassWord_New.setToolTip("")
        self.LineEdit_PassWord_New.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LineEdit_PassWord_New.setObjectName("LineEdit_PassWord_New")
        self.gridLayout_2.addWidget(self.LineEdit_PassWord_New, 3, 1, 1, 1)
        self.PushButton_Random_New = QtWidgets.QPushButton(self.GroupBox_New)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.PushButton_Random_New.setFont(font)
        self.PushButton_Random_New.setCheckable(False)
        self.PushButton_Random_New.setAutoDefault(False)
        self.PushButton_Random_New.setObjectName("PushButton_Random_New")
        self.gridLayout_2.addWidget(self.PushButton_Random_New, 3, 2, 1, 1)
        self.Label_PW_2 = QtWidgets.QLabel(self.GroupBox_New)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.Label_PW_2.setFont(font)
        self.Label_PW_2.setObjectName("Label_PW_2")
        self.gridLayout_2.addWidget(self.Label_PW_2, 4, 0, 1, 1)
        self.TextEdit_Other = QtWidgets.QTextEdit(self.GroupBox_New)
        self.TextEdit_Other.setObjectName("TextEdit_Other")
        self.gridLayout_2.addWidget(self.TextEdit_Other, 4, 1, 2, 1)
        self.PushButton_Save_New = QtWidgets.QPushButton(self.GroupBox_New)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.PushButton_Save_New.setFont(font)
        self.PushButton_Save_New.setCheckable(False)
        self.PushButton_Save_New.setAutoDefault(False)
        self.PushButton_Save_New.setObjectName("PushButton_Save_New")
        self.gridLayout_2.addWidget(self.PushButton_Save_New, 5, 2, 1, 1)
        self.gridLayout_3.addWidget(self.GroupBox_New, 1, 0, 1, 1)
        self.GroupBox_New_2 = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.GroupBox_New_2.setFont(font)
        self.GroupBox_New_2.setObjectName("GroupBox_New_2")
        self.Label_Addr_2 = QtWidgets.QLabel(self.GroupBox_New_2)
        self.Label_Addr_2.setGeometry(QtCore.QRect(10, 26, 32, 16))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.Label_Addr_2.setFont(font)
        self.Label_Addr_2.setObjectName("Label_Addr_2")
        self.LineEdit_Addr_New_2 = QtWidgets.QLineEdit(self.GroupBox_New_2)
        self.LineEdit_Addr_New_2.setGeometry(QtCore.QRect(48, 26, 351, 26))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(13)
        self.LineEdit_Addr_New_2.setFont(font)
        self.LineEdit_Addr_New_2.setAcceptDrops(False)
        self.LineEdit_Addr_New_2.setToolTip("")
        self.LineEdit_Addr_New_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LineEdit_Addr_New_2.setObjectName("LineEdit_Addr_New_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.GroupBox_New_2)
        self.textBrowser.setGeometry(QtCore.QRect(50, 110, 351, 88))
        self.textBrowser.setAcceptDrops(False)
        self.textBrowser.setObjectName("textBrowser")
        self.Label_Account_2 = QtWidgets.QLabel(self.GroupBox_New_2)
        self.Label_Account_2.setGeometry(QtCore.QRect(10, 58, 32, 16))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.Label_Account_2.setFont(font)
        self.Label_Account_2.setObjectName("Label_Account_2")
        self.LineEdit_Account_New_2 = QtWidgets.QLineEdit(self.GroupBox_New_2)
        self.LineEdit_Account_New_2.setGeometry(QtCore.QRect(48, 58, 351, 26))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(13)
        self.LineEdit_Account_New_2.setFont(font)
        self.LineEdit_Account_New_2.setAcceptDrops(False)
        self.LineEdit_Account_New_2.setToolTip("")
        self.LineEdit_Account_New_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LineEdit_Account_New_2.setObjectName("LineEdit_Account_New_2")
        self.PushButton_Save_New_2 = QtWidgets.QPushButton(self.GroupBox_New_2)
        self.PushButton_Save_New_2.setGeometry(QtCore.QRect(440, 50, 75, 24))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.PushButton_Save_New_2.setFont(font)
        self.PushButton_Save_New_2.setCheckable(False)
        self.PushButton_Save_New_2.setAutoDefault(False)
        self.PushButton_Save_New_2.setObjectName("PushButton_Save_New_2")
        self.Label_Account_3 = QtWidgets.QLabel(self.GroupBox_New_2)
        self.Label_Account_3.setGeometry(QtCore.QRect(10, 140, 32, 16))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.Label_Account_3.setFont(font)
        self.Label_Account_3.setObjectName("Label_Account_3")
        self.gridLayout_3.addWidget(self.GroupBox_New_2, 2, 0, 1, 1)
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "账密盾"))
        self.GroupBox_Config.setTitle(_translate("mainWindow", "配置"))
        self.Label_pw.setText(_translate("mainWindow", "加密秘钥"))
        self.RadioButton_ShowPW.setText(_translate("mainWindow", "显示密码"))
        self.Lable_PWFile.setText(_translate("mainWindow", "密码文件"))
        self.PushButton_SelPWFile.setText(_translate("mainWindow", "选择..."))
        self.GroupBox_New.setTitle(_translate("mainWindow", "新密码"))
        self.Label_Addr.setText(_translate("mainWindow", "地址"))
        self.CheckBox_Num.setText(_translate("mainWindow", "数字"))
        self.Label_Account.setText(_translate("mainWindow", "账号"))
        self.CheckBox_Char.setText(_translate("mainWindow", "字母"))
        self.CheckBox_Other.setText(_translate("mainWindow", "字符"))
        self.Label_PW.setText(_translate("mainWindow", "密码"))
        self.PushButton_Random_New.setText(_translate("mainWindow", "随机密码"))
        self.Label_PW_2.setText(_translate("mainWindow", "备注"))
        self.PushButton_Save_New.setText(_translate("mainWindow", "存储"))
        self.GroupBox_New_2.setTitle(_translate("mainWindow", "查询"))
        self.Label_Addr_2.setText(_translate("mainWindow", "地址"))
        self.Label_Account_2.setText(_translate("mainWindow", "账号"))
        self.PushButton_Save_New_2.setText(_translate("mainWindow", "查询"))
        self.Label_Account_3.setText(_translate("mainWindow", "结果"))
