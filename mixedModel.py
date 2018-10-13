'''
Created on 18/09/2017

#Modulo MixedModel
Este e um modulo que ira axiliar no uso de MVC (Model view controller)
No modulo iremos encontrar metodos reusaveis de diferentes MV (model/Viewer).

@author: chernomirdinmacuvele
'''
from PyQt5.Qt import Qt, QSqlRelationalTableModel, QSqlQueryModel, QSqlTableModel, QDataWidgetMapper
from PyQt5 import QtSql
import QT_msg as msg
import FuncMakeScript


def setViewModel(tblName=None, filtro=None, lstVal2Rel=None, lstRelTblName=None,lstNewNames=None, sort=0):
    '''
    Funcao para configurar o modelos[model] Relacionais.
    Tem como objectivo facilitar visualizacao de dados.
    Este Modelo aconcelho a usar para #dict Style 
    
    Args:
        tblName = Nome da tabela aqual queremos ligar na base de dados,  (Obrigatorio)
        filtro = filtro ou where e como desejamaos filtrar, (opicional)
        lstVal2Rel = os valores que desejamos fazer a relacao, (opicional)
        lstRelTblName = a tabela aqual desejamaos nos relacionar (obrigatorio se o campo anterior foi passado)
        lstNewNames =  os novos nomes que irao aparecer no header  (opicional)
        sort = como desejamos organizar a tabela por padrao e sempre o primeiro elemento e pode ser mudado (opicional)
    
    dictModel['val2Rel'] = lstVal2Rel
    dictModel['relTblName'] = lstRelTblName
    dictModel['newNames'] = lstNewNames
    '''
    bOK = False
    try:
        Model = QSqlRelationalTableModel()#Cria o object QSqlRelationalTableModel
        Model.setTable(tblName) #Atribuimos uma tabela ao objecto criado
        if filtro is not None: #Verifica se Lhe foi atribuido um Filtro
            Model.setFilter(filtro) #Caso tenha sido atribuido Colocamos o filtro
        if lstVal2Rel is not None and lstRelTblName is not None: #Vericamos se as listas de valores e tabelas relacionais estao vazias
            for idx, val in enumerate (lstVal2Rel):#Caso nao estejam vazias 
                if val is not None:
                    Model.setRelation(idx, QtSql.QSqlRelation(lstRelTblName[idx], val[0], val[1]))  #atribuimos uma relacao a cada valor com a devida Tabela a que pertence
                    Model.setJoinMode(QSqlRelationalTableModel.LeftJoin)#Identificamos o tipo de relacao 
        if lstNewNames is not None:#Verificamos se lhe foi atribuida uma lista de novos nome[headers]
            for idx, val in enumerate (lstNewNames): #Levamos para cada nome 
                Model.setHeaderData(idx, Qt.Horizontal, val)#Atribuimos a cada valos no nosso objecto
        Model.setSort(sort, Qt.AscendingOrder) #Organizado em ordem crescente
        bOK = Model.select() #Metodo para executar todas mudancas (select), que se todos os campos acima foram correctamentes prenchenchos retoma Verdade caso contrario Falso
        
        if not bOK: #Se a Excucao foi Falsa entao mostramos a menssagem de error.
            msg.error(txt="Erro na configuracao do Modelo", verbTxt=str(Model.lastError().text()))
            return (bOK, Model)
        else:
            return (bOK, Model)#Se correr tudo bem Retorna Verdade e o Modelo Criaado
        
    except TypeError as TE:#Se a Excucao foi Falsa entao mostramos a menssagem de error, isto e nos casos mais extremos.
        msg.error(txt="Erro na configuracao do Modelo", verbTxt=str(TE))
        return (bOK, None)


def setQueryModel(query=None, filtro=None, lstNewNames=None):
        """Funcao para configurar o model usando script, este modelo
        e usado para tabelas que muitas das vezes contem relacoes dentro de relacoes,
        nao a conselho a usar com mapper pois havera problemas de sicronizacao de elementos.
        Args:
            - query = a query que vamos querer executar (obrigatoria)
            - filtro = caso a query precise de lementos adicionas para ser excutada (depende)
            - lstNewNames =  os novos nomes que irao aparecer no header  (opicional)
            - sort = como desejamos organizar a tabela por padrao e sempre o primeiro elemento e pode ser mudado (opicional)
        """
        model = QSqlQueryModel() #Cria o Objecto QSqlQueryModel
        if filtro is None:  #Verifica se Lhe foi atribuido um Filtro
            model.setQuery(query) #Definimosa query ao modelo
        else:
            model.setQuery(query.format(filtro)) #Caso tenha sido atribuido Colocamos o filtro na query
        if lstNewNames is not None:#Verificamos se lhe foi atribuida uma lista de novos nome[headers]
            for idx, val in enumerate (lstNewNames): #Levamos para cada nome 
                model.setHeaderData(idx, Qt.Horizontal, val)#Atribuimos a cada valos no nosso objecto
        model.lastError().isValid()#Verificamos se a query atrbuida e valida ou nao 
        if model.lastError().text() != ' ': #Caso exista algum error Mostra o erro
            verbTxt = model.lastError().text() 
            msg.error(txt="Erro na configuracao do Modelo", verbTxt=str(verbTxt))
            model = None
            return model # Retorna um modelo vazio
        else:
            return model


