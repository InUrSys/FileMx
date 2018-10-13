'''
Created on 12/09/2017
Module de Funcoes sql, neste modelo se enctram algumas das funcoes 
em sql usadas para:
CREATE 
READ
UPDATE
DELETE
@author: chernomirdinmacuvele
'''
from PyQt5.Qt import QSqlQuery, QSqlError
import QT_msg as msg
import FuncMakeScript as script

def getLast(tblName=None, val="id", ordBy="id"):
        ''' Funcao para trazer o ultimo elemento ou data de uma 
        Tabela na base de dados. 
        Retorna uma tupla, com (Bool e Val)
        Args:
            tblName= Nome da tabela que vamos quere o id 
            val = o valor ou nome
            ordBy= Ordernar por ( e aconselhavel usar o mesmo que o "val")
        '''
        bOK =False
        scrpt =  "select "+val+" from "+tblName+" order by "+ordBy+" DESC LIMIT 1"
        quer = QSqlQuery()
        bOK = quer.exec_(scrpt)
        if not bOK:
            last = -99
            verbTxt = quer.lastError.text()
            msg.error("error "+ str(verbTxt))
            return (bOK, last)
        else:
            bNums = quer.first()
            if bNums:
                last = quer.value(0)
            else:
                last = 0
            return (bOK, last)

 
def insertVal( tblName=None, val=None, ordBy=None, lstNames=None, lstVal=None, lstQuot=None):
    """ Funcao usada para inserir valores na base de dados,
        primeiro ela verifica se foi o primeiro elemento
        e none, caso seja None significa que o id e auto incremente
        entao ela excuta a funca getLast
        Args:
            tblName = Nome da tabela
            val = o Nome da coluna na base de dados
            ordBy =  o nome da coluna que devera ser ordenada
            lstNames = lista dos nomes das colunas
            lstVal = lista dos valores correspondente
            lstQuot =  lista do valores se vamos querer colocar eles entre '' ou nao (interios e booleanos fica entre '', mas os outros nao)
    """
    bOK=False
    msgOut = None
    if tblName is None or lstNames is None or lstVal is None:
        msg.error('Nao foi possivel criar o script, porque nao foi passado todos argumentos.')
        return bOK
    else:
        if lstVal[0] is None or lstVal[0] is '':
            if val is None and  ordBy is None:
                returndBok, last = getLast(tblName= tblName)
            else:
                returndBok, last = getLast(tblName= tblName, val=val, ordBy=ordBy)           
            if returndBok:
                lstVal[0] = str(int(last) + 1)       
        bOK, istStr = script.insertScp(tblName= tblName, lstNames= lstNames, lstVals=lstVal , lstQuot= lstQuot)
        quer = QSqlQuery()
        if not bOK:
            msg.error("Erro ao criar o script")
            return bOK, None
        else:
            istStr= istStr.replace(" 'NULL',", " NULL,")
            b_Exec= quer.prepare(istStr)
            if b_Exec:
                b_Exec = quer.exec_(istStr)
                if b_Exec:
                    msgOut= "Dados Inseridos"
                else:
                    verbTxt=quer.lastError().text()
                    msg.error("Error: Nao sera possivel Inserir os Dados.",verbTxt=str(verbTxt))
            else:
                verbTxt=quer.lastError().text()
                msg.error("Error: Nao sera possivel Inserir os Dados.",verbTxt=str(verbTxt))
        return b_Exec, msgOut
    
 
def updateVal(tblName=None , lstNames=None , lstVals=None , lstQuot=None ,  cond=None , conVal=None , condQuot=None ):
        """
        Metodo para atualizar dados, na base de dados.
        
        Args:
            - tblName - Nome da tabela 
            - lstNames - Lista dos campos que vamos querer autualizar
            - lstVals - os Valores dos campos
            - lstQuot - List se of valores seram Quotes
            - cond - onde queremos atualizar Ex:(id)
            - conVal - o valor Ex:(1)
            - condQuod - se sera quoted.
        """ 
        msgOut = None
        bOK =False
        bOk, updstr = script.updateScp(tblName=tblName , lstNames=lstNames , lstVals=lstVals , lstQuot=lstQuot ,  cond=cond , conVal=conVal , condQuot=condQuot )
        quer = QSqlQuery()
        if bOk:
            updstr= updstr.replace(" 'NULL' ,", " NULL,")
            b_Exec = quer.exec_(updstr)
            if b_Exec:
                txt= str(cond)+" e igual a "+str(conVal)
                msgOut= "Dados atualizados onde "+str(txt)
                bOK = True
            else:
                verbTxt=quer.lastError().text()
                msg.error(txt="Error ao atulizar os dados Na tabela "+str(tblName), verbTxt=verbTxt)
                bOK = False
        else:
            msg.error()
            bOK = False       
        return bOK, msgOut


def deleteVal(tblName=None , cond=None , conVal=None , condQuot=None ):
        """
        Metodo para atualizar dados, na base de dados.
        
        Args:
            - tblName - Nome da tabela 
            - cond - onde queremos atualizar Ex:(id)
            - conVal - o valor Ex:(1)
            - condQuod - se sera quoted.
        """ 
        bOk, deldstr = script.deletScrpt(tblName=tblName, cond=cond, conVal=conVal, condQuot=condQuot)
        quer = QSqlQuery()
        if bOk:
            b_Exec = quer.exec_(deldstr)
            if b_Exec:
                txt= "Dados removidos onde "+str(cond)+" e igual a "+str(conVal)
                msg.Sucessos(txt)
                return True
            else:
                verbTxt=quer.lastError().text()
                msg.error(txt="Error ao Remover os dados Na tabela "+str(tblName), verbTxt=verbTxt)
                return False
        else:
            msg.error()
            return False  


def anySelectScript(scpt=None,fldNum=None):
    "::>> Metodo para execurar query de select que retorna uma linha"
    
    quer = QSqlQuery()
    b_Exec = quer.exec_(scpt)
    valOut = []
    if b_Exec:
        if quer.first():
            if fldNum is None:
                fldNum = quer.record().count()
            for i in range(fldNum):
                valOut.append(quer.value(i))
        else:
            b_Exec = False
    else:
        verbTxt=quer.lastError().text()
        msg.error(txt="Error ", verbTxt=verbTxt)
    return b_Exec, valOut
    
def verifyInDatabase(scpt=None):
    values = anySelectScript(scpt)[1]
    if len(values) == 0:
        return False
    else:
        return True

def multLineSelect(scpt):  
    """Metodo para executar select de multilinhas"""
    try: 
        quer = QSqlQuery()
        b_Exec = quer.exec_(scpt)
        if b_Exec:
            quer.last()
            fldRow = int(quer.at()) + 1
            fldCol = quer.record().count()
            quer.first()
            valOut=[]
            for i in range(fldRow):
                valOut.append(None)
                colOut=[]
                for j in range(fldCol):
                    colOut.append(quer.value(j))
                valOut[i]=colOut
                quer.next()
            return b_Exec, valOut
        else:
            verbTxt=quer.lastError().text()
            msg.error(txt="Error ", verbTxt=verbTxt)
            valOut=None
            return b_Exec, valOut
    except Exception:
        msg.error(txt="Error ", verbTxt="Nao foi Possivel aceder a Base de Dados")
        valOut=None
        return b_Exec, valOut
    