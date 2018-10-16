'''
Created on Oct 15, 2018

@author: chernomirdinmacuvele
'''
import os

from PyQt5.QtGui import QIcon, QPixmap

import SettingsForm
from ui_Main import Ui_MainWindow
from PyQt5.Qt import QMainWindow, QStandardItemModel
import CloudStorage
from PyQt5.QtWidgets import QTreeWidget, QAbstractItemView, QTableWidget
import time
from ExtraExtra import Generic_extra
from CloudStorage import setConnectionToCloud
from Services import Thread_Google_Bucket


class frm_Main(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.setCon()
        self.setUpIcons()

        self.selectionBehavior()
        self.PBConfigurar.clicked.connect(self.openConfig)
        self.TVFiles.clicked.connect(self.obtainBlob)
        self.bucket = None
        self.blob = None

    def obtainBlob(self, mdx):
        self.blob = self.lstOut[mdx.row()][0]

    def setUpIcons(self):
        self.PBOpen.setIcon(QIcon(QPixmap(os.path.join("res","open.png"))))
        self.PBOpen_2.setIcon(QIcon(QPixmap(os.path.join("res","download.png"))))

    def openConfig(self):
        frm = SettingsForm.Settings_Frm()
        frm.exec_()

    def selectionBehavior(self):
        self.TVFiles.setSelectionBehavior(QAbstractItemView.SelectRows)
    
    def setCon(self):
        jsonFile = 'File Mx EE-de38156917d4.json'
        NomeBalde = '1_empresa'
        self.setCon = Thread_Google_Bucket(jsonFile, NomeBalde)
        self.setCon.bucket.connect(self.setBucket)
        self.setCon.start()
        
    def setBucket(self, bucket):
        self.bucket = bucket
        self.lstOut = CloudStorage.getListItem(bucket=self.bucket)
        self.setViewer()
    
    def setViewer(self):
        if self.lstOut != None:
            Generic_extra.makeModel(Generic_extra, self.TVFiles, self.lstOut)
