'''
Created on 26/08/2017
Modulo contendo funcoes para criar Menssangens de Texto,

- Confirmacao
- Aviso
- Error
- Sucessos
@author: chernomirdinmacuvele
'''
from PyQt5.Qt import QMessageBox
def is2insert(txt="Tem a certaza que gostari de realizar essa operacao?"):
    msg = QMessageBox()
    msg.setWindowTitle("Confirmação")
    msg.setText("            Confirmação            ")
    msg.setInformativeText(txt)
    msg.setIcon(QMessageBox.Question)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    clicked = msg.exec()
    resp = True if clicked == QMessageBox.Yes else False
    return resp
    
       
def inserted():
    msg = QMessageBox()
    msg.setWindowTitle("Sucesso")
    msg.setText("             Sucessos              ")
    msg.setInformativeText("Os Dados Foram inseridos com sucesso na base de dados")
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()
    

def updated(txt):
    msg = QMessageBox()
    msg.setWindowTitle("Sucesso")
    msg.setText("             Sucessos              ")
    msg.setInformativeText("Os Dados Foram Atualizados onde: "+txt+"  na base de dados")
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()


def aviso(txt):
    msg = QMessageBox()
    msg.setWindowTitle("Aviso")
    msg.setText("              Aviso                ")
    msg.setInformativeText(txt)
    msg.setIcon(QMessageBox.Warning)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def error(txt=None, verbTxt=None):
    msg = QMessageBox()
    msg.setWindowTitle("Erro")
    msg.setText("              Error                ")
    if txt is None and verbTxt is None:
        msg.setInformativeText("Erro Algo aconteceu tente De novo.")
    elif txt is not None and verbTxt is None:
        msg.setInformativeText(txt)
    else:
        msg.setInformativeText(txt)
        msg.setDetailedText(verbTxt)
    msg.setIcon(QMessageBox.Warning)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()


def Sucessos(txt):
    msg = QMessageBox()
    msg.setWindowTitle("Sucesso")
    msg.setText("             Sucessos              ")
    msg.setInformativeText(txt)
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()     