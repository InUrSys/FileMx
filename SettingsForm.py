'''
Created on Oct 16, 2018

@author: chernomirdinmacuvele
'''
import BuildTreeForm
from ui_settings import Ui_Form
from PyQt5.Qt import QDialog, QFileDialog, QLineEdit
import os
import shutil
import CloudStorage
class Settings_Frm(QDialog, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.shelvpaht = None;
        self.TBPathJson.clicked.connect(self.selectJsonFile)
        self.TBPath.clicked.connect(self.openTreeModel)
        # self.PBGuardar.clicked.connect()


    def openTreeModel(self):
        tree = BuildTreeForm.BuildTree()
        tree.exec_()
        self.shelvpaht = BuildTreeForm.BuildTree.shelvPath;
        if self.shelvpaht is None:
            self.LEPath.setText("Nenhum ficheiro Carregado")
        else:
            self.LEPath.setText(self.shelvpaht)

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