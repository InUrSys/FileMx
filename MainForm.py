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


class frm_Main(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.setViewer()
    
    def setViewer(self):
        startTime = time.time()
        jsonFile = '/Users/chernomirdinmacuvele/Documents/workspace/File_MX_EE/File Mx EE-de38156917d4.json'
        NomeBalde = '1_empresa'
        lstOut = CloudStorage.getListItem(jsonFile, NomeBalde)
        if lstOut != None:
            Generic_extra.makeModel(Generic_extra, self.TVFiles, lstOut)
            print("--- %s seconds ---" % (time.time() - startTime))