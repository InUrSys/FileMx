'''
Created on Oct 16, 2018

@author: chernomirdinmacuvele
'''
from ui_settings import Ui_Form
from PyQt5.Qt import QDialog, QFileDialog, QLineEdit
import os
import shutil
import CloudStorage
class Settings_Frm(QDialog, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.TBPathJson.clicked.connect(self.selectJsonFile)
        self.PBGuardar.clicked.connect()
    
    def selectJsonFile(self):
        jsonFile, _ = QFileDialog().getOpenFileName(self, "Select File", "","Json File(*.json)")
        curDir = os.getcwd()
        if jsonFile != '':
            newPath = shutil.copy(jsonFile, curDir)
            self.LEPathJson.setText(newPath)
    
    
    def save(self):
        #test if it works
        empresa = self.LECompany.text()
        jsonFile = self.LEPathJson.text()
        bucket = CloudStorage.setConnectionToCloud(jsonFile, empresa)
        if bucket != None:
            #Ficheiro valido salvar
            #fechar
            #Criar um ficherio shelve para armazenar os Dados de todos os campos
            pass
        else:
            #ficherio nao valido nao salvar e mostrar msg de erro
            #nao fechar 
            pass
    
    #save in a shelvewhere the app resides