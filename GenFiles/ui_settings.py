# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/chernomirdinmacuvele/Documents/workspace/File_MX_EE/UI/ui_settings.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(453, 237)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.LEPath = QtWidgets.QLineEdit(Form)
        self.LEPath.setObjectName("LEPath")
        self.gridLayout.addWidget(self.LEPath, 1, 1, 1, 1)
        self.TBPath = QtWidgets.QToolButton(Form)
        self.TBPath.setObjectName("TBPath")
        self.gridLayout.addWidget(self.TBPath, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.LEPathJson = QtWidgets.QLineEdit(Form)
        self.LEPathJson.setObjectName("LEPathJson")
        self.gridLayout.addWidget(self.LEPathJson, 2, 1, 1, 1)
        self.TBPathJson = QtWidgets.QToolButton(Form)
        self.TBPathJson.setObjectName("TBPathJson")
        self.gridLayout.addWidget(self.TBPathJson, 2, 2, 1, 1)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 3, 0, 1, 3)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.PBGuardar = QtWidgets.QPushButton(Form)
        self.PBGuardar.setObjectName("PBGuardar")
        self.gridLayout_2.addWidget(self.PBGuardar, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.PBFechar = QtWidgets.QPushButton(Form)
        self.PBFechar.setObjectName("PBFechar")
        self.gridLayout_2.addWidget(self.PBFechar, 0, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 4, 0, 1, 3)
        self.LECompany = QtWidgets.QLineEdit(Form)
        self.LECompany.setObjectName("LECompany")
        self.gridLayout.addWidget(self.LECompany, 0, 1, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Configuracao"))
        self.label.setText(_translate("Form", "<html><head/><body><p>Nome da </p><p>Empresa</p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p>Configuraçāo</p><p>﻿Hierárquica: </p></body></html>"))
        self.TBPath.setText(_translate("Form", "..."))
        self.label_3.setText(_translate("Form", "<html><head/><body><p>Ficheiro </p><p>Chave: </p></body></html>"))
        self.TBPathJson.setText(_translate("Form", "..."))
        self.PBGuardar.setText(_translate("Form", "Guardar"))
        self.PBFechar.setText(_translate("Form", "Fechar"))

