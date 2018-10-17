'''
Created on 25/04/2018

@author: chernomirdinmacuvele
'''
from PIL import Image
import subprocess
from fpdf.fpdf import FPDF
from pdfrw.pdfreader import PdfReader
from pdfrw.objects.pdfdict import PdfDict
from pdfrw.pdfwriter import PdfWriter
from pprint import pprint
from pdfrw.pagemerge import PageMerge
import os
import platform
from datetime import datetime
from PyQt5.Qt import QDialog, QStandardItemModel, QStandardItem, QDate,\
    QTableView, QTableWidget, QTableWidgetItem, QTime
from PyQt5.Qt import QFileDialog
import QT_msg
import mixedModel
import shelve
import google.cloud.storage.blob as g
import CloudStorage
from Services import Thread_Google_Uploader

class Generic_extra(QDialog):
    
    def uploadMainConfig(self, jsonFile, bucketName):
        bucket = CloudStorage.setConnectionToCloud(jsonFile, bucketName)
        fileName = "mainConfig"
        extLst = ['.dir', '.bak', '.db', '.dat']
        for ext in extLst:
            cFile = fileName+ext
            if os.path.exists(cFile):
                fileToUpload = cFile
                break
        blob = bucket.blob(fileToUpload)
        if blob != None:
            blob.upload_from_filename(fileToUpload)
    
    
    def getMainConfig(self, jsonFile, bucketName):
        bucket = CloudStorage.setConnectionToCloud(jsonFile, bucketName)
        lstBuckets = bucket.list_blobs()
        extLst = ['mainConfig.dir', 'mainConfig.bak', 'mainConfig.db', 'mainConfig.dat']
        for blob in lstBuckets:
            nome = blob.name
            for ext in extLst:
                if nome == ext:
                    blob.download_to_filename(nome)
                    break
                
        #blob = CloudStorage.setBlobToGet(fileName, bucket, jsonFile, NomeBalde)
        
        
        
    
    def filterPath(self, lstIn):
        lstOut =[]
        mainPath = os.path.expanduser(os.path.join('~','File Mx'))
        for path in lstIn:
            _, pathNeeded = path.split('File Mx')
            newPath = mainPath+pathNeeded
            if os.path.exists(newPath):
                lstOut.append(newPath)
        return lstOut
        
    
    
    def checkMainConfig(self):
        fileName = "mainConfig"
        extLst = ['.dir', '.bak', '.db', '.dat']
        for ext in extLst:
            cFile = fileName+ext
            if os.path.exists(cFile):
                return True
        return False
    
    
    def makeModel(self, tbView, mtxIn):
        tbView.setRowCount(len(mtxIn))
        tbView.setColumnCount(len(mtxIn[0]))
        for i, row in enumerate(mtxIn):
            for j, val in enumerate(row):
                if type(val) == QDate:
                    val = val.toPyDate().isoformat()
                elif type(val) == QTime:
                    val = val.toPyTime().isoformat()
                elif type(val) == g.Blob:
                    val = val.name
                item = QTableWidgetItem(str(val))
                tbView.setItem(i,j, item)
        self.setMainTableHeader(self, tbView)
    
    #on click get the path where the file is (IMG)
    def getFile(self):
        isImg=None
        lstImg = ['.jpg', '.png', '.jpeg', '.gif', '.tiff', '.bmp']
        filepath, _ = QFileDialog().getOpenFileName(self, "Select File", "","Images or pdf(*.png *.jpg *.jpeg *.pdf *.gif *.tiff *.bmp")
        if filepath != '':
            _, formatX = os.path.splitext(filepath)
            formatX = formatX.lower()
            if formatX in lstImg:
                isImg=True
            else:
                isImg=False 
        return (isImg, filepath)
    
    
    def checkIfEqual(self, valIn, OgLst):
        #Check if exists a equal file in the list
        bOK=False
        if valIn in OgLst:
            bOK = True
        else:
            bOK = False
        return bOK
    
    
    def clickedItem(self, mdx=None):
        self.clkFilePath = mdx
        
        
    def DoubleclickedItem(self,mdx=None):
        self.mdx=mdx
        path = mdx.model().data(mdx)
        sop = os.sys.platform.lower()
        if sop == 'darwin':
            subprocess.Popen(['open', path])
        elif sop == 'windows':
            subprocess.Popen(path, shell=True)
        else:
            QT_msg.aviso(txt="Sistema Operativo Desconhecido. Contacte o Criador.")
            
    
    def name_Generator(self):
        self.create_month_dict()
        month = self.month_string.get(str(self.DEData.date().month()))
        
        name = "FileMX"
        date = str(self.DEData.date().year()) +'_'+ month +'_'+ str(self.DEData.date().day())
        tempo = str(datetime.today().hour)  +'_'+  str(datetime.today().minute) #+'_'+  str(datetime.today().second)
        doctype = mixedModel.getDataCombox(widg=self.CBType)
        nameOut = name+"__"+date+"__"+tempo+"__"+doctype+"__"
        return nameOut
    
    
    def FusionImg(self, lstImgFile):
        output_list = []
        namePath = None
        if lstImgFile != []:
            pdf = FPDF(orientation='P', unit='cm', format='A4') #::> BS :mod: 06_07_2018
            for imgFile in lstImgFile:
                imgObj = Image.open(imgFile)
                w,h = imgObj.size
                if w > h: #landscape Mode
                    pdf.add_page('L')
                    x,y,w,h = 0.3, 0.5, 29, 20 #For LandScape mode
                    pdf.image(imgFile,x,y,w,h)#x,y,w,h
                else:
                    pdf.add_page('P')
                    x,y,w,h = 0.5, 0.3, 20, 29
                    pdf.image(imgFile,x,y,w,h)#x,y,w,h

            """::>>BackSlash : modified : 06_07_2018"""
            if len(lstImgFile) > 1:
                nameOut = self.extract_file_name(self.name_Generator()) + ".pdf"
            else:
                nameOut = self.extract_file_name(os.path.basename(imgFile)) + ".pdf"
            try:
                os.makedirs('temp_files')
            except FileExistsError:
                pass
            namePath = os.path.join('temp_files', nameOut)
            pdf.output(namePath, "F")
            output_list.append(namePath)
            return output_list

            """    
            nameOut = str(self.LEName.text())+".pdf"
            try:
                os.makedirs('temp_files')
            except FileExistsError:
                pass
            namePath = os.path.join('temp_files',nameOut)
            pdf.output(namePath, "F")
        return namePath  
        """
    
    
    def AddMetadata(self, lstPdfIn):
        lstNameOut= []
        if lstPdfIn != []:
            try:
                
                Mx_name = self.name_Generator()
                for idx, pdf in enumerate(lstPdfIn):
                    _, file = os.path.split(pdf)
                    file_name = self.extract_file_name(file) 
                    if self.PTEInfo.toPlainText() == '':
                        info = 'N/A'
                    else:
                        info = self.PTEInfo.toPlainText()
                    
                    
                    dictIn= {
                            'doc_num':str(idx+1)+" Of "+str(len(lstPdfIn)),
                            'nome':file_name,
                            'data':datetime.today().date().isoformat(),
                            'horas':datetime.today().time().isoformat(),
                            'treePath': self.CBToStore.currentText(),
                            'doc_type':self.CBType.currentText(),
                            'info':info,
                            'systemEncoding':os.sys.getfilesystemencoding(),
                            'os':platform.platform()
                            }
                    
                    trailer = PdfReader(pdf) #Open the pdf FIle
                    metadata = PdfDict(doc_num = dictIn['doc_num'], nome = dictIn['nome'], data = dictIn['data'], 
                                       horas = dictIn['horas'], treePath=dictIn['treePath'], doc_type = dictIn['doc_type'], info = dictIn['info'], 
                                       systemEncoding = dictIn['systemEncoding'], os = dictIn['os'], numero = idx)#Dict where we gointo insert our metadata
                    trailer.Info.clear() #we clear the default data that the lib adds
                    trailer.Info.update(metadata)#We add our own Metadata
                    
                    abs_path = self.CBToStore.currentText()
                    if abs_path == None:
                        return False, None
                    else:
                        cat =self.CBType.currentText()
                        file_path = self.return_path(abs_path, cat)
                        #file_mx = file[:7] #separe the firts 6 char
                        
                        namePath = os.path.join(file_path, Mx_name+ ".pdf")
                        PdfWriter().write(namePath, trailer)
                        lstNameOut.append(namePath)
                bOK=True
            except:
                bOK=False
                #Check if it is encrypted 
                try:
                    PdfReader(pdf)
                except ValueError:
                    QT_msg.aviso(txt='O Ficherio <i>'+pdf+'</i> esta <b>Corrompido</b> ou <b>Encriptado</b>, queria por favor removê-lo e voltar a tentar.')
        else:
            bOK=None
        return bOK, lstNameOut
            
    
    def getDirMx(self):
        pathToDir = None
        shelfFile = shelve.open('pathToDir')
        try:
            pathToDir = shelfFile['dir']
        except KeyError:
            QT_msg.aviso(txt="Não Sera possivel Guardar. <p>Porque ainda não Foi selecionado o Local onde os Ficheiros vão ficar.</p>")
        shelfFile.close()
        return pathToDir
    
    
    def checkWhiteSpace(self, string=None):
        if string is None:
            return False
        evaluator = string.split(" ");
        if len(evaluator) > 1:
            return True
        else:
            return False

    def return_path(self, cwd=None, category=None):
        self.create_month_dict()

        parent = cwd
        year = str(self.DEData.date().year())
        month = self.month_string.get(str(self.DEData.date().month()))

        """::>> Step 1: Check if the filename for the user has been created!"""
        if not os.path.exists(parent):
            os.makedirs(parent)

        child = os.path.join(parent, category)
        if not os.path.exists(child):
            os.makedirs(child)

        grand_child = os.path.join(child, year)
        if not os.path.exists(grand_child):
            os.makedirs(grand_child)

        grand_grand_child = os.path.join(grand_child, month)
        if not os.path.exists(grand_grand_child):
            os.makedirs(grand_grand_child)

        return grand_grand_child

    def setMainTableHeader(self, tableWidget):
        headerList = ['Ficheiro', 'Tipo de Documento', 'Data', 'Hora']
        for i, txt in enumerate(headerList):
            tableWidget.setHorizontalHeaderItem(i,QTableWidgetItem(txt))
            
            
    def create_month_dict(self):
        self.month_string = {
            '1': "Jan",
            "2": "Feb",
            "3": "Mar",
            "4": "Apr",
            "5": "May",
            "6": "Jun",
            "7": "Jul",
            "8": "Aug",
            "9": "Sep",
            "10": "Oct",
            "11": "Nov",
            "12": "Dec"

        }

    def extract_file_name(self, filename=None):
        file_components = filename.split(".")
        file_name = file_components[0]
        return file_name