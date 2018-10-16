from PyQt5.Qt import QThread, pyqtSignal
from CloudStorage import setConnectionToCloud
import google.cloud.storage.bucket as go
import time

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