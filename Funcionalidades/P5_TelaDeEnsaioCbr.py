"""=====================================================================================================================
                                          IMPORTAÇÃO DE MODULOS
====================================================================================================================="""
from tkinter import *
import serial.tools.list_ports
from time import sleep
import F_Auxiliares
import threading

buscar_ComPorts = False
eixo_x_forca = []; eixo_y_forca = []
"""=====================================================================================================================
                                                  FUNÇÕES
====================================================================================================================="""
def botao_buscar():
    global buscar_ComPorts
    buscar_ComPorts = True

def buscar_ComPorts():
    global buscar_ComPorts
    while True:
        sleep(0.3)
        if buscar_ComPorts:
            messagem.botton('AGUARDE, procurando COM PORT...', "red")
            ports = serial.tools.list_ports.comports(include_links=False)
            lista_ComPorts.delete('0', 'end')
            idx = 0
            for port in sorted(ports):
                lista_ComPorts.insert(idx, port.device)
                idx = idx + 1
                lista_ComPorts["height"] = idx
                buscar_ComPorts = False
                messagem.botton('BUSCA FINALIZADA, escolha a COM PORT...', "yellow")

def botao_conectar():
    if F_Auxiliares.Port == 'COMx':
        messagem.botton('BUSCA FINALIZADA, escolha a COM PORT...', "yellow")
        return None
    if not F_Auxiliares.comport.is_open:
        F_Auxiliares.open()
        if F_Auxiliares.comport.is_open:
            messagem.botton("CONECTADO!", "green")
            sleep(2.5)
            if not recebendo_serial.is_alive():
                recebendo_serial.start()
    else:
        F_Auxiliares.comport.close()
        messagem.botton("DESCONECTADO!", "red")

def recebe_dados_serial():
    global eixo_x_forca, eixo_y_forca
    while True:
        sleep(0.3)
        if F_Auxiliares.comport.is_open:
            F_Auxiliares.comport.reset_input_buffer()
            try:
                serial_temporaria1 = str(F_Auxiliares.comport.readline())
                serial_temporaria1 = serial_temporaria1.replace("b'", "")
                serial_temporaria1 = serial_temporaria1.replace("r", "")
                serial_temporaria1 = serial_temporaria1.replace("\\", "")
                serial_temporaria1 = (float(serial_temporaria1.replace("n'", ""))) / 100
                eixo_x_forca.append(serial_temporaria1)
                messagem.forca(str(serial_temporaria1))
                serial_temporaria2 = str(F_Auxiliares.comport.readline())
                serial_temporaria2 = serial_temporaria2.replace("b'", "")
                serial_temporaria2 = serial_temporaria2.replace("r", "")
                serial_temporaria2 = serial_temporaria2.replace("\\", "")
                serial_temporaria2 = (float(serial_temporaria2.replace("n'", ""))) / 100
                eixo_y_forca.append(serial_temporaria2)
                messagem.deslocamento(str(serial_temporaria2))
            except IOError:
                messagem.forca("ERRO!")
                messagem.deslocamento("ERRO!")

"""
                serial_data2 = F_Auxiliares.read_line()
                serial_data2 = str(serial_data2)
                serial_data2 = serial_data2.replace("b'", "")
                serial_data2 = serial_data2.replace("r", "")
                serial_data2 = serial_data2.replace("\\", "")
                serial_data2 = serial_data2.replace("n'", "")
                serial_data2 = serial_data2.replace(".00", "")
                serial_data2 = float(serial_data2) / 100
                Grafico_Deslocamento = float(serial_data2)
                y.append(Grafico_Deslocamento)
                messagem.deslocamento(str(serial_data2))
            except IOError:
                messagem.forca("ERRO!")
                messagem.deslocamento("ERRO!")
"""





"""=====================================================================================================================
                            CRIAÇÃO DE WIDGETS,LAYOUT DA TELA E CONECÇÃO COM O BD
====================================================================================================================="""
#CRIA JANELA DO TKINTER
tela5 = Tk()
#tela5.iconbitmap(default=r"Funcionalidades\tela1.ico")
tela5.iconbitmap(default="tela1.ico")
tela5.title("Ensaio CBR")
tela5.geometry('1366x705+-11+1')
#img_fundo = PhotoImage(file=r"Funcionalidades\tela_formulario_cbr.png")
img_fundo = PhotoImage(file="tela_ensaio_cbr.png")
label_fundo = Label(tela5, image=img_fundo); label_fundo.place(x=0, y=0)

messagem = F_Auxiliares.Messege1(tela5)                           #CONECÇÃO COM AS LABELS DE EXIBIÇÃO DE DADOS DO ENSAIO

#CRIA OS BOTOES DA TELA
B_Buscar = Button(tela5, text="Buscar", bd=4, bg="orange", font=("Arial", 18), command=botao_buscar)
B_Buscar.place(width=122, height=34, x=91, y=344)
B_Conectar = Button(tela5, text="Conectar", bd=4, bg="orange", font=("Arial", 18), command=botao_conectar)
B_Conectar.place(width=122, height=34, x=91, y=390)
#CRIA LISTA CLICAVEL PARA O USUARIO ESCOLHER A COM PORT
lista_ComPorts = Listbox(tela5, height=1, width=7, bd=10, font="Arial 10", bg="black",
                    fg="green", highlightcolor="black", highlightthickness=0, highlightbackground="black")
lista_ComPorts.place(width=122, height=99, x=90, y=233)
lista_ComPorts.insert(END, "------")
lista_ComPorts.bind('<Double-Button>', lambda e: messagem.port("orange", lista_ComPorts.get(ANCHOR)))

#VAREDURA PARA BUSCAR PORTAS ENQUANTO A VARIAVEL FOR 'TRUE'
Buscar_ports = threading.Thread(target=buscar_ComPorts)                             #Busca por dispositivos seriais
Buscar_ports.daemon = True
Buscar_ports.start()
#VARREDURA PARA VER SE A DADOS A RECEBER/CONECÇÃO COM A PORTA SERIAL
recebendo_serial = threading.Thread(target=recebe_dados_serial)                    #REFERENCIA À receiving_serial
recebendo_serial.daemon = True

tela5.mainloop()
"""=====================================================================================================================            
                                               FIM DO PROGRAMA
====================================================================================================================="""

