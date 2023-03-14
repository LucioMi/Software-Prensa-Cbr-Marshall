"""==================================================================================================================================================
                                                            IMPORTAÇÕES
=================================================================================================================================================="""
from tkinter import*
from tkinter import messagebox
import F_Auxiliares
import threading
import serial.tools.list_ports
from time import sleep
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import animation
import pymysql
from subprocess import run         
from datetime import datetime
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4                               
"""==================================================================================================================================================
                                                     VARIAVEIS DO PROGRAMA
=================================================================================================================================================="""
buscar_ComPorts = False                                            #variavel que controla a busca por comunicação serial
eixo_y_forca = []; eixo_x_deslocamento = []                        #listas que guardam os valores de força e deslocamento
serial_forca = ''                                                  #valor de força em tempo real
prensa_ligada = False                                              #variavel que diz se o ensaio esta em andamento
data_atual = datetime.now()
data_str = data_atual.strftime('Relatorio_Marshall_%d-%m-%Y_%H-%M')     #transforma a data atual no nome do arquivo
pastaApp = os.path.dirname(f'Relatorios\{data_str}.pdf')           #caminho da pasta do pdf
"""==================================================================================================================================================
                                                             FUNÇÕES
=================================================================================================================================================="""
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
            port_list.delete('0', 'end')
            idx = 0
            for port in sorted(ports):
                port_list.insert(idx, port.device)
                idx = idx + 1
                port_list["height"] = idx
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
            messagem.botton("CONECTADO!, Ajuste o sensor de delocamento", "green")
            if not recebendo_serial.is_alive():
                recebendo_serial.start()
    else:
        F_Auxiliares.comport.close()
        messagem.botton("DESCONECTADO!", "red")

#Recebe os dados de força e deslocamento do microcontrolador, trata esses dados, salva esses dados em variaveis e exibe para o usuario
def recebe_dados_serial():
    global eixo_y_forca, eixo_x_deslocamento, serial_forca
    while True:
        sleep(0.3)
        if F_Auxiliares.comport.is_open:                                                  #verifica se ha comunicação serial
            F_Auxiliares.comport.reset_input_buffer()                                     #'limpa' a comunicação serial
            try:
                serial_forca = str(F_Auxiliares.comport.readline())                       #leitura da comunicação serial
                serial_forca = serial_forca.replace("b'", ""); serial_forca = serial_forca.replace("r", "")
                serial_forca = serial_forca.replace("\\", ""); serial_forca = (float(serial_forca.replace("n'", ""))) / 100
                eixo_y_forca.append(serial_forca)
                messagem.forca(str(serial_forca))
                serial_deslocamento = str(F_Auxiliares.comport.readline())
                serial_deslocamento = serial_deslocamento.replace("b'", ""); serial_deslocamento = serial_deslocamento.replace("r", "")
                serial_deslocamento = serial_deslocamento.replace("\\",""); serial_deslocamento = (float(serial_deslocamento.replace("n'",""))) / 100
                eixo_x_deslocamento.append(serial_deslocamento)
                messagem.deslocamento(str(serial_deslocamento))   
            except IOError:
                messagem.forca("ERRO!"); messagem.deslocamento("ERRO!")

#Inicia o ensaio se as condições para realizalo estiverem sendo atendidas, informa o usuario.
def iniciar_ensaio():       #voltar ate aqui
    global serial_deslocamento, ax, animar
    if F_Auxiliares.comport.is_open:  
        if float(serial_deslocamento) < 0.1 or b == True:         
            if F_Auxiliares.comport.is_open:
                #Cria uma animação na tela que é o grafico de força x deslocamento
                F_Auxiliares.comport.write((F_Auxiliares.Liga_Marshall, ))         #envia o byte que é o comando de ligar em modo CBR (251) na serial
                figura = plt.Figure(figsize=(8, 4), dpi=60,facecolor='orange')
                ax = figura.add_subplot(facecolor=(.0, .50, .0))
                canva = FigureCanvasTkAgg(figura, tela4)
                canva.get_tk_widget().place(width=1052, height=410, x=290, y=173)
                animar = animation.FuncAnimation(figura, plotar, interval=1000, frames=10)        #gera a animação e chama a função que a "comandara"
                b = True                                                              #Variavel de controle so pra não gerar um bug na programação
                messagem.botton('Ensaio em andamento!', "green")
            else:
                messagebox.showwarning("ERRO!!!!!", "O computador não esta conectado com a prensa")
                messagem.botton('ATENÇÃO: Conecte o seu computador com a prensa...', "red")
        else:
            messagebox.showwarning("ERRO!!!!!", "Para iniciar o ensaio o deslocamento deve ser igual a 0, ajuste o sensor de deslocamento")
            messagem.botton('ATENÇÃO: Ajuste o sensor de deslocamento para a posição 0', "red")

