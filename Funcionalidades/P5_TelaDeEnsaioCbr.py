"""=====================================================================================================================
                                          IMPORTAÇÃO DE MODULOS
====================================================================================================================="""
from tkinter import *
import serial.tools.list_ports
from time import sleep
import F_Auxiliares
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import animation
from tkinter import messagebox
import Posicionador_De_Objetos

buscar_ComPorts = False                                            #variavel que controla a busca por comunicação serial
eixo_y_forca = []; eixo_x_deslocamento = []                       #listas que guardam os valores de força e deslocamento
serial_deslocamento = ''                                                            #valor do deslocamento em tempo real
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
    global eixo_y_forca, eixo_x_deslocamentoa, serial_deslocamento
    while True:
        sleep(0.3)
        if F_Auxiliares.comport.is_open:
            F_Auxiliares.comport.reset_input_buffer()
            try:
                serial_forca = str(F_Auxiliares.comport.readline())
                serial_forca = serial_forca.replace("b'", "")
                serial_forca = serial_forca.replace("r", "")
                serial_forca = serial_forca.replace("\\", "")
                serial_forca = (float(serial_forca.replace("n'", ""))) / 100
                eixo_y_forca.append(serial_forca)
                messagem.forca(str(serial_forca))
                serial_deslocamento = str(F_Auxiliares.comport.readline())
                serial_deslocamento = serial_deslocamento.replace("b'", "")
                serial_deslocamento = serial_deslocamento.replace("r", "")
                serial_deslocamento = serial_deslocamento.replace("\\", "")
                serial_deslocamento = (float(serial_deslocamento.replace("n'", ""))) / 100
                eixo_x_deslocamento.append(serial_deslocamento)
                messagem.deslocamento(str(serial_deslocamento))
            except IOError:
                messagem.forca("ERRO!")
                messagem.deslocamento("ERRO!")

def iniciar_ensaio():
    global serial_deslocamento, ax, animar
    if serial_deslocamento < 0.1:
        if F_Auxiliares.comport.is_open:
            F_Auxiliares.comport.write((252, ))                      #envia o byte que é o comando de ligar em modo CBR)
            figura = plt.Figure(figsize=(8, 4), dpi=60)
            ax = figura.add_subplot(111)
            canva = FigureCanvasTkAgg(figura, tela5)
            canva.get_tk_widget().place(width=1052, height=410, x=290, y=173)
            animar = animation.FuncAnimation(figura, plotar, interval=1000, frames=10)
        else:
            messagebox.showwarning("ERRO!!!!!", "O computador não esta conectado com a prensa")
            messagem.botton('ATENÇÃO: Conecte o seu computador com a prensa...', "red")
    else:
        messagebox.showwarning("ERRO!!!!!", "Para iniciar o ensaio o deslocamento deve ser igual a 0, "
                                            "ajuste o sensor de deslocamento")
        messagem.botton('ATENÇÃO: Ajuste o sensor de deslocamento para a posição 0', "red")

def plotar(i):
    global eixo_y_forca, eixo_x_deslocamento
    max = None
    for num in eixo_x_deslocamento:
        if (max is None or num > max):                                              #pega o valor maximo do deslocamento
            max = num

    if len(eixo_y_forca) == len(eixo_x_deslocamento):
        ax.clear()
        ax.plot(eixo_x_deslocamento, eixo_y_forca, ls='-', lw=2, marker='o')
        ax.axis([0, 25.5, 0, 5500])
        ax.grid(True)
        ax.set_title('GRAFICO: FORÇA(Kg/f) x DESLOCAMENTO(mm)', fontsize=28)
        ax.set_xlabel('DESLOCAMENTO (mm)', fontsize=22)
        ax.set_ylabel('FORÇA (Kg/F)', fontsize=22)






def parar_ensaio():
    F_Auxiliares.comport.write((253,))                                   #envia o byte que é o comando de parar a prensa






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
B_Iniciar = Button(tela5, text="INICIAR ENSAIO", bg="dark green", bd=4, font=("Arial", 18), command=iniciar_ensaio)
B_Iniciar.place(width=211, height=53, x=45, y=458)
B_Parar = Button(tela5, text="PARAR ENSAIO", bg="dark red", bd=4, font=("Arial", 18), command=parar_ensaio)
B_Parar.place(width=211, height=53, x=45, y=532)
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


tela5.bind('<Button-1>', lambda e: Posicionador_De_Objetos.m_btn1(e, tela5))
tela5.bind('<Button-3>', lambda e: Posicionador_De_Objetos.m_btn3(e, tela5))
tela5.bind('<ButtonRelease-1>', lambda e: Posicionador_De_Objetos.m_btn1_release(e, tela5))


tela5.mainloop()
"""=====================================================================================================================            
                                               FIM DO PROGRAMA
====================================================================================================================="""

