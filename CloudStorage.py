'''
Created on Oct 11, 2018

@author: chernomirdinmacuvele
@colaborator: felicianoMAZOIO
'''
from google.cloud import storage
from PyQt5.Qt import QDate, QTime
import time
import shutil
import os
import ExtraExtra
import send2trash

import QT_msg as msg
#Create sotrage client
#connectar google cloud Storage
#jsonFile = '/Users/chernomirdinmacuvele/Documents/workspace/File_MX_EE/File Mx EE-de38156917d4.json'
#NomeBalde = '1_empresa'

def setConnectionToCloud(jsonFile, NomeBalde):
    try:
        storage_client = storage.Client.from_service_account_json(jsonFile)
        bucket = storage_client.get_bucket(NomeBalde)
    except Exception:
        return None
    return bucket


def setBlobToGet(fileName, bucket=None, jsonFile=None, NomeBalde=None):
    if jsonFile != None and NomeBalde != None:
        bucket = setConnectionToCloud(jsonFile, NomeBalde)
    #to upload file 
    if bucket != None:
        #nome que o ficheiro tera na cloud
        blob = bucket.blob(fileName)
        if blob.exists():
            blob = bucket.get_blob(fileName)
            return blob
        else:
            msg.error("Erro!", "Ficheiro nao existe.")
        
    
def setBlobToUpload(fileName, bucket=None, jsonFile=None, NomeBalde=None):
    if jsonFile != None and NomeBalde != None:
        bucket = setConnectionToCloud(jsonFile, NomeBalde)
    #to upload file 
    if bucket != None:
        blob = bucket.blob(fileName)
        if blob.exists():
            msg.error("Error!", "Fichiero ja existente")
        else:
            return blob


def getListItem(bucket=None, jsonFile=None, NomeBalde=None):
    if jsonFile != None and NomeBalde != None:
        bucket = setConnectionToCloud(jsonFile, NomeBalde)
    if bucket != None:
        lst_blobs = bucket.list_blobs()
        lst=[]
        for blob in lst_blobs:
            nome = blob.name
            extLst = ['mainConfig.dir', 'mainConfig.bak', 'mainConfig.db', 'mainConfig.dat']
            if nome not in extLst:
                typeDoc, dateOut, timeOut = makeItReadeble(nome)
                lst.append((blob, typeDoc, dateOut, timeOut))
        return lst
    
    
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
    blob.upload_from_filename(fileToUpload)
    send2trash.send2trash(fileToUpload)
    

def download(blob, fileToDown):
    #download
    blob.download_to_filename(fileToDown)


def delete(blob):
    #delete jus need a blob
    blob.delete()




