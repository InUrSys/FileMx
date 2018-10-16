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
            print("Correndo")
            time.sleep(1)
       
        
        
    #===========================================================================
    # def internet_on(self):
    #     '''
    #     Check if there is internet
    #     '''
    #     timeout = 1
    #     address = "8.8.8.8"
    #     rc = s.call("ping -c 1 -W %d %s" % (timeout, address),
    #                         shell=True, stdout=open('.pingOut.txt','w'), 
    #                         stderr = subprocess.STDOUT)
    #     if rc == 0:
    #         #print("Yes Internet")
    #         return True
    #     else:
    #         #print("No Internet")
    #         return False
    # 
    # 
    # def run(self):
    #     #Verifica se tem coneccao a internet
    #     while True:
    #         bOK = self.internet_on()
    #         self.status.emit(bOK)
    #         sleep(1)
    #===========================================================================
                