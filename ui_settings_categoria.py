# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/chernomirdinmacuvele/Documents/workspace/File_MX_Projects/UI/ui_settings_categoria.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(287, 200)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.PBClose = QtWidgets.QPushButton(Form)
        self.PBClose.setMaximumSize(QtCore.QSize(115, 16777215))
        self.PBClose.setObjectName("PBClose")
        self.gridLayout.addWidget(self.PBClose, 3, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 2, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.removeLabel = QtWidgets.QLabel(Form)
        self.removeLabel.setObjectName("removeLabel")
        self.verticalLayout_2.addWidget(self.removeLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.CBRemove = QtWidgets.QComboBox(Form)
        self.CBRemove.setObjectName("CBRemove")
        self.horizontalLayout_2.addWidget(self.CBRemove)
        self.PBRemove = QtWidgets.QPushButton(Form)
        self.PBRemove.setMaximumSize(QtCore.QSize(30, 16777215))
        self.PBRemove.setText("")
        self.PBRemove.setObjectName("PBRemove")
        self.horizontalLayout_2.addWidget(self.PBRemove)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_2, 2, 0, 1, 3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.adicionarLabel = QtWidgets.QLabel(Form)
        self.adicionarLabel.setObjectName("adicionarLabel")
        self.verticalLayout.addWidget(self.adicionarLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LEAdd = QtWidgets.QLineEdit(Form)
        self.LEAdd.setObjectName("LEAdd")
        self.horizontalLayout.addWidget(self.LEAdd)
        self.PBAdd = QtWidgets.QPushButton(Form)
        self.PBAdd.setMaximumSize(QtCore.QSize(30, 16777215))
        self.PBAdd.setText("")
        self.PBAdd.setObjectName("PBAdd")
        self.horizontalLayout.addWidget(self.PBAdd)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 3)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "configuração da Categorias"))
        self.PBClose.setText(_translate("Form", "Close"))
        self.removeLabel.setText(_translate("Form", "Remover Categoria"))
        self.adicionarLabel.setText(_translate("Form", "Adicionar Categoria"))

