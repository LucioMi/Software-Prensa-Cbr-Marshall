"""=============================================================================================================================================================
                                                           IMPORTAÇÃO DE MODULOS
============================================================================================================================================================="""
from tkinter import *
import serial.tools.list_ports
from time import sleep
import F_Auxiliares
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import animation
from tkinter import messagebox
from subprocess import run
import Posicionador_De_Objetos
"""=============================================================================================================================================================
                                                                VARIAVEIS
============================================================================================================================================================="""
buscar_ComPorts = False                                            #variavel que controla a busca por comunicação serial
eixo_y_forca = []; eixo_x_deslocamento = []                        #listas que guardam os valores de força e deslocamento
serial_deslocamento = ''                                           #valor do deslocamento em tempo real
deslo_max_ensaio = 12.79                                           #valor maximo de deslocamento do ensaio cbr (controla o fim do ensaio)
"""=============================================================================================================================================================
                                                                FUNÇÕES
============================================================================================================================================================="""
#Função do botão de busca por portas COM
def botao_buscar():
    global buscar_ComPorts
    buscar_ComPorts = True

#Exibe todas as portas COM disponiveis na lista tkinter (lista_ComPorts), informa o usuario.
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

#Tenta realizar a conecção por comunicação serial e informa usuario o resultado.
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

#Recebe os dados de força e deslocamento do microcontrolador, trata esses dados, salva esses dados em variaveis e exibe para o usuario
def recebe_dados_serial():
    global eixo_y_forca, eixo_x_deslocamento, serial_deslocamento
    while True:
        sleep(0.3)
        if F_Auxiliares.comport.is_open:                                                  #verifica se ha comunicação serial
            F_Auxiliares.comport.reset_input_buffer()                                     #'limpa' a comunicação serial
            try:
                serial_forca = str(F_Auxiliares.comport.readline())                       #leitura da comunicação serial
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

#Inicia o ensaio se as condições para realizalo estiverem sendo atendidas, informa o usuario.
def iniciar_ensaio():
    global serial_deslocamento, ax, animar
    if float(serial_deslocamento) < 0.1:
        if F_Auxiliares.comport.is_open:
            F_Auxiliares.comport.write((F_Auxiliares.Liga_Cbr, ))                           #envia o byte que é o comando de ligar em modo CBR (252) por comunicação serial
            #Cria uma animação na tela que é o grafico de força x deslocamento
            figura = plt.Figure(figsize=(8, 4), dpi=60)
            ax = figura.add_subplot(111)
            canva = FigureCanvasTkAgg(figura, tela5)
            canva.get_tk_widget().place(width=1052, height=410, x=290, y=173)
            animar = animation.FuncAnimation(figura, plotar, interval=1000, frames=10)                #gera a animação e chama a função que a "comandara"
        else:
            messagebox.showwarning("ERRO!!!!!", "O computador não esta conectado com a prensa")
            messagem.botton('ATENÇÃO: Conecte o seu computador com a prensa...', "red")
    else:
        messagebox.showwarning("ERRO!!!!!", "Para iniciar o ensaio o deslocamento deve ser igual a 0, "
                               "ajuste o sensor de deslocamento")
        messagem.botton('ATENÇÃO: Ajuste o sensor de deslocamento para a posição 0', "red")

#Grafico em tempo real até que o deslomento maximo seja atingido, quando atingido retorna a prensa para a posição inicial e chama a função de criar o relatorio
def plotar(i):
    global eixo_y_forca, eixo_x_deslocamento
    desl_max_atual = None
    for num in eixo_x_deslocamento:
        if (desl_max_atual is None or num > desl_max_atual):                                  
            desl_max_atual = num
    if desl_max_atual < deslo_max_ensaio:
        if len(eixo_y_forca) == len(eixo_x_deslocamento):
            #Gerando grafico em tempo real
            ax.clear()
            ax.plot(eixo_x_deslocamento, eixo_y_forca, ls='-', lw=2, marker='o')
            ax.axis([0, 25.5, 0, 5500])
            ax.grid(True)
            ax.set_title('GRAFICO: FORÇA(Kg/f) x DESLOCAMENTO(mm)', fontsize=28)
            ax.set_xlabel('DESLOCAMENTO (mm)', fontsize=22)
            ax.set_ylabel('FORÇA (Kg/F)', fontsize=22)
    else:
        F_Auxiliares.comport.write((F_Auxiliares.Retorna_Prensa,))    #Escreve na porta serial o 253 que é o byte que retorna a prensa para a posição inicial (deslocamento == 0)
        gerar_relatorio_cbr()                 #função de criaro relatorio
"""
RELATORIO AIND NÃO DESENVOLVIDO VOLTAR AQUI DEPOIS
"""   
def gerar_relatorio_cbr():   
    print('RELATORIO CRIADO MEU TRUTA')
    messagem.forca(str("------"))
    messagem.deslocamento(str("------"))
    F_Auxiliares.comport.close() 

#Para a prensa imediatamente se o ensaio for interrompido, informa o usuario
def parar_ensaio():
    if F_Auxiliares.comport.is_open:
        F_Auxiliares.comport.write((F_Auxiliares.Desliga_Prensa,))  #Escreve na porta serial 0 byte que deslica a prensa (254)
        messagem.botton('PARADA MANUAL!!!. O ensaio foi interrempido durante sua execução', "red")
        messagebox.showwarning("PARADA MANUAL!!!", "Amostra comprometida os dados do formulario seram apagados e você sera redirecionado para a tela inicial")
        tela5.destroy()
        run(r"Funcionalidades\P1_TelaPrincipal.exe", shell=True)
    else:
        messagem.botton('Informação: Se deseja voltar para a tela anterior clique no botão "VOLTAR"', "red")
        messagebox.showwarning("ERRO!!!!!!!!!!","O ensaio ainda não foi iniciado")






"""=============================================================================================================================================================
                                             CRIAÇÃO DE WIDGETS,LAYOUT DA TELA E CONECÇÃO COM O BD
============================================================================================================================================================="""
#CRIA JANELA DO TKINTER
tela5 = Tk()
tela5.iconbitmap(default=r"Funcionalidades\tela1.ico")
tela5.title("Ensaio CBR")
tela5.geometry('1366x705+-11+1')
img_fundo = PhotoImage(file=r"Funcionalidades\tela_ensaio_cbr.png")
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

#VARREDURA PARA BUSCAR PORTAS ENQUANTO A VARIAVEL FOR 'TRUE'
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
"""============================================================================================================================================================ 
                                                               FIM DO PROGRAMA
============================================================================================================================================================="""