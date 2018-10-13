'''
Created on Oct 11, 2018

@author: chernomirdinmacuvele
@colaborator: felicianoMAZOIO
'''
from google.cloud import storage


#Create sotrage client
#connectar google cloud Storage
jsonFile = 'File Mx EE-de38156917d4.json'
NomeBalde = '1_empresa'

def setConnectionToCloud(jsonFile, NomeBalde):
    try:
        storage_client = storage.Client.from_service_account_json(jsonFile)
        bucket = storage_client.get_bucket(NomeBalde)
    except Exception:
        return None
    return bucket


def setBlob(fileName, jsonFile, NomeBalde):
    bucket = setConnectionToCloud(jsonFile, NomeBalde)
    #to upload file 
    if bucket != None:
        #nome que o ficheiro tera na cloud
        blobToUpload = bucket.blob(fileName)
        if blobToUpload.exists():
            blob = blobToUpload
        else:
            blob = bucket.get_blob(fileName)
        return blob


def upload(blob, fileToUpload):
    #to upload \blod
    blob.upload_from_filename(fileToUpload)


def download(blob, fileToDown):
    #download
    blob.download_to_filename(fileToDown)


def delete(blob):
    #delete jus need a blob
    blob.delete()
    
