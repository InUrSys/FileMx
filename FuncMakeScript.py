#-*- coding: utf-8 -*-
"""
Modulo para cricao de scripts SQL
este modol vai permitir que criem scrits sql flexiveis 
para insersao, atulizacao e leitura dos dados na base de 
dados. 
"""
 
def readScp(tblName, lstNames, condName=None, condVal=None, condQuot=None ):
    """Genarates a SQL Select script, that can select in a give position 
    or not, by creating the frist part of the script with the table name
    then we provide the list of the values the table has, then it will
    verify we gave it condition, if we gave then it will pass them 
    the condition can be given as a list or string, if its a list it
    must be same size or it will report an error.
     
    Note:
        the args can be list or string except for tblName that string only
    Args:
        tblName: table name
        lstNames: list of names on the data base tables
        cond: condition where 
        Valcond: condition values
     
    """
    try:
        bOK=False
        isList, isString, _ = _verf(lstNames)
        if isList:
            sql = "SELECT " + _lst2Str(lstNames) +" FROM "
        elif isString:
            sql = "SELECT " + lstNames +" FROM "
        sql += tblName
        bOK=True
        if condName and condVal is not None:
            isList, isString, isEqual = _verf(condName, condVal, condQuot)
            if isList and isEqual:
                if condQuot is not None:
                    sql +=" WHERE " + _lst2Val(condName, condVal, " AND ", condQuot)
                else:
                    sql +=" WHERE " + _lst2Val(condName, condVal, " AND ")
                bOK=True
            elif isString:
                if condQuot:
                    sql += " WHERE " + condName +" = '"+ str(condVal)+"'"
                else:
                    sql += " WHERE " + condName +" = "+ str(condVal)
                bOK=True
            else:
                print("Type error: Select script Faild to creat") 
                bOK=False
    except:
        bOK = False
        sql = None
    return (bOK, sql)
 
  
def insertScp(tblName, lstNames, lstVals, lstQuot=None):
    """Genarates a SQL Insert script, that can insert data into the table 
    if the insert was sucessfull it will return True else False.
      
    Note:
        the args can be list or string except for tblName that string only
    Args:
        tblName: table name
        lstNames: list of names on the data base tables
        lstVals:  are the values we want to insert
        lstType: is more like a quote or not quote method
      
    """
    try:
        bOK= False
        sql = "INSERT INTO " + tblName + " ("
        isList, isString, isEqual = _verf(lstNames=lstNames, lstVal=lstVals, lstQut=lstQuot)
        if isList and isEqual:
            fldNames = _lst2Str(lstNames)
            fldVals = _lst2Str(lstVals, lstQuot)
            bOK = True       
        elif isString:
            fldNames = lstNames
            fldVals = lstVals
            bOK = True 
        else:
            bOK = False  
        sql = sql + fldNames
        sql = sql + ") VALUES ("
        sql = sql + fldVals
        sql = sql + ")"
    except:
        bOK = False
        sql = None
    return (bOK, sql)
  
  
def updateScp(tblName, lstNames, lstVals, lstQuot, cond, conVal, condQuot):
    """Genarates a SQL Update script, that can insert data into the database table 
    if the up was sucessfull it will return True else False,
    frist it verifis if it is list or string, if it is list, it will check to see if the length 
    is is the same on the list of elementes and the list of values.
    if it is string it will go and creat the query, it does the same for the conditions on where.
       
    Note:
        the args can be list or string except for tblName that string only
    Args:
        tblName: table name
        lstNames: list of names on the data base tables
        lstVals:  are the values we want to insert
        lstType: is more like a quote or not quote method
        con: where do we want to update
        valcond: the value corresponding to it
        typcond: if the value cond is quotable
       
    """
    try:
        bOK = False
        sql = "UPDATE " + tblName + " SET  "
        isList, isString, isEqual = _verf(lstNames=lstNames, lstVal=lstVals, lstQut=lstQuot)
        if isList and isEqual:
            sql += _lst2Val(lstNames=lstNames, lstVal=lstVals,lstQuot=lstQuot)
            bOK= True
        elif isString:
            if lstQuot:
                sql += lstNames +" = '"+lstVals+"'"
            else:
                sql += lstNames +" = "+lstVals
            bOK= True    
        else:
            print("Type error: secao 1") 
            bOK = False 
        condisList, condisString, condisEqual = _verf(lstNames=cond, lstVal=conVal, lstQut=condQuot)
        if condisList and condisEqual:
            lstOut= _lst2Val(lstNames, lstVals, " AND ", lstQuot)
            sql +=" WHERE ( " + lstOut +" )"
        elif condisString:
            if condQuot:
                sql += " WHERE " + cond +" = '"+ str(conVal)+"'"
            else:
                sql += " WHERE " + cond +" = "+ str(conVal)
        else:
            print("Type error: secao 1") 
            bOK = False 
    except:
        bOK = False
        sql = None
    return(bOK, sql)
         
         


