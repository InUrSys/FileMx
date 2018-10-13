# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/chernomirdinmacuvele/Documents/workspace/File_MX_EE/UI/ui_TreeForm.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(648, 460)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.twTreeObj = QtWidgets.QTreeView(Dialog)
        self.twTreeObj.setObjectName("twTreeObj")
        self.gridLayout.addWidget(self.twTreeObj, 1, 0, 3, 1)
        self.pbMake = QtWidgets.QPushButton(Dialog)
        self.pbMake.setObjectName("pbMake")
        self.gridLayout.addWidget(self.pbMake, 4, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(76, 225, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(454, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 1)
        self.pbRemove = QtWidgets.QPushButton(Dialog)
        self.pbRemove.setEnabled(False)
        self.pbRemove.setObjectName("pbRemove")
        self.gridLayout.addWidget(self.pbRemove, 1, 1, 1, 2)
        self.pbAdd = QtWidgets.QPushButton(Dialog)
        self.pbAdd.setObjectName("pbAdd")
        self.gridLayout.addWidget(self.pbAdd, 0, 1, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        self.label_2.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lbItem = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbItem.setFont(font)
        self.lbItem.setObjectName("lbItem")
        self.horizontalLayout.addWidget(self.lbItem)
        self.tbClean = QtWidgets.QToolButton(Dialog)
        self.tbClean.setObjectName("tbClean")
        self.horizontalLayout.addWidget(self.tbClean)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Estrutura Hierárquica"))
        self.pbMake.setText(_translate("Dialog", "Criar"))
        self.pbRemove.setText(_translate("Dialog", "Remove"))
        self.pbAdd.setText(_translate("Dialog", "Add"))
        self.label_2.setText(_translate("Dialog", "Item Selecionado:"))
        self.lbItem.setText(_translate("Dialog", "Nenhum"))
        self.tbClean.setText(_translate("Dialog", "..."))

