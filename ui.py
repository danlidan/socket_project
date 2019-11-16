# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(793, 620)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit_chat = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_chat.setGeometry(QtCore.QRect(10, 60, 571, 361))
        self.textEdit_chat.setObjectName("textEdit_chat")
        self.textEdit_input = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_input.setGeometry(QtCore.QRect(10, 430, 571, 161))
        self.textEdit_input.setObjectName("textEdit_input")
        self.label_curchat = QtWidgets.QLabel(self.centralwidget)
        self.label_curchat.setGeometry(QtCore.QRect(10, 40, 471, 16))
        self.label_curchat.setObjectName("label_curchat")
        self.pushButton_send = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_send.setGeometry(QtCore.QRect(660, 490, 121, 28))
        self.pushButton_send.setObjectName("pushButton_send")
        self.pushButton_record = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_record.setGeometry(QtCore.QRect(660, 530, 121, 28))
        self.pushButton_record.setObjectName("pushButton_record")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(600, 10, 121, 16))
        self.label.setObjectName("label")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(600, 30, 181, 441))
        self.listWidget.setObjectName("listWidget")
        self.label_welcome = QtWidgets.QLabel(self.centralwidget)
        self.label_welcome.setGeometry(QtCore.QRect(10, 10, 371, 16))
        self.label_welcome.setObjectName("label_welcome")
        self.pushButton_nick = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_nick.setGeometry(QtCore.QRect(400, 10, 71, 31))
        self.pushButton_nick.setObjectName("pushButton_nick")
        self.lineEdit_nick = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_nick.setGeometry(QtCore.QRect(490, 10, 91, 21))
        self.lineEdit_nick.setObjectName("lineEdit_nick")
        self.label_change = QtWidgets.QLabel(self.centralwidget)
        self.label_change.setGeometry(QtCore.QRect(490, 40, 101, 16))
        self.label_change.setObjectName("label_change")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 793, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_curchat.setText(_translate("MainWindow", "当前聊天："))
        self.pushButton_send.setText(_translate("MainWindow", "发送"))
        self.pushButton_record.setText(_translate("MainWindow", "显示更多记录"))
        self.label.setText(_translate("MainWindow", "选择聊天"))
        self.label_welcome.setText(_translate("MainWindow", "欢迎！"))
        self.pushButton_nick.setText(_translate("MainWindow", "修改昵称"))
        self.label_change.setText(_translate("MainWindow", "17307130009"))
