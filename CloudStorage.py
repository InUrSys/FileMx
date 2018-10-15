'''
Created on Oct 11, 2018

@author: chernomirdinmacuvele
@colaborator: felicianoMAZOIO
'''
from google.cloud import storage
from PyQt5.Qt import QDate, QTime
import time


#Create sotrage client
#connectar google cloud Storage
jsonFile = '/Users/chernomirdinmacuvele/Documents/workspace/File_MX_EE/File Mx EE-de38156917d4.json'
NomeBalde = '1_empresa'

def setConnectionToCloud(jsonFile, NomeBalde):
    try:
        storage_client = storage.Client.from_service_account_json(jsonFile)
        bucket = storage_client.get_bucket(NomeBalde)
    except Exception:
        return None
    return bucket


def setBlobToGet(fileName, jsonFile, NomeBalde):
    bucket = setConnectionToCloud(jsonFile, NomeBalde)
    #to upload file 
    if bucket != None:
        #nome que o ficheiro tera na cloud
        blob = bucket.blob(fileName)
        if blob.exists():
            blob = bucket.get_blob(fileName)
            return blob
        else:
            print("Ficherio nao Existe")
        
    
def setBlobToUpload():
    bucket = setConnectionToCloud(jsonFile, NomeBalde)
    #to upload file 
    if bucket != None:
        blob = bucket.blob(fileName)
        if blob.exists():
            print("Ficherio ja Existe")
        else:
            return blob


def getListItem(jsonFile, NomeBalde):
    bucket = setConnectionToCloud(jsonFile, NomeBalde)
    lst_blobs = bucket.list_blobs()
    lst=[]
    for blob in lst_blobs:
        nome = blob.name
        typeDoc, dateOut, timeOut = makeItReadeble(nome)
        lst.append((blob, typeDoc, dateOut, timeOut))
        
    print(lst)
    
def makeItReadeble(nome):
    lstData = nome.split('__')
    lstData.pop(0)
    date = lstData[0]
    time = lstData[1]
    typeDoc = lstData[2]
    dateOut = getDate(date)
    timeOut = getTime(time)
    return typeDoc, dateOut, timeOut
    

def getTime(timeIn):
    horas = int(timeIn.split('_')[0])
    minutos = int(timeIn.split('_')[1])
    timeQ = QTime(horas, minutos)
    return timeQ

    
def getDate(dateIn):
    month_string = {
                    "Jan":1,
                    "Feb":2,
                    "Mar":3,
                    "Apr":4,
                    "May":5,
                    "Jun":6,
                    "Jul":7,
                    "Aug":8,
                    "Sep":9,
                    "Oct":10,
                    "Nov":11,
                    "Dec":12
                    }
    ano = int(dateIn.split('_')[0])
    mes = month_string[dateIn.split('_')[1]]
    dia = int(dateIn.split('_')[2])
    
    dateQ = QDate(ano,mes, dia)
    return dateQ



def upload(blob, fileToUpload):
    #to upload \blod
    blob.upload_from_filename(fileToUpload)


def download(blob, fileToDown):
    #download
    blob.download_to_filename(fileToDown)


def delete(blob):
    #delete jus need a blob
    blob.delete()



startTime = time.time()
fileName = "FileMX__2000_Jan_1__20_25__Factura__.pdf"
setConnectionToCloud(jsonFile, NomeBalde)
#upload(blob, fileName)
print("--- %s seconds ---" % (time.time() - startTime))
