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
from PyQt5.Qt import QDialog
from PyQt5.Qt import QFileDialog
import QT_msg
import mixedModel
import shelve


class Generic_extra(QDialog):

    #on click get the path where the file is (IMG)
    def getFile(self):
        isImg=None
        lstImg = ['.jpg', '.png', '.jpeg', '.gif', '.tiff', '.bmp']
        filepath, _ = QFileDialog().getOpenFileName(self, "Select File", "","Images or pdf(*.png *.jpg *.pdf *.gif *.tiff *.bmp")
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
        name = "File_MX"
        date = str(self.DEData.date().year()) +'_'+ str(self.DEData.date().month()) +'_'+ str(self.DEData.date().day()) +'_'+  str(datetime.today().hour)  +'_'+  str(datetime.today().minute) +'_'+  str(datetime.today().second)
        doctype = mixedModel.getDataCombox(widg=self.CBType)
        nameOut = name+date+doctype
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
                    pdf.add_page()
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
    
    
    def AddMetadata(self, lstPdfIn, cat=None):
        lstNameOut= []
        if lstPdfIn != []:
            try:
                Mx_name = self.name_Generator()
                for idx, pdf in enumerate(lstPdfIn):
                    
                    if self.PTEInfo.toPlainText() == '':
                        info = 'N/A'
                    else:
                        info = self.PTEInfo.toPlainText()
                        
                    dictIn= {
                            'cod':self.SBCod.text(),
                            'doc_num':idx,
                            'nome':Mx_name,
                            'data':datetime.today().date().isoformat(),
                            'horas':datetime.today().time().isoformat(),
                            'doc_type':self.CBType.currentText(),
                            'info':info,
                            'systemEncoding':os.sys.getfilesystemencoding(),
                            'os':platform.platform()
                            }
                    
                    trailer = PdfReader(pdf) #Open the pdf FIle
                    metadata = PdfDict(cod = dictIn['cod'],doc_num = dictIn['doc_num'], nome = dictIn['nome'], data = dictIn['data'], 
                                       horas = dictIn['horas'], doc_type = dictIn['doc_type'], info = dictIn['info'], 
                                       systemEncoding = dictIn['systemEncoding'], os = dictIn['os'], numero = idx)#Dict where we gointo insert our metadata
                    trailer.Info.clear() #we clear the default data that the lib adds
                    trailer.Info.update(metadata)#We add our own Metadata
                    _, file = os.path.split(pdf)
                    abs_path = self.getDirMx()
                    if abs_path == None:
                        return False, None
                    else:
                        file_path = self.return_path(abs_path, 'File_Mx', cat)
                        #file_mx = file[:7] #separe the firts 6 char
                        file_name = self.extract_file_name(file) + ".pdf"
                        namePath = os.path.join(file_path, file_name)
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

    def return_path(self, cwd=None, start=None, category=None):
        self.create_month_dict()

        parent = os.path.join(cwd, start)
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