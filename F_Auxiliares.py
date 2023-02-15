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
Liga_Marshall = 251                                                                    #Liga a prensa em estado marshall
Liga_Cbr = 252                                                                              #Liga a prensa em estado Cbr
Retorna_Prensa = 253                                       #Retorna a prensa para a posição 0 do sensor de deslocamento
Desliga_Prensa = 254                                                                     #Desliga a prensa imediatamente
Funcionamento_Modo = 257
"""=====================================================================================================================
                                                  FUNÇÕES
====================================================================================================================="""
def open():                                                   #Função que conecta à porta e o baud do dispositivo serial
    global comport,Port
    if not comport.is_open:
        try:
            comport = serial.Serial(port=Port,baudrate=256000)
        except IOError:
            comport.close()
            comport.open()

def close():
    global comport
    comport.close

def is_open():                                                               #Função que estabelece a comunicação serial
    global comport
    return comport.is_open

def write_byte(byte):
    if comport.is_open:
        comport.write((byte, ))

def read_line():
    return comport.readline()

def reset_input_buffer():
    if comport.is_open:
        comport.reset_input_buffer()

class Messege1:
    def __init__(self, Master):                             #Cria as labels que indicam estado e funcionamento da prensa
        self.label_port = Label(Master, text="COMx", font="Arial 16 bold", bg="black", fg="white")
        self.label_port.place(width=105, height=29, x=71, y=219)
        self.label_forca = Label(Master, text="0.0  Kg/F", font="Arial 22 bold", bg="black", fg="yellow")
        self.label_forca.place(width=249, height=44, x=405, y=70)
        self.label_deslocamento = Label(Master, text="0.0  mm", font="Arial 22 bold", bg="black", fg="yellow")
        self.label_deslocamento.place(width=249, height=44, x=1080, y=66)
        self.label_mensagem = Label(Master, text="---", font="Arial 22 bold", bg="black", fg="yellow")
        self.label_mensagem.place(width=904, height=57, x=245, y=629)

    def port(self, color, port):
        global Port
        Port = port
        self.label_port["fg"] = color
        self.label_port["text"] = port

    def forca(self, forca):
        forca = forca
        self.label_forca["text"] = forca + " Kg/F"

    def deslocamento(self, deslocamento):
        deslocamento = deslocamento
        self.label_deslocamento["text"] = deslocamento + " mm"

    def botton(self, mensagem,color):
        self.label_mensagem["text"] = mensagem
        self.label_mensagem["fg"] = color
"""=====================================================================================================================            
                                               FIM DO PROGRAMA
====================================================================================================================="""
