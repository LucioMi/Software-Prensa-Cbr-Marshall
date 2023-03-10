"""=====================================================================================================================
                                          IMPORTAÇÃO DE MODULOS
====================================================================================================================="""
import serial
from tkinter import *
"""=====================================================================================================================
                                          VARIAVEIS DO PROGRAMA
====================================================================================================================="""
Port = "COMx"                                                     #Variavel que representa a porta da comunicação serial
comport = serial.Serial()                                                                 #Cria um objeto do tipo serial
#Terminadores para o reconhecimento dos comandos
Liga_Marshall = 251                                                              #Liga a prensa em estado marshall
Liga_Cbr = 252                                                                   #Liga a prensa em estado Cbr
Desliga_Prensa = 254                                                             #Desliga a prensa
Retorna_Prensa = 253                                                             #Retorna a prensa                                             
Funcionamento_Modo = 257
"""=====================================================================================================================
                                                  FUNÇÕES
====================================================================================================================="""
#VERIFICAÇÃO SE É POSSIVEL CONECTAR (SE A PORTA ESTA OPEN) E ATRIBUIÇÃO DO BAUD
def open():
    global comport,Port
    if not comport.is_open:
        try:
            comport = serial.Serial(port=Port,baudrate=256000)
        except IOError:
            comport.close()
            comport.open()

#LABELS DE EXIBIÇÃO DE DADOS DO ENSAIO
class Messege1:
    def __init__(self, Master):                             #Cria as labels que indicam estado e funcionamento da prensa
        self.label_port = Label(Master, text="------", font="Arial 16 bold", bg="black", fg="red")
        self.label_port.place(width=123, height=27, x=89, y=192)
        self.label_forca = Label(Master, text="------"+" Kg/f", font="Arial 22 bold", bg="darkblue", fg="red")
        self.label_forca.place(width=214, height=46, x=440, y=118)
        self.label_deslocamento = Label(Master, text="------"+" mm", font="Arial 22 bold", bg="darkblue", fg="red")
        self.label_deslocamento.place(width=214, height=46, x=1019, y=117)
        self.label_mensagem = Label(Master, text="------", font="Arial 22 bold", bg="black", fg="red")
        self.label_mensagem.place(width=1052, height=68, x=290, y=601)

    def port(self, color, port):
        global Port
        Port = port
        self.label_port["fg"] = color
        self.label_port["text"] = port

    def forca(self, forca):
        forca = forca
        self.label_forca["text"] = forca + " Kg/F"
        self.label_forca["fg"] = "orange"

    def deslocamento(self, deslocamento):
        deslocamento = deslocamento
        self.label_deslocamento["text"] = deslocamento + " mm"
        self.label_deslocamento["fg"] = "orange"

    def botton(self, mensagem,color):
        self.label_mensagem["text"] = mensagem
        self.label_mensagem["fg"] = color

#Converte o tamanho de pontos para milimetros em um pdf (reportlab)
def mm_ponto(mm):                                                        
    return mm/0.352777
"""=============================================================================================================================================================            
                                                                     FIM DO PROGRAMA
============================================================================================================================================================="""
