'''
Created on Oct 12, 2018

@author: chernomirdinmacuvele
'''
from time import sleep
import subprocess
from PyQt5.Qt import QThread, pyqtSignal

class Thread_Internet_Status(QThread):
    status = pyqtSignal(bool, name="Internet Status")
    
    def __init__(self, ):
        super().__init__()
        
        
    def internet_on(self):
        '''
        Check if there is internet
        '''
        timeout = 1
        address = "8.8.8.8"
        rc = subprocess.call("ping -c 1 -W %d %s" % (timeout, address),
                            shell=True, stdout=open('.pingOut.txt','w'), 
                            stderr = subprocess.STDOUT)
        if rc == 0:
            #print("Yes Internet")
            return True
        else:
            #print("No Internet")
            return False
    
    
    def run(self):
        #Verifica se tem coneccao a internet
        while True:
            bOK = self.internet_on()
            self.status.emit(bOK)
            sleep(1)
                

