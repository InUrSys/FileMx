'''
Created on Oct 13, 2018

@author: chernomirdinmacuvele
'''
import os
from PyQt5.Qt import QDialog, QLabel, Qt, QLineEdit, QCheckBox, QPushButton,\
    QVBoxLayout
import shutil
import send2trash
    
    
def createMainFolder():
    pathOut = os.path.expanduser(os.path.join('~','File Mx'))#Get path to user’s home directory
    if not os.path.exists(pathOut):
        os.makedirs(pathOut)
    return pathOut

def createFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def createSavedPaths(shelveDictInfo): #recieves the DictInfo of the directories created

    paths = []
    dictValues = list(shelveDictInfo.values())
    for path in dictValues:
        paths.append(path[0])

    for path in paths:
        createFolder(path)



def getName(dictInfo, parent=None):
    '''
    Get Name and to store
    '''
    nome = "Nome"
    toSave = False
    if parent != None:
        #get name
        #get toSave
        nome = parent.name()
        _, toSave = dictInfo[parent]
        
    popOut = PopOut(nome, toSave)
    popOut.exec()
    nameOut, bOK = popOut.items
    return nameOut, bOK


def setFolder(folderName, parent, dictInfo):
    '''
    Metodo para adicionar nova pasta ao directorio do parent
    '''
    dirParent = getDirFromDict(dictInfo, parent)
    newFolder = os.path.join(dirParent, folderName)
    if not os.path.isdir(newFolder):
        os.makedirs(newFolder)
        return True, newFolder
    return False, None
   
    
def getDirFromDict(dictInfo, parent):
    '''
    Get parent directory
    '''
    dirParent, _ = dictInfo[parent]
    return dirParent


def editFolder(parent, dictInfo):
    #get folder
    pathDir = getDirFromDict(dictInfo, parent)
    newName, toStore = getName(dictInfo, parent)
    if newName != None:
        parentParent =  parent.parent()
        parentDir = getDirFromDict(dictInfo, parentParent)
        newFolderName = os.path.join(parentDir, newName)
        if not os.path.isdir(newFolderName):
            shutil.move(pathDir, newFolderName)  
            parent.setName(newName)   
        return parent, newFolderName, toStore
    return None, None, None


def deleteFolder(folder):
    try:
        send2trash.send2trash(folder)
    except OSError:
        pass


class PopOut(QDialog):
        '''
        Pop Out para modificar ou adicionar nome de um elemento na arvore
        '''
        def __init__(self, name, bOK=False):
            super().__init__()
            
            self.items = None, None
            
            self.setWindowFlags(Qt.FramelessWindowHint)
            
            self.lineEdit = QLineEdit(name)
            
            self.chbStore =  QCheckBox()
            self.chbStore.setText("Guardar dados")
            self.chbStore.setChecked(bOK)
            
            self.pbOK = QPushButton()
            self.pbOK.setText("OK")
            self.pbOK.clicked.connect(self.getNewName)
            
            self.pbCancel = QPushButton()
            self.pbCancel.setText("Cancel")
            self.pbCancel.clicked.connect(self.close)
            
            layout = QVBoxLayout()
            layout.addWidget(self.lineEdit)
            layout.addWidget(self.chbStore)
            layout.addWidget(self.pbOK)
            layout.addWidget(self.pbCancel)
            
            self.setLayout(layout)
            
        
        def getNewName(self):
            nome = self.lineEdit.text()
            toStore = self.chbStore.isChecked()
            self.items = (nome, toStore)
            self.close() 
    