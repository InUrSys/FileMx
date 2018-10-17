'''
Created on 25/04/2018

@author: chernomirdinmacuvele
@colaborator: felicianoMazoio
'''
import shelve

import QT_msg as msg
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QListWidgetItem
from frm_settings import frm_setting_categoria as settings
import sqlMagic
import mixedModel
import QT_msg
from ExtraExtra import Generic_extra
from ui_Documento import Ui_Form
import os
import FuncSQL
from datetime import datetime
from PyQt5.Qt import QDateEdit, QComboBox
import MainForm
import CloudStorage
import shutil
from Services import Thread_Google_Uploader
import send2trash

class frm_Documento(Ui_Form, Generic_extra):
    def __init__(self, jsonFile=None, bucketName=None):

        super().__init__()
        self.setupUi(self)
        
        self.jsonFile = jsonFile
        self.bucketName = bucketName
        self.extra = Generic_extra()

        self.shelvePath = None
        self.lstImg = []
        self.lstPdf = []
        self.lstDocTypes = []
        self.dictMetaData={}
        self.clkFilePath=None
        
        #self.configCbModel()
        self.setLstDocType()
        self.setUpIcons()
        
        self.PBAdd.clicked.connect(self.addFilesToLst) #working 100%
        self.PBRemove.clicked.connect(self.removeFileFromLst) #working 100%
        self.LWPaths.clicked.connect(self.clickedItem) #working 100%
        self.LWPaths.doubleClicked.connect(self.DoubleclickedItem) #working 100%
        self.PBSave.clicked.connect(self.start_Save)
        self.PBClose.clicked.connect(self.ToClosed) #working 100%
 
 
    def setLstDocType(self):
        shelvePath = "mainConfig"
        shelvFile = shelve.open(shelvePath);
        try:
            shelvFile['mainDict']
            try:
                self.lstDocTypes = shelvFile['docTypes']
            except KeyError:
                self.lstDocTypes = ['Factura', 'Recibo', 'Curriculum Vitae', 'Certificado']
            shelvFile.close()
        except KeyError:
            print("Porfavor carregue ou crie um ficheiro de configuracao")
         
    def 
 
    def extractToWrite(self, folder = None):
        #Gets all the writable folders
        folders_to_write = []
        values = list(folder.values())#Extracts all the values inside the mainDict in the shelveFile and gets Tupls (path, boolean)
        for val in values:
            if val[1]: #Checks the boolean to see if it is writable
                folders_to_write.append(val[0])
 
        folders_to_write = self.filterPahts(folders_to_write) #Filters the folder path to get only its name.
        self.CBToStore.addItems(folders_to_write)
 
    def filterPahts(self, collection = None):
        filtered = []
        for val in collection:
            filtered.append(os.path.basename(val))
 
        return filtered


    def ToClosed(self):
        self.isClosed = True
        self.close()


    def setUpIcons(self):
        self.settingsButton.setIcon(QIcon(QPixmap(os.path.join(os.getcwd(),"res","settings.png"))))
        

    def goToSettings(self):
        self.settings_window = settings(self.dbcon);
        self.settings_window.exec()
        if self.settings_window.close():
            self.updateCbModel()


    def start_Save(self):
        self.CBType.addItems(["Factura"])
        self.CBToStore.addItems(["/Users/chernomirdinmacuvele/File Mx/BIM/RH/Steban"])

        pdfObj = self.FusionImg(lstImgFile=self.lstImg) #working 100$
        if pdfObj is not None:
            for pdf_obj in pdfObj:
                self.lstPdf.append(pdf_obj)
        
        bOK, lstObjOut = self.AddMetadata(lstPdfIn=self.lstPdf)
        if bOK==True:
            QT_msg.Sucessos(txt='Ficheiro <b>MX</b> Criado com Sucesso')
            self.saving_part2(lstObjOut)
            self.clearWdg()
        elif bOK==False:
            QT_msg.aviso(txt='Erro ao Criar Ficheiro <b>MX</b>!<p> Por favor tente novamente.')
        return bOK
        
    
    def saving_part2(self,lstObjOut):
        bucket = CloudStorage.setConnectionToCloud(self.jsonFile, self.bucketName)
        for mxFile in lstObjOut:
            curDir = os.getcwd() 
            newFile = shutil.copy(mxFile, curDir)
            _, fileToUpload = os.path.split(newFile)
            blob = CloudStorage.setBlobToUpload(fileToUpload, bucket)
            if blob != None:
                self.uploading = Thread_Google_Uploader(blob, fileToUpload)
                self.uploading.done.connect(self.clean)
                self.uploading.start()
                #CloudStorage.upload(blob, fileToUpload)
        
    def clean(self, bOK, fileToClean):
        if bOK:
            send2trash.send2trash(fileToClean)
            msg.Sucessos("Cleanned")
            
        
    def clearWdg(self):
        #self.getLast()
        self.PTEInfo.clear()
        self.CBType.setCurrentIndex(0)
        self.CBToStore.setCurrentIndex(0)
        self.lstImg.clear()
        self.lstPdf.clear()
        self.LWPaths.clear()
        
        
    def configCbModel(self):
        #Fill the combox (--tipo de documento--)
        quer = sqlMagic.table_query_scrpts['DocTypes']
        model = mixedModel.setQueryModel(query=quer)
        self.CBType.setModel(model)
        self.CBType.setModelColumn(1)


    def addFilesToLst(self):
        txtErrorSame = 'Este ficheiro ja existe na lista'
        isImg, fileOut = self.getFile()
        self.clkFilePath=None

        if isImg == True:
            bOK = self.checkIfEqual(valIn=fileOut, OgLst=self.lstImg)
            if not bOK:
                self.lstImg.append(fileOut)
                self.addLstFileToView()
                #self.LEName.setText(fileName)
            else:
                QT_msg.aviso(txt=txtErrorSame)
        elif isImg == False:
            bOK = self.checkIfEqual(valIn=fileOut, OgLst=self.lstPdf)
            if  not bOK:
                self.lstPdf.append(fileOut)
                self.addLstFileToView()
            else:
                QT_msg.aviso(txt=txtErrorSame)


    def addLstFileToView(self):
        self.clkFilePath=None
        self.LWPaths.clear()

        for file_path in self.lstImg:
            res = ''
            file_name_list = os.path.basename(file_path).split(".")
            if file_name_list[1].lower() == "jpg":
                res = "jpg.png"
            elif file_name_list[1].lower() == "png":
                res = "png.png"
            self.LWPaths.addItem(QListWidgetItem(QIcon(os.path.join(os.getcwd(),"res", res)), file_path))
            
        for file_path in self.lstPdf:
            self.LWPaths.addItem(QListWidgetItem(QIcon(os.path.join(os.getcwd(),"res", "pdf.png")), file_path))
    
    
    def removeFileFromLst(self):
        if self.clkFilePath is not None:
            mdixToFile = self.clkFilePath
            item = mdixToFile.data()
            itemRow = mdixToFile.row()
            self.LWPaths.takeItem(itemRow)
            try:
                if item in self.lstImg:
                    self.lstImg.remove(item)
                else:
                    self.lstPdf.remove(item)
            except ValueError:
                pass
            self.clkFilePath= None
            self.addLstFileToView()
            
    def updateCbModel(self):
        self.configCbModel()

            