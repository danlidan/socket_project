# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(372, 246)
        self.login_button = QtWidgets.QPushButton(Form)
        self.login_button.setGeometry(QtCore.QRect(140, 170, 93, 28))
        self.login_button.setObjectName("login_button")
        self.sign_button = QtWidgets.QPushButton(Form)
        self.sign_button.setGeometry(QtCore.QRect(140, 210, 93, 28))
        self.sign_button.setObjectName("sign_button")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(50, 20, 72, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(50, 50, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(50, 110, 111, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(140, 20, 191, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 50, 191, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(140, 110, 191, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(20, 140, 91, 21))
        self.label_4.setObjectName("label_4")
        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(140, 140, 191, 21))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_state = QtWidgets.QLabel(Form)
        self.label_state.setGeometry(QtCore.QRect(10, 80, 321, 16))
        self.label_state.setObjectName("label_state")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.login_button.setText(_translate("Form", "登录"))
        self.sign_button.setText(_translate("Form", "注册"))
        self.label.setText(_translate("Form", "账号"))
        self.label_2.setText(_translate("Form", "密码"))
        self.label_3.setText(_translate("Form", "昵称"))
        self.label_4.setText(_translate("Form", "再次输入密码"))
        self.label_state.setText(_translate("Form", "以下内容为注册必填"))