#Grafico em tempo real até que deslocamento maximo, quando atingido retorna a prensa para a posição inicial e chama a função de criar o relatorio
def plotar(i):
    global eixo_y_forca, eixo_x_deslocamento, prensa_ligada, serial_forca
    if prensa_ligada == False:     
        prensa_ligada = True       
    forca_max_atual = None
    for num in eixo_y_forca:
        if (forca_max_atual is None or num > forca_max_atual):                                  
            forca_max_atual = num
    if forca_max_atual > (serial_forca + 500.00):
        if len(eixo_y_forca) == len(eixo_x_deslocamento):
            #Gerando grafico em tempo real
            ax.clear()
            ax.plot(eixo_x_deslocamento, eixo_y_forca, ls='-', lw=2, marker='o',color='black')
            ax.axis('tight')
            ax.grid(True)
            ax.set_title('GRAFICO: FORÇA(Kg/f) x DESLOCAMENTO(mm)', fontsize=28)
            ax.set_xlabel('DESLOCAMENTO (mm)', fontsize=22)
            ax.set_ylabel('FORÇA (Kg/F)', fontsize=22)
    else:
        F_Auxiliares.comport.write((F_Auxiliares.Retorna_Prensa,)) #byte que retorna a prensa para a posição 0 (deslocamento == 0)
        prensa_ligada = False 
        messagem.botton('Fim do ensaio!', "green")
        gerar_relatorio_cbr()                                                             #função de criaro relatorio

#Para a prensa imediatamente se o ensaio for interrompido, informa o usuario
def parar_ensaio():
    if F_Auxiliares.comport.is_open:
        F_Auxiliares.comport.write((F_Auxiliares.Desliga_Prensa,))          #Escreve na porta serial o byte que deslica a prensa (254)
        messagem.botton('PARADA MANUAL!!!. O ensaio foi interrempido durante sua execução', "red")
        messagebox.showwarning("PARADA MANUAL!!!", "Amostra comprometida os dados do formulario seram apagados e você sera redirecionado para a tela inicial")
        F_Auxiliares.comport.close() 
        tela4.destroy()
        run(r"Funcionalidades\P1_TelaPrincipal.exe", shell=True)
    else:
        messagem.botton('Informação: Se deseja voltar para a tela anterior clique no botão "VOLTAR"', "red")
        messagebox.showwarning("ERRO!!!!!!!!!!","O ensaio ainda não foi iniciado")

#Volta para a pagina inicial caso o ensaio não tenha ainda não tenha sido iniciado, informa o usuario
def voltar_pagina():
    if prensa_ligada == True:
        messagem.botton('Ensaio em andamento, se deseja parar o ensaio pressione o botão "PARAR"', "red")
    else:
        F_Auxiliares.comport.close() 
        tela4.destroy()       
        run(r"Funcionalidades\P2_FormularioMarshall.exe", shell=True)

#Cria o pdf do relatorio e fecha o aplicativo
def gerar_relatorio_marshall():
    global pastaApp, data_str, eixo_y_forca, eixo_x_deslocamento, forca_relatorio 
    F_Auxiliares.comport.close()                                                                                #Fecha a comunicação serial
    #Connecta com o DB, pega os dados e manipula-os para usalos no relatorio
    conexao = pymysql.connect ( host='localhost', user='root', passwd='',database='db_prensa_software')
    cursor = conexao.cursor()


"""==================================================================================================================================================
                                 CRIAÇÃO DE WIDGETS, LAYOUT DA TELA, BUSCA POR COMUNICAÇÃO SERIAL
=================================================================================================================================================="""
#Cria janela do tipo tk
tela4 = Tk()
tela4.title("Ensaio Marshall"); tela4.iconbitmap(default=r"Funcionalidades\tela1.ico"); tela4.geometry('1366x705+-11+1')
img_fundo = PhotoImage(file=r"Funcionalidades\Tela_Ensaio_Marshall.png"); label_fundo = Label(tela4, image=img_fundo); label_fundo.place(x=0, y=0)

#cria os botões presentes na tela
B_LigaMar = Button(tela4, text = "INICIAR ENSAIO", bg = "dark green", bd = 4, font = ("Arial", 18), command = iniciar_ensaio)
B_LigaMar.place(width=211, height=53, x=45, y=458)
B_ParaMar = Button(tela4, text="PARAR ENSAIO", bg="red", font=("Arial", 18), bd=5, command=parar_ensaio) 
B_ParaMar.place(width=211, height=53, x=45, y=532)
B_Voltar = Button(tela4, text="VOLTAR", bd=4, bg="yellow", font=("Arial", 18), command=voltar_pagina)
B_Voltar.place(width=211, height=53, x=45, y=606)
B_Buscar = Button(tela4, text="Buscar", bd=4, bg="blue", font=("Arial", 18), command=botao_buscar); B_Buscar.place(width=122, height=34, x=91, y=344)
B_Conectar = Button(tela4, text="Conectar", bd=4, bg="blue", font=("Arial", 16), command = botao_conectar)
B_Conectar.place(width=122, height=34, x=91, y=390)
#cria uma lista para escolher em qual porta COM a prensa esta conectada
port_list = Listbox(tela4, height=1, width=7, bd=10, font="Arial 10", bg="black", fg="#008000", highlightcolor="black", highlightthickness=0,
highlightbackground="black"); port_list.place(width=122, height=99, x=90, y=233); port_list.insert(END, "----")                                     
port_list.bind('<Double-Button>', lambda e: messagem.port("green", port_list.get(ANCHOR)))

#threding para buscar portas para comunicação serial
Buscar_ports = threading.Thread(target=buscar_ComPorts); Buscar_ports.daemon = True; Buscar_ports.start()
#threding para receber dados por comunicação serial
recebendo_serial = threading.Thread(target=recebe_dados_serial); recebendo_serial.daemon = True

#coneção com as labels de exibição da tela
messagem = F_Auxiliares.Messege1(tela4)

tela4.mainloop()
"""==================================================================================================================================================
                                                               FIM DO PROGRAMA
=================================================================================================================================================="""