def setModel4CombBox(tblName= None, lstNames= None ,widg= None, namePos = 1, condName=None, condVal=None, condQuot=None):
    """
    Esta e a Funcao para configuracao de um model para combox onde o model podera ser script ou nao script.
    Pode ser usada para configurar multiplos modelos em multiplos combox.
    
    Args:
        tblName: Nome da tabela
        lstNames: Lista dos Nomes dos campos da tabela que queremos usar(obrigatorio)
        widg: o combox que iremos usar (obrigatorio)
        namePos: position of the name we want to show in the combox normaly 1 because the name is always in position 1 (opcional)
        condName: Lista dos nomes dos campos que vao pertencer a condicao (opcional)
        condVal: Lista de Valores do campos que vamos usar (Obrigatorio se o condName foi atribuido)
        condQuot: Se queremos ou nao colocar dentro de aspas (Obrigatorio se o condName foi atribuido)
        
     e depois cria uma scritp para fazer-se o modelo do combox.   
    """
    bOK=False
    if tblName is not None and lstNames is not None:#Verificacao 
        CbModel = QSqlQueryModel() #Criar o objecto QSqlQueryModel
        if condName is not None and condVal is not None and  condQuot is not None:#Verificacao
            bOK, strSelect = FuncMakeScript.readScp(tblName, lstNames, condName, condVal, condQuot)#Cria o script de select
        else:
            bOK, strSelect = FuncMakeScript.readScp(tblName, lstNames)#Cria o script de select
        CbModel.setQuery(strSelect)#Atribuindo o script ao query object
    else:
        CbModel = QSqlTableModel() #Caso seja SQL Table Model
        bOK = True
    if bOK:#Verificacao
        widg.setModel(CbModel)#Configura o modelo ao widget
        widg.setModelColumn(namePos)#Configura a coluna ser usada pelo model
        return bOK
    else:
        msg.error(txt= "Error a Criar o Modelo para o Combbox", verbTxt=CbModel.lastError().text())
        return bOK
        
        
def getDataCombox(widg=None):
    """
    Func to Get the Combox current value, id
    Procura o index corrente depois, compara no modelo 
    e depois ele traz o id que estara na possicao 0
    
    Args:
        widg: o widget do combox
    """
    if widg is not None:
        row = widg.currentIndex()#Current index is the same as row in the table
        idx = widg.model().index(row, 0)#idx = row and column  
        data = widg.model().data(idx)#get the data in that position
        if widg.model().data(idx) is '' or widg.model().data(idx) == 0:#verficacao
            data = 'NULL' #se nao for encontrado da Retorna NULL
        return data
    if widg is None:
        return None


def reverseGetDataCombox(relText=None,widg=None):
    widg.model()


class withWidgets():
    '''
    Todos Metodos aqui sao para o auxilio caso queria trabalhar com model com Mappers
    '''
          
    def setMapper(self, model=None, fldToMap=None):
            """
            Metodo para configurar o mapper ao modelo
            
            modelo = Modelo
            fldToMap = Campos para mappear
            """
            self.mapper = QDataWidgetMapper()# cria objecto Mapper
            self.mapper.setModel(model) #Define modelo ao mapper
            for cidx, field in enumerate(fldToMap):#Para cada campo
                if field is not None: #Verdicacao
                    self.mapper.addMapping(field, cidx)#Atribuimos ao mapping
            self.mapper.toFirst()#e movemos para o primeiro(obrigatorio)
           
    def mapperToNext(self):
        self.mapper.toNext()#Proxima linha 
    
    
    def mapperToPerv(self):
        self.mapper.toPrevious()#Linha previa
    
    
    def getCurrentIndex(self):
        cIdx = self.mapper.currentIndex()#Get Current Index
        return cIdx
    
    
    def getValueFromMapper(self, pos=0):
        try:
            val = self.mapper.model().record(self.mapper.currentIndex()).value(0) #Get the value from the mapper
            row = self.mapper.currentIndex() #Get the current row or index
        except Exception:
            row = None
            val = None 
        return val, row
    
    
    def sychClickWithMap(self,indexModel=None):
            self.mapper.setCurrentModelIndex(indexModel) #Scncy clicked object with mapper
    
    
    def setMapperToIdx(self, idx):      
        self.mapper.setCurrentIndex(idx)#Set Current index to row or index
               

