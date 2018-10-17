'''
Created on Oct 15, 2018

@author: chernomirdinmacuvele
@colaborator: felicianoMazoio
'''
import os

from PyQt5.QtGui import QIcon, QPixmap
import QT_msg as msg

import SettingsForm
from ui_Main import Ui_MainWindow
from PyQt5.Qt import QMainWindow, QStandardItemModel, QPushButton
import CloudStorage
from PyQt5.QtWidgets import QTreeWidget, QAbstractItemView, QTableWidget, QHeaderView
import time
from ExtraExtra import Generic_extra
from CloudStorage import setConnectionToCloud
from Services import Thread_Google_Bucket
import DocumentoForm
import send2trash


class frm_Main(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.oldLst = None;
        
        self.setCon()
        self.configTable()
        self.setUpIcons()
        self.clearTempFiles()
        self.selectionBehavior()
        self.PBConfigurar.clicked.connect(self.openConfig)
        self.TVFiles.clicked.connect(self.obtainBlob)
        self.bucket = None
        self.PBAdicionar.clicked.connect(self.onAddClicked)
        self.PBRemover.clicked.connect(self.deleteFile)
        self.PBOpen.clicked.connect(self.open)
        self.blob = None
        
    def open(self):
        pass


    def configTable(self):
        self.TVFiles.horizontalHeader().setStretchLastSection(True)
        self.TVFiles.setColumnWidth(1, 90)
        self.TVFiles.horizontalHeader().setSectionResizeMode(1)
        self.TVFiles.setEditTriggers(QAbstractItemView.NoEditTriggers)



    def clearTempFiles(self):
        try:
            send2trash.send2trash('temp_files')
        except OSError:
            pass
        

    def disableButton(self):
        self.blob = None
        self.PBRemover.setEnabled(False)

    def obtainBlob(self, mdx):
        self.blob = self.lstOut[mdx.row()][0]
        self.PBRemover.setEnabled(True)

    def setUpIcons(self):
        self.PBOpen.setIcon(QIcon(QPixmap(os.path.join("res","open.png"))))
        self.PBOpen_2.setIcon(QIcon(QPixmap(os.path.join("res","download.png"))))

    def openConfig(self):
        frm = SettingsForm.Settings_Frm()
        frm.exec_()
        self.disableButton()
        
    def deleteFile(self):
        CloudStorage.delete(self.blob)
        msg.Sucessos("Item removido")

        
    def selectionBehavior(self):
        self.TVFiles.setSelectionBehavior(QAbstractItemView.SelectRows)
    
    
    def setCon(self):
        
        self.jsonFile = 'File Mx EE-de38156917d4.json'
        self.NomeBalde = '1_empresa'
        Generic_extra().getMainConfig(self.jsonFile, self.NomeBalde)
        self.setCon = Thread_Google_Bucket(self.jsonFile, self.NomeBalde)
        self.setCon.bucket.connect(self.setBucket)
        self.setCon.start()

    def checkLists(self):
        if str(self.lstOut) != str(self.oldLst):
            self.disableButton()
        self.oldLst = self.lstOut
        
    def setBucket(self, bucket):
        self.bucket = bucket
        self.lstOut = CloudStorage.getListItem(bucket=self.bucket)
        self.checkLists()
        self.setViewer()
        
    
    def setViewer(self):
        if self.lstOut != None:
            Generic_extra.makeModel(Generic_extra, self.TVFiles, self.lstOut)

    
    def onAddClicked(self):
        frmAdd = DocumentoForm.frm_Documento(self.jsonFile, self.NomeBalde)
        frmAdd.exec_()
        self.disableButton()