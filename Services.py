from PyQt5.Qt import QThread, pyqtSignal
from CloudStorage import setConnectionToCloud
import google.cloud.storage.bucket as go
import time
import send2trash

class Thread_Google_Bucket(QThread):
    bucket = pyqtSignal(go.Bucket, name="Bucket")
    
    def __init__(self, jsonFile, bucketName):
        super().__init__()
        
        self.jsonFile = jsonFile
        self.bucketName = bucketName
        
    def run(self):
        while True:
            bucket = setConnectionToCloud(jsonFile=self.jsonFile, NomeBalde=self.bucketName)
            self.bucket.emit(bucket)
            time.sleep(1)


class Thread_Google_Uploader(QThread):
    done = pyqtSignal((bool, str), name="done")
    def __init__(self, blob, fileToUpload):
        super().__init__()
          
        self.blob = blob
        self.fileToUpload = fileToUpload
#          
    def run(self):
        self.blob.upload_from_filename(self.fileToUpload)
        #send2trash.send2trash(self.fileToUpload)
        self.done.emit(True, self.fileToUpload)