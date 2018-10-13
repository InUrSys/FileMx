'''
Created on Oct 13, 2018

@author: chernomirdinmacuvele
'''
from ui_TreeForm import Ui_Dialog
from PyQt5.Qt import QDialog, QLabel, Qt, QLineEdit, QCheckBox, QPushButton,\
    QVBoxLayout, QTreeView
import TreeBuilder
import AbsMethods
import os
import shelve


class BuildTree(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.mdxClicked = None
        self.nodoRoot = None
        self.mainAppFolder = None
        
        self.setRootObj()
        self.setModel()
        
        self.twTreeObj.clicked.connect(self.onTreeClick)
        self.twTreeObj.doubleClicked.connect(self.onDoubleClicked)
        self.pbAdd.clicked.connect(self.onAddClicked)
        self.pbRemove.clicked.connect(self.onRemoveClicked)
        self.tbClean.clicked.connect(self.setToNone)
        self.pbMake.clicked.connect(self.onMakeClicked)
        
        
    def onMakeClicked(self):
        nodoObj = self.nodoRoot
        print(nodoObj.log())
        #Create a shelve object and store 
        #the dictionary and the noot objects
        shelveFile = shelve.open('mainConfig')
        shelveFile['mainRoot'] = self.nodoRoot
        shelveFile['mainDict'] = self.dictInfo
        shelveFile.close()
        
    
    def onTreeClick(self, mdx):
        self.mdxClicked = mdx
        self.pbRemove.setEnabled(True)
        #Get Name to set On label Clicked
        nodoObj = mdx.internalPointer()
        nome = nodoObj.name()
        self.lbItem.setText(nome)
        
        
    def onRemoveClicked(self):
        #check if and item is clicked
        if self.mdxClicked != None:
            nodoObj = self.mdxClicked.internalPointer()
            nodoObj.removeChild()
            self.removeDict(nodoObj)
            self.setModel()
    
    
    def removeDict(self, parent):
        path, _ = self.dictInfo.pop(parent)
        AbsMethods.deleteFolder(path)
        
        
    def onAddClicked(self):
        nameOut, ToStore = AbsMethods.getName(self.dictInfo) #Get name and if it is to store
        ParentNodoObj = self.getParentNodes() #get parent nodo object
        bOK, dirFolder = AbsMethods.setFolder(nameOut, ParentNodoObj, self.dictInfo) #adiconar folder ao directorio main
        if bOK:
            nodoObj = TreeBuilder.th0_Nodo(nameOut, ParentNodoObj)
            self.setDict(nodoObj, dirFolder, ToStore)
            self.setModel()
        else:
            #add msgBox here
            print("Nao sera possivel criar directorio porque o directorio ja e existente!")
    
    
    def onDoubleClicked(self, mdix):
        #when double clicked change the name of the selected Elemente and its folder
        nodoObj = mdix.internalPointer()
        parent, newFolderName, toStore = AbsMethods.editFolder(nodoObj, self.dictInfo)
        if parent != None:
            self.setDict(parent, newFolderName, toStore)
        self.setToNone()
    
    
    def getParentNodes(self):
        '''
        Get Parent nodes
        '''
        if self.mdxClicked == None:
            '''
            Set child from root
            '''
            nodoObj = self.nodoRoot
        else:
            '''
            Set child from sub-root
            '''
            nodoObj = self.mdxClicked.internalPointer()
        return nodoObj
    
    
    def setDict(self, nodoObj, newFolder, ToStore):
        '''
        Set nodo object, folder path, to store data in the dict
        '''
        self.dictInfo[nodoObj] = (newFolder, ToStore)
    
    
    def setRootObj(self):
        rootName = "File Mx"
        self.nodoRoot = TreeBuilder.th0_Nodo(rootName) #Creates a nodo
        rootModel = TreeBuilder.TreeModel(self.nodoRoot) #Convert the nodo to a model
        self.twTreeObj.setModel(rootModel)
        self.mainAppFolder = AbsMethods.createMainFolder()
        self.setMainDict()
    
    
    def setMainDict(self):
        toSorte = False#Guardar Dados 
        self.dictInfo = {self.nodoRoot:(self.mainAppFolder, toSorte)}

    
    def setModel(self):
        rootModel = TreeBuilder.TreeModel(self.nodoRoot)
        self.twTreeObj.setModel(rootModel)
        self.twTreeObj.expandAll()
        self.setToNone()
        
        
    def setToNone(self):
        self.mdxClicked = None
        self.lbItem.setText("Nenhum")
        self.pbRemove.setEnabled(False)
        
    