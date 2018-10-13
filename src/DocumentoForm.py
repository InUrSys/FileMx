'''
Created on 25/04/2018

@author: chernomirdinmacuvele
'''

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
from PyQt5.Qt import QDateEdit

class frm_Documento(Ui_Form, Generic_extra):
    def __init__(self, dbcon=None):

        super().__init__()
        self.setupUi(self)
        
        self.dbcon=dbcon

        self.extra = Generic_extra()
        
        self.lstImg = []
        self.lstPdf = []
        
        self.dictMetaData={}
        self.clkFilePath=None
        self.configCbModel()
        self.configLwClickes()
        self.setUpIcons()
        self.PBAdd.clicked.connect(self.addFilesToLst)
        self.PBRemove.clicked.connect(self.removeFileFromLst)
        self.PBSave.clicked.connect(self.start_Save)
        self.settingsButton.clicked.connect(self.goToSettings)
        self.getLast()
        self.isClosed=True
        self.PBClose.clicked.connect(self.ToClosed)
        self.setUpEffects()


    def ToClosed(self):
        self.isClosed = True
        self.close()


    def setUpIcons(self):
        self.settingsButton.setIcon(QIcon(QPixmap(os.path.join("res","settings.png"))))
        # lst_wd = QListWidgetItem()
        # lst_wd.setText("File_Mx_1");
        # lst_wd.setIcon(QIcon(QPixmap(os.path.join("res", "Layer 1.png"))));
        # self.LWPathsPdf.addItem(lst_wd)


    def goToSettings(self):
        self.settings_window = settings(self.dbcon);
        self.settings_window.exec()
        if self.settings_window.close():
            self.updateCbModel()


    def getLast(self):
        bOK, value = FuncSQL.getLast(tblName='docfile', val='cod', ordBy='cod')
        if bOK:
            self.SBCod.setValue(value+1)
        else:
            self.SBCod.setValue(0)
        self.DEData.setDate(datetime.today())
        
    
    def start_Save(self):
        #Get the info from the widget
        pathToDir = self.getDirMx()
        if pathToDir == None:
            form = setting_Path()
            form.exec_() 
        
        #The saving PRocess
        if self.CBType.currentIndex() == 0:
            QT_msg.aviso(txt='Não e possivel salver um Dado sem a sua <b>Categoria</b>.')
        else:
            self.saving_part2()
        
    
    def saving_part2(self):
        bOK=None
        category = self.CBType.currentText()

        pdfObj = self.FusionImg(lstImgFile=self.lstImg)
        if pdfObj is not None:
            for pdf_obj in pdfObj:
                self.lstPdf.append(pdf_obj)

        bOK, lstObjOut = self.AddMetadata(lstPdfIn=self.lstPdf, cat=category)
        if bOK==True:
            self.saveToDatabase(lstObjOut=lstObjOut)
            QT_msg.Sucessos(txt='Ficheiro <b>MX</b> Criado com Sucesso')
            self.clearWdg()
        elif bOK==False:
            QT_msg.aviso(txt='Erro ao Criar Ficheiro <b>MX</b>!<p> Por favor tente novamente.')
        
    
    
    def saveToDatabase(self, lstObjOut):
        strLst='lista: '
        for idx, obj in enumerate(lstObjOut):
            if idx+1 == len(lstObjOut):
                strLst+=obj
            else:
                strLst+=obj+','
        if self.PTEInfo.toPlainText() == '':
            info = 'N/A'
        else:
            info = self.PTEInfo.toPlainText()
        bOK, msg = FuncSQL.insertVal(tblName='docfile', 
                          lstNames=['cod', 'cod_type',
                                    'path_file', 'data_file', 
                                    'info_file'], 
                          lstVal=[self.SBCod.text(), mixedModel.getDataCombox(widg=self.CBType),
                                  strLst, self.DEData.date().toPyDate().isoformat(),
                                  info], 
                          lstQuot=[False, True,
                                   True, True,
                                   True])     
        if bOK != True:
            QT_msg.aviso(txt=msg)   
            
        
    def clearWdg(self):
        self.getLast()
        self.PTEInfo.clear()
        self.CBType.setCurrentIndex(0)
        self.lstImg.clear()
        self.lstPdf.clear()
        self.LWPathsImg.clear()
        self.LWPathsPdf.clear()
        

    """
    ::>> BakcSlahs : modified : 04_07_2018
    def setFileName(self):
        #Clear name form LEdit
        if self.CBType.currentIndex() == 0:
            self.LEName.clear()
        else:
            #get name from generator
            name = self.name_Generator()
            self.LEName.setText(str(name))
    """

        
    def configLwClickes(self):
        lstLW = [self.LWPathsImg, self.LWPathsPdf]
        for Lw in lstLW:
            Lw.clicked.connect(self.clickedItem)
            Lw.doubleClicked.connect(self.DoubleclickedItem)
        
        
    def configCbModel(self):
        #Fill the combox (--tipo de documento--)
        quer = sqlMagic.table_query_scrpts['DocTypes']
        model = mixedModel.setQueryModel(query=quer)
        self.CBType.setModel(model)
        self.CBType.setModelColumn(1)


    def addFilesToLst(self):
        isImg, fileOut = self.getFile()
        self.clkFilePath=None

        fileName = os.path.basename(fileOut)
        fileName = self.extra.extract_file_name(filename=fileName)

        if isImg == True:
            bOK = self.checkIfEqual(valIn=fileOut, OgLst=self.lstImg)
            if not bOK:
                self.lstImg.append(fileOut)
                self.addLstFileToView()
                #self.LEName.setText(fileName)

            else:
                QT_msg.aviso(txt='Estes Dados ja existem na lista de Imagens')
                #messagem informando que os dados ja existem
        elif isImg == False:
            bOK = self.checkIfEqual(valIn=fileOut, OgLst=self.lstPdf)
            if  not bOK:
                self.lstPdf.append(fileOut)
                self.addLstFileToView()
                #self.LEName.setText(fileName)
            else:
                QT_msg.aviso(txt="Estes Dados ja existem na lista de PDF")
                #messagem informando que os dados ja existem


    def addLstFileToView(self):
        self.clkFilePath=None
        self.LWPathsImg.clear()
        self.LWPathsPdf.clear()


        for file_path in self.lstImg:
            res = ''
            file_name_list = os.path.basename(file_path).split(".")

            if file_name_list[1] == "jpg":
                res = "jpg.png"
            elif file_name_list[1] == "png":
                res = "png.png"
            self.LWPathsImg.addItem(QListWidgetItem(QIcon(os.path.join("res", res)), file_name_list[0]))

        for file_path in self.lstPdf:
            file_name_list = os.path.basename(file_path).split(".")
            self.LWPathsPdf.addItem(QListWidgetItem(QIcon(os.path.join("res", "pdf.png")), file_name_list[0]))
    
    
    def removeFileFromLst(self):
        if self.clkFilePath is not None:
            Lwidget, mdixToFile = self.clkFilePath
            item = mdixToFile.data()
            itemRow = mdixToFile.row()
            Lwidget.takeItem(itemRow)
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

            