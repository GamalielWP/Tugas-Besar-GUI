# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_loginForm(object):
    def setupUi(self, loginForm):
        loginForm.setObjectName("loginForm")
        loginForm.resize(322, 490)
        self.labelLogo = QtWidgets.QLabel(loginForm)
        self.labelLogo.setGeometry(QtCore.QRect(40, 40, 241, 201))
        self.labelLogo.setText("")
        self.labelLogo.setPixmap(QtGui.QPixmap("resource/telmed.png"))
        self.labelLogo.setScaledContents(True)
        self.labelLogo.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLogo.setObjectName("labelLogo")
        self.layoutWidget = QtWidgets.QWidget(loginForm)
        self.layoutWidget.setGeometry(QtCore.QRect(70, 320, 181, 79))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineNIK = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineNIK.setToolTip("")
        self.lineNIK.setAlignment(QtCore.Qt.AlignCenter)
        self.lineNIK.setObjectName("lineNIK")
        self.verticalLayout.addWidget(self.lineNIK)
        self.linePassword = QtWidgets.QLineEdit(self.layoutWidget)
        self.linePassword.setAlignment(QtCore.Qt.AlignCenter)
        self.linePassword.setObjectName("linePassword")
        self.verticalLayout.addWidget(self.linePassword)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.loginButton = QtWidgets.QPushButton(self.layoutWidget)
        self.loginButton.setObjectName("loginButton")
        self.horizontalLayout.addWidget(self.loginButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(loginForm)
        QtCore.QMetaObject.connectSlotsByName(loginForm)

    def retranslateUi(self, loginForm):
        _translate = QtCore.QCoreApplication.translate
        loginForm.setWindowTitle(_translate("loginForm", "Telkom Medika"))
        self.lineNIK.setPlaceholderText(_translate("loginForm", "NIK"))
        self.linePassword.setPlaceholderText(_translate("loginForm", "Password"))
        self.loginButton.setText(_translate("loginForm", "Login"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loginForm = QtWidgets.QWidget()
    ui = Ui_loginForm()
    ui.setupUi(loginForm)
    loginForm.show()
    sys.exit(app.exec_())