def deletScrpt(tblName=None,  cond=None, conVal=None, condQuot=None): 
    bOK=False
    if cond is None or conVal is None or condQuot is None:
        return bOK, None
    else:
        sql = "DELETE FROM "+tblName
        if condQuot:
            sql += " WHERE " + cond +" = '"+ str(conVal)+"'"
        else:
            sql += " WHERE " + cond +" = "+ str(conVal)
        bOK=True
        return bOK, sql
        
             
    
         
def _lst2Str(lstNames, lstQuot=None):
    """Fucntion to convert List to Str
    The function takes 2 arguments, 
    a lstNames: the data we want to remove from the list
    and the lstQuote: if the data is quoted or not.
    How does it do?
    - it will verf if we gave a lst of quotes, 
    if we did it will quote the data that needs to be quoted
    else it will just convert the list to string.
    """
    strOut=None
    if lstQuot is None:
        strOut=", ".join(lstNames)
    else:
        for idx, val in enumerate(lstNames):
            if lstQuot[idx]:
                lstNames[idx]="'"+val+"'"
        strOut=", ".join(lstNames)
    return strOut
    
    
def _lst2Val(lstNames, lstVal, sep=" , ", lstQuot=None):
    """list to string of values
    these func will atribute the data to the given
    name and value, we only need to supply a list of
    names, list of values and a list of is quoted or not.
    if we dont supply a list of quotedes it will attribute 
    to them quotes for all, else only the especified data
    """
    strOut = None
    lst2str = []
    if lstQuot is None:
        for idx, val in enumerate(lstNames):
            val2 = str(lstVal[idx])
            lst2str.append(val+" = '"+val2+"'")
        strOut=sep.join(lst2str)
    else:
        for idx, val in enumerate(lstNames):
            val2 = "'"+str(lstVal[idx])+"'"
            if lstQuot[idx]:
                lst2str.append(val+" = "+val2)
            else:
                lst2str.append(val+" = "+val2.replace("'", ""))
        strOut=sep.join(lst2str)
    return strOut


def _verf(lstNames, lstVal=None, lstQut=None):
    """ Verification, this func verf if the
    argumets passed are Lists or Strings,
    if they are list it will verf if they all have the same
    length.
    """
    alList = False
    alString = False
    alEqual = False
     
    if lstVal is None and lstQut is None:
        alList = True if isinstance(lstNames, list) else False
        alString =  True if isinstance(lstNames, str) else False
         
    elif lstNames is not None and lstVal is not None:
        alList = True if isinstance(lstNames, list) and isinstance(lstVal, list) else False
        alString = True if isinstance(lstNames, str) else False
        if alList:
            alEqual = True if len(lstNames) is len(lstVal) else False
             
    else:
        alList = True if isinstance(lstNames, list) and isinstance(lstVal, list) and isinstance(lstQut, list) else False
        alString = True if isinstance(lstNames, str) and isinstance(lstVal, str) else False
        if alList:
            alEqual = True if len(lstNames) is len(lstVal) is len(lstQut) else False
     
    return (alList, alString, alEqual)

