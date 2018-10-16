'''
Created on 16/04/2018
@author: BackSlash
'''

from PyQt5.Qt import QApplication, QStyleFactory
import sys
from InternetServices import Thread_Internet_Status
import BuildTreeForm
import DocumentoForm
from MainForm import frm_Main


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    
    internetStatus = bool
    
    def InternetStatus(status):
        '''
        Set interentStatus Var global
        and adding it a state (True or False)
        '''
        global internetStatus 
        internetStatus = status
        
    
    InternetThread = Thread_Internet_Status()
    InternetThread.status.connect(InternetStatus)
    InternetThread.start()

    #form2Show = DocumentoForm.frm_Documento()
    #form2Show.exec_()
    
    mainApp = frm_Main()
    mainApp.show()
    
    try:
        app.verbose_crash = True
#TODO: Use the line below only when not debugging
        app.exec_()
    except BaseException as e1:
        sys.exit()