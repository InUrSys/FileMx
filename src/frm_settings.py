from PyQt5.QtGui import QIcon, QPixmap

from ui_settings_categoria import Ui_Form
from extra_extra import Generic_extra
import sqlMagic
import mixedModel
import QT_msg
import os
from datetime import datetime
import platform
import FuncSQL
from PyQt5.Qt import QLineEdit, QComboBox, QPlainTextEdit, QListWidget, QDate
from builtins import str

class frm_setting_categoria(Ui_Form, Generic_extra):
    def __init__(self,dbcon = None):
        super().__init__()
        self.setupUi(self)

        self.setUpIcons()
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
            #Todas as categorias devem ser inseridas em um padrao [capitalizados]
            new_category= self.capCategory(new_category)
            #Deve-se verificar se essa categoria existe na base de dados
            isIn = self.checkIfExits(new_category)
            if isIn:
                QT_msg.aviso("Categoria <b> "+ new_category +"</b> ja existente na base de dados.")
            else:
                self.insertCategory(new_category)
        else:
            QT_msg.aviso("Insira nova categoria antes de Guardar")
    
    
    def capCategory(self, new_category):
        lst = new_category.split(sep=' ')
        new_lst = []
        if len(lst) > 1:
            for idx, txt in enumerate(lst):
                if txt != '' and txt != ' ':
                    txt = txt.capitalize()
                    space = ' '
                    new_lst.append(txt)
                    if idx < (len(lst) - 1) and lst[idx+1]!= '' and lst[idx+1] != ' ':
                        new_lst.append(space)
            new_category = ''.join(new_lst)
        else:
            new_category = new_category.capitalize()
        return new_category
            
        
    def checkIfExits(self, new_category):
        script = "select * from doctype where nome='" + new_category + "'"
        _, isIn = FuncSQL.anySelectScript(scpt=script)
        if len(isIn) > 0:
            return True
        else:
            return False 
        
    
    def insertCategory(self, new_category):
        table_name = "doctype"
        lstNames = ["cod", "nome"]
        category_code = self.generateCode(new_category)
        lstVal = [category_code, new_category]
        lstQuote = [True, True]
        bOK, msg = FuncSQL.insertVal(tblName=table_name, lstNames=lstNames, lstVal=lstVal,lstQuot=lstQuote);
        if bOK:
            QT_msg.Sucessos(msg)
            self.setCombox()
        else:
            QT_msg.aviso(txt=msg)
        
        
        

    """"::> This one generates a new code to the new added category. It ensures no repetition in database """
    def generateCode(self, category_name=None):
        def generator(category_name):
            if len(category_name) < 3:
                QT_msg.aviso("A nova categoria deve conter pelomenos 3 caracteres")
                return False
            hasWhiteSpace = self.checkWhiteSpace(category_name)
            new_code = ""
            if hasWhiteSpace:
                used_words = category_name.split(" ");
                if len(used_words) > 2:
                    for i in range(3):
                        letter_sample = used_words[i][0].upper()
                        new_code += letter_sample
                else:
                    new_code += used_words[0][0].upper()
                    new_code += used_words[1][0].upper()
            else:
                new_code = category_name[0].upper() + category_name[1].upper() + category_name[2].upper()
            return new_code

        """
        ::>> Dude, chill, this works in case there are categories with the same code, so in order to 
            avoid a lot of messages to the user about the Database Structure (UNIQUE constraint mainly) i 
            decided to whenever there's a new category, it add the same code to the previous one with an underscore
            Ex: FEA_FEA
        """
        new_code = generator(category_name)
        script = "select * from doctype where cod='" + new_code + "'"
        isIn = FuncSQL.verifyInDatabase(scpt=script)
        while isIn:
            new_code += "_" + generator(category_name)
            script = "select * from doctype where cod='" + new_code + "'"
            isIn = FuncSQL.verifyInDatabase(scpt=script)
        return new_code


    def setCombox(self):
        #Fill the combox (--tipo de documento--)
        quer = sqlMagic.table_query_scrpts['DocTypes']
        model = mixedModel.setQueryModel(query=quer)
        self.CBRemove.setModel(model)
        self.CBRemove.setModelColumn(1)

    
    def removeItem(self):
        if self.CBRemove.currentIndex() != 0:
            table_name = "doctype"
            cond = "nome"
            cond_val = self.CBRemove.currentText()
            cond_quote = True
            done = FuncSQL.deleteVal(tblName=table_name, cond=cond, conVal= cond_val, condQuot=cond_quote)
            if done:
                self.setCombox()
    
            
            

