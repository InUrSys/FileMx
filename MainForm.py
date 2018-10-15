'''
Created on Oct 15, 2018

@author: chernomirdinmacuvele
'''
from ui_Main import Ui_MainWindow
from PyQt5.Qt import QMainWindow


class frm_Main(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        