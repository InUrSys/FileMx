'''
Created on Oct 15, 2018

@author: chernomirdinmacuvele
'''
from ui_Main import Ui_MainWindow
from PyQt5.Qt import QMainWindow, QStandardItemModel
import CloudStorage
from PyQt5.QtWidgets import QTreeWidget
import time
from ExtraExtra import Generic_extra
from CloudStorage import setConnectionToCloud
from Services import Thread_Google_Bucket


class frm_Main(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.setCon()
        self.bucket = None
    
    def setCon(self):
        jsonFile = '/Users/chernomirdinmacuvele/Documents/workspace/File_MX_EE/File Mx EE-de38156917d4.json'
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
            