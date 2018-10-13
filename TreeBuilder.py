from PyQt5.Qt import QAbstractItemModel, QModelIndex, Qt
class TreeNode(object): #Estrutura de dados Hirarica
    def __init__(self, name, parent=None):
        
        self._name = name #Name of the Node 
        self._children = [] #Children of the Node
        self._parent = parent #Parent of the Node
        
        
        if parent is not None:
            '''
            Adds a child to parente.
            self is the new child
            parent is the parent
            '''
            parent.addChild(self)
    
    
    def typeInfo(self):
        '''
        Informacao Do tipo de Nodo
        Ex: Nodo Provincia
        '''
        return "Nodo"
            
            
    def addChild(self, child):
        #Add the given child to the Chidren list
        self._children.append(child)
        child._parent = self
        
    def name(self):
        #Get the name of the node
        return self._name
    
    def child(self, row):
        #get the child at that exact position
        return self._children[row]

    def childCount(self):
        #Get the number of childs ther are inside the child list
        return len(self._children)
    
    def parent(self):
        #Get the parent object
        return self._parent
    
    def row(self):
        #gets the row of the of the Node->Parent->Children  
        if self._parent is not None:
            return self._parent._children.index(self)
        
    def setName(self, name):
        #Sets a name for the the node 
        self._name = name
        
        
    def log(self, tablevel=-1):
        #Used to make something like this
        '''
        |---1
            |---1.1
            |---1.2
        .
        .
        .   
        '''
        output = ""
        tablevel +=1
        
        for i in range(tablevel):
            #adds Escaping char tab or tabular on text
            # tablevel of time
            output += '\t'
            
        output += '|-----'+self._name+'\n'
        
        for child in self._children:
            output += child.log(tablevel)#Creats another log inside the log (inseption) 
        
        tablevel -= 1
        output += '\n'
        
        return output
    
    
    def setParent(self, new_parent):
        self._parent._children.remove(self)
        self._parent = new_parent
        new_parent._children.append(self)
        
    
    def removeChild(self):
        parent = self.parent()
        for idx in range(len(parent._children)):
            child = parent._children[idx]
            if self == child:
                #when on the selected child 
                #remove it form the tree and all its sub childs
                childOut= parent._children.pop(idx)
                childOut._parent = None
                return True
        return False
        
    
class TreeModel(QAbstractItemModel):
    #Input: root object of type TreeView_Node.th0_Nodo
    def __init__(self, root, parent=None):
        super(TreeModel, self).__init__(parent)
        self._rootNode = root

    #input QmodelIndex
    #Output int
    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()
        return parentNode.childCount()
    
    
    #input QmodelIndex
    #Output int
    def columnCount(self, parent):
        return 1
    
    
    #input QmodelIndex, int
    #Output QVariant, string are cast to QString which is a QVariant
    def data(self, index, role):
        if not index.isValid():
            return None
        
        node = index.internalPointer()
        
        if role == Qt.DisplayRole or role ==Qt.EditRole:
            if index.column() == 0:#column corresponds to the header section
                return node.name()
            else:
                return node.typeInfo()
        
        
    #Input int, Qt:: Orientation, int
    #Output QVariant, string are cast to QString which is a QVariant
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if section == 0:
                return "Area"
            else:
                return "Descrição"
    
    
    #Input ModelIndex
    #Int(flag)
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable #|Qt.ItemIsEditable
    
    #QModelIndex
    #QModelIndex
    #Should return the paren of the node with the given QModelIndex
    def parent(self, index):
        node = index.internalPointer()
        parentNode = node.parent()

        if parentNode == self._rootNode:
            return QModelIndex()
        
        return self.createIndex(parentNode.row(), 0, parentNode)
        
        
    #int, int, QModelIndex
    #QModelIndex
    #should return the a QModelIndex that corresponds to the given Row, column and parent Node
    def index(self, row, column, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()
        childItem = parentNode.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()


class th0_Nodo(TreeNode):
    """
    Sub-Class do Nodo 
    Usa-se este para criar o nodo princinpal
    """
    def __init__(self, name, parent=None):
        super().__init__(name, parent)#Super class constructor
        
    def typeInfo(self):
        return "Descrição"


#===============================================================================
# class th1_Nodo(TreeNode):
#     """
#     Sub-Class do Nodo 
#     Usa-se este para criar o nodo secundario
#     """
#     def __init__(self, name, parent=None):
#         super().__init__(name, parent)#Super class constructor
#         
#     def typeInfo(self):
#         return "Departamento"
#===============================================================================
