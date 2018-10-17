from PyQt5.QtGui import QIcon, QPixmap


from ExtraExtra import Generic_extra
from ui_SetCategorias import Ui_Form
import sqlMagic
import mixedModel
import QT_msg
import os
from datetime import datetime
import platform
import FuncSQL
from PyQt5.Qt import QLineEdit, QComboBox, QPlainTextEdit, QListWidget, QDate,\
    QDialog
import shelve

class SetCategorias_Form(QDialog, Ui_Form):
    def __init__(self, jsonFile=None, bucketName=None):
        super().__init__()
        self.setupUi(self)

        self.jsonFile = jsonFile
        self.bucketName = bucketName

        self.setUpIcons()
        self.lstDocTypes = [] 
        self.setLstDocType()
        self.setCombox()
        
        self.PBAdd.clicked.connect(self.adicionarCategoria)
        self.PBRemove.clicked.connect(self.removeItem)
        self.PBClose.clicked.connect(self.close)

    
    def setUpIcons(self):
        """::>> Just to setup some icons"""
        path_to_res = "res" #os.path.join(os.getcwd(), 'res');

        self.PBAdd.setIcon(QIcon(QPixmap(os.path.join(path_to_res,"check.png"))))
        self.PBRemove.setIcon(QIcon(QPixmap(os.path.join(path_to_res,"cross.png"))))


    
    def adicionarCategoria(self):
        """::>> Metodo responsavel por adicionar uma nova categoria"""
        new_category = self.LEAdd.text();
        if new_category != "":
            #Deve-se verificar se essa categoria existe na base de dados
            isIn = self.checkIfExits(new_category)
            if not isIn:
                QT_msg.aviso("Categoria <b> "+ new_category +"</b> ja existente na base de dados.")
            else:
                self.insertCategory(new_category)
                self.LEAdd.clear()
        else:
            QT_msg.aviso("Insira nova categoria antes de Guardar")
    
                
    def checkIfExits(self, new_category):
        if new_category not in self.lstDocTypes:
            return True
        else:
            return False 
        
    
    def insertCategory(self, new_category):
        if Generic_extra().checkMainConfig():
            shelvePath = "mainConfig"
            shelvFile = shelve.open(shelvePath);
            try:
                self.lstDocTypes.append(new_category)
                shelvFile['docTypes'] = self.lstDocTypes
            except KeyError:
                print("A janela sera fechada. Porfavor carregue ou crie um ficheiro de configuracao")
                self.close() 
            shelvFile.close()
            msg = "Nova categoria introduzido com sucessos"
            QT_msg.Sucessos(msg)
            self.setLstDocType()
            self.setCombox()
            Generic_extra().uploadMainConfig(self.jsonFile, self.bucketName)
            

    def setCombox(self):
        self.CBRemove.clear()
        self.CBRemove.addItems(self.lstDocTypes)
        
    def setLstDocType(self):
        if Generic_extra().checkMainConfig():
            shelvePath = "mainConfig"
            shelvFile = shelve.open(shelvePath);
            try:
                shelvFile['mainDict']
                try:
                    self.lstDocTypes = shelvFile['docTypes']
                    if self.lstDocTypes == []:
                        self.lstDocTypes = ['--Selecione o Tipo de Doc.--','Factura', 'Recibo', 'Curriculum Vitae', 'Certificado']
                        shelvFile['docTypes'] = self.lstDocTypes
                except KeyError:
                    self.lstDocTypes = ['--Selecione o Tipo de Doc.--','Factura', 'Recibo', 'Curriculum Vitae', 'Certificado']
                    shelvFile['docTypes'] = self.lstDocTypes
                shelvFile.close()
            except KeyError:
                print("Porfavor carregue ou crie um ficheiro de configuracao")
        else:
            print("A janela sera fechada. Porfavor carregue ou crie um ficheiro de configuracao")
            self.close()

    
    def removeItem(self):
        if self.CBRemove.currentIndex() != 0:
            table_name = "doctype"
            cond = "nome"
            cond_val = self.CBRemove.currentText()
            cond_quote = True
            done = FuncSQL.deleteVal(tblName=table_name, cond=cond, conVal= cond_val, condQuot=cond_quote)
            if done:
                self.setCombox()
                Generic_extra().uploadMainConfig(self.jsonFile, self.bucketName)
    
            
            

