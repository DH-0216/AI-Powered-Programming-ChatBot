from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(410, 300)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")

        self.textEdit = QtWidgets.QTextEdit(parent=Form)
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 2)
        self.textEdit.setObjectName("textEdit")

        self.lineEdit = QtWidgets.QLineEdit(parent=Form)
        self.lineEdit.setPlaceholderText("Type your message here...")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.lineEdit.setObjectName("lineEdit")

        self.pushButton = QtWidgets.QPushButton(parent=Form)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Send"))