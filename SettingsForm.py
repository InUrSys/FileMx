'''
Created on Oct 16, 2018

@author: chernomirdinmacuvele
@colaborator: felicianoMazoio
'''
import shelve

import BuildTreeForm
import QT_msg as msg
from ui_settings import Ui_Form
from PyQt5.Qt import QDialog, QFileDialog, QLineEdit
import os
import shutil
import CloudStorage
from shutil import SameFileError
from ExtraExtra import Generic_extra
class Settings_Frm(QDialog, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.shelvpaht = None;
        self.populateAreas()
        self.TBPathJson.clicked.connect(self.selectJsonFile)
        self.TBPath.clicked.connect(self.openTreeModel)
        self.PBGuardar.clicked.connect(self.save)
        self.PBFechar.clicked.connect(self.close)

    def populateAreas(self):

        shelveFile = shelve.open("mainConfig")
        jsonPath = shelveFile['jsonPath']
        bucketName = shelveFile['companyName']
        mainConfigPath = os.path.abspath('mainConfig')


        #Variaveis que vao controlar a exitencia do path de cada ficherio
        """
            Why you ask
            Imaginemos que (devemos pensar em todos os casos) o File Mx nao baixe os ficheiros da cloud mas no directorio do File_Mx EE exista um ficheiro .dat (nao .dir, .ba,, .db)
            Tenho de verificar se pelomenos um destes ficheiros existem para colocar  LineEdit do path, dai que temos de verifica-los percorrendo a lista das extensoes ate ao ultimo 
            elemento e se nem o ultimo elemento existe, significa que nao temos nenhum ficheiro mainConfig
        """
        ext = ['.dir', '.bak', '.db', '.dat']
        exists = True
        size = 0

        for extension in ext:
            full_path = mainConfigPath + extension
            #Se pelomenos um existir, ele sai do loop
            if not os.path.exists(full_path):
                size += 1
            else:
                break

            if size == len(ext):
                exists = False


        if not exists:
            msg.error("Ficheiro de configuracoes nao existente!")
        else:
            self.LEPath.setText(mainConfigPath)

        self.LECompany.setText(bucketName)
        self.LEPathJson.setText(jsonPath)

        shelveFile.close()
        print("working")


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
            try:
                newPath = shutil.copy(jsonFile, curDir)
            except SameFileError:
                _, file = os.path.split(jsonFile)
                newPath = os.path.join(curDir,file)
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
            shelveFiel = shelve.open("mainConfig")
            shelveFiel['jsonPath'] = jsonFile
            shelveFiel['companyName'] = empresa
            shelveFiel.close()
            generic_extra = Generic_extra()
            generic_extra.uploadMainConfig(jsonFile=jsonFile, bucketName=empresa)
            msg.Sucessos("Configuracoes guardadas!")
        else:
            #ficherio nao valido nao salvar e mostrar msg de erro
            msg.error("<b>Ficheiro Invalido</b>.<p>Ficheiro nao valido para salvar. Acrescente o nome da empresa</p>")
            #nao fechar

    #save in a shelvewhere the app resides