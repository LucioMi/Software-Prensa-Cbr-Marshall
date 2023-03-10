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
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from subprocess import run
import os
from datetime import datetime
import pymysql
"""=============================================================================================================================================================
                                                                VARIAVEIS
============================================================================================================================================================="""
buscar_ComPorts = False                                            #variavel que controla a busca por comunicação serial
eixo_y_forca = []; eixo_x_deslocamento = [] ; forca_relatorio = [] #listas que guardam os valores de força e deslocamento
serial_deslocamento = ''                                           #valor do deslocamento em tempo real
deslo_max_ensaio = 12.79                                           #valor maximo de deslocamento do ensaio cbr (controla o fim do ensaio)
prensa_ligada = False                                              #variavel que diz se o ensaio esta em andamento ou não
data_atual = datetime.now()
data_str = data_atual.strftime('Relatorio_Cbr_%d-%m-%Y_%H-%M')                   #transforma a data atual no nome do arquivo
pastaApp = os.path.dirname(f'Relatorios\{data_str}.pdf')                                        #caminho da pasta do pdf
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
                serial_forca = serial_forca.replace("b'", ""); serial_forca = serial_forca.replace("r", "")
                serial_forca = serial_forca.replace("\\", ""); serial_forca = (float(serial_forca.replace("n'", ""))) / 100
                eixo_y_forca.append(serial_forca)
                messagem.forca(str(serial_forca))
                serial_deslocamento = str(F_Auxiliares.comport.readline())
                serial_deslocamento = serial_deslocamento.replace("b'", ""); serial_deslocamento = serial_deslocamento.replace("r", "")
                serial_deslocamento = serial_deslocamento.replace("\\", ""); serial_deslocamento = (float(serial_deslocamento.replace("n'", ""))) / 100
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
                F_Auxiliares.comport.write((F_Auxiliares.Liga_Cbr, ))         #envia o byte que é o comando de ligar em modo CBR (252) por comunicação serial
                figura = plt.Figure(figsize=(8, 4), dpi=60,facecolor='orange')
                ax = figura.add_subplot(facecolor=(.0, .50, .0))
                canva = FigureCanvasTkAgg(figura, tela5)
                canva.get_tk_widget().place(width=1052, height=410, x=290, y=173)
                animar = animation.FuncAnimation(figura, plotar, interval=1000, frames=10)                   #gera a animação e chama a função que a "comandara"
                b = True                                                                            #Variavel de controle so pra não gerar um bug na programação
            else:
                messagebox.showwarning("ERRO!!!!!", "O computador não esta conectado com a prensa")
                messagem.botton('ATENÇÃO: Conecte o seu computador com a prensa...', "red")
        else:
            messagebox.showwarning("ERRO!!!!!", "Para iniciar o ensaio o deslocamento deve ser igual a 0, "
                                "ajuste o sensor de deslocamento")
            messagem.botton('ATENÇÃO: Ajuste o sensor de deslocamento para a posição 0', "red")
    else:
        pass

#Grafico em tempo real até que o deslomento maximo seja atingido, quando atingido retorna a prensa para a posição inicial e chama a função de criar o relatorio
def plotar(i):
    global eixo_y_forca, eixo_x_deslocamento, prensa_ligada
    if prensa_ligada == False:     
        prensa_ligada = True       
    desl_max_atual = None
    for num in eixo_x_deslocamento:
        if (desl_max_atual is None or num > desl_max_atual):                                  
            desl_max_atual = num
    if desl_max_atual < deslo_max_ensaio:
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
        F_Auxiliares.comport.write((F_Auxiliares.Retorna_Prensa,))  #Escreve na serial o 253, o byte que retorna a prensa para a posição 0 (deslocamento == 0)
        prensa_ligada = False 
        gerar_relatorio_cbr()                                                                                             #função de criaro relatorio

#Para a prensa imediatamente se o ensaio for interrompido, informa o usuario
def parar_ensaio():
    if F_Auxiliares.comport.is_open:
        F_Auxiliares.comport.write((F_Auxiliares.Desliga_Prensa,))                                   #Escreve na porta serial o byte que deslica a prensa (254)
        messagem.botton('PARADA MANUAL!!!. O ensaio foi interrempido durante sua execução', "red")
        messagebox.showwarning("PARADA MANUAL!!!", "Amostra comprometida os dados do formulario seram apagados e você sera redirecionado para a tela inicial")
        F_Auxiliares.comport.close() 
        tela5.destroy()
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
        tela5.destroy()       
        run(r"Funcionalidades\P3_FormularioCbr.exe", shell=True)

#Cria o pdf do relatorio e fecha o aplicativo
def gerar_relatorio_cbr():    
    global pastaApp, data_str, eixo_y_forca, eixo_x_deslocamento, forca_relatorio 
    F_Auxiliares.comport.close()                                                                                #Fecha a comunicação serial
#Connecta com o DB, pega os dados e manipula-os para usalos no relatorio
    conexao = pymysql.connect ( host='localhost',
                            user='root', passwd='',database='db_prensa_software')
    cursor = conexao.cursor()
    cursor.execute(f"SELECT altura_inicial FROM id_cp_cbr;") 
    altura_inicial = str(cursor.fetchall()); altura_inicial = altura_inicial.replace("((", ""); altura_inicial = altura_inicial.replace(",),)", "")
    cursor.execute(f"SELECT exp_umidade_otima  FROM id_cp_cbr;") 
    exp_umidade_otima = str(cursor.fetchall());exp_umidade_otima =exp_umidade_otima.replace("((", ""); exp_umidade_otima = exp_umidade_otima.replace(",),)", "")
    cursor.execute(f"SELECT id_molde FROM id_cp_cbr;") 
    id_molde = str(cursor.fetchall()); id_molde = id_molde.replace("(('", ""); id_molde = id_molde.replace("',),)", "")
    cursor.execute(f"SELECT leitura_exp0 FROM id_cp_cbr;") 
    leitura_exp0 = str(cursor.fetchall()); leitura_exp0 = leitura_exp0.replace("((", ""); leitura_exp0 = leitura_exp0.replace(",),)", "")
    cursor.execute(f"SELECT leitura_exp1 FROM id_cp_cbr;") 
    leitura_exp1 = str(cursor.fetchall()); leitura_exp1 = leitura_exp1.replace("((", ""); leitura_exp1 = leitura_exp1.replace(",),)", "")
    cursor.execute(f"SELECT leitura_exp2 FROM id_cp_cbr;") 
    leitura_exp2 = str(cursor.fetchall()); leitura_exp2 = leitura_exp2.replace("((", ""); leitura_exp2 = leitura_exp2.replace(",),)", "")
    cursor.execute(f"SELECT leitura_exp3 FROM id_cp_cbr;") 
    leitura_exp3 = str(cursor.fetchall()); leitura_exp3 = leitura_exp3.replace("((", ""); leitura_exp3 = leitura_exp3.replace(",),)", "")
    cursor.execute(f"SELECT leitura_exp4 FROM id_cp_cbr;") 
    leitura_exp4 = str(cursor.fetchall()); leitura_exp4 = leitura_exp4.replace("((", ""); leitura_exp4 = leitura_exp4.replace(",),)", "")
    cursor.execute(f"SELECT massa_amosta FROM id_cp_cbr;") 
    massa_amosta = str(cursor.fetchall()); massa_amosta = massa_amosta.replace("((", ""); massa_amosta = massa_amosta.replace(",),)", "")
    cursor.execute(f"SELECT massa_amostra_cilindro FROM id_cp_cbr;") 
    massa_amostra_cilindro = str(cursor.fetchall()); massa_amostra_cilindro = massa_amostra_cilindro.replace("((", ""); 
    massa_amostra_cilindro = massa_amostra_cilindro.replace(",),)", "")
    cursor.execute(f"SELECT massa_cilindro FROM id_cp_cbr;") 
    massa_cilindro = str(cursor.fetchall()); massa_cilindro = massa_cilindro.replace("((", ""); massa_cilindro = massa_cilindro.replace(",),)", "")
    cursor.execute(f"SELECT massa_esp_ap_seca FROM id_cp_cbr;") 
    massa_esp_ap_seca=str(cursor.fetchall()); massa_esp_ap_seca = massa_esp_ap_seca.replace("((", ""); massa_esp_ap_seca = massa_esp_ap_seca.replace(",),)", "")
    cursor.execute(f"SELECT peso_esp_umido FROM id_cp_cbr;") 
    peso_esp_umido = str(cursor.fetchall()); peso_esp_umido = peso_esp_umido.replace("((", ""); peso_esp_umido = peso_esp_umido.replace(",),)", "")
    cursor.execute(f"SELECT teor_umidade_media FROM id_cp_cbr;") 
    teor_umidade_media=str(cursor.fetchall());teor_umidade_media=teor_umidade_media.replace("((","");teor_umidade_media = teor_umidade_media.replace(",),)", "")
    cursor.execute(f"SELECT volume FROM id_cp_cbr;") 
    volume = str(cursor.fetchall()); volume = volume.replace("((", ""); volume = volume.replace(",),)", "")
    cursor.execute(f"SELECT amostra FROM id_ensaio_cbr;") 
    amostra = str(cursor.fetchall()); amostra = amostra.replace("(('", ""); amostra = amostra.replace("',),)", "")
    cursor.execute(f"SELECT dia FROM id_ensaio_cbr;") 
    dia = str(cursor.fetchall()); dia = dia.replace("(('", ""); dia = dia.replace("',),)", "")
    cursor.execute(f"SELECT energia FROM id_ensaio_cbr;") 
    energia = str(cursor.fetchall()); energia = energia.replace("((", ""); energia = energia.replace(",),)", "")
    cursor.execute(f"SELECT furo FROM id_ensaio_cbr;")
    furo = str(cursor.fetchall()); furo = furo.replace("(('", ""); furo = furo.replace("',),)", "")
    cursor.execute(f"SELECT material FROM id_ensaio_cbr;")
    material = str(cursor.fetchall()); material = material.replace("(('", ""); material = material.replace("',),)", "")
    cursor.execute(f"SELECT obra FROM id_ensaio_cbr;")
    obra= str(cursor.fetchall()); obra = obra.replace("(('", ""); obra = obra.replace("',),)", "")
    cursor.execute(f"SELECT operador FROM id_ensaio_cbr;")
    operador = str(cursor.fetchall()); operador = operador.replace("(('", ""); operador = operador.replace("',),)", "")
    cursor.execute(f"SELECT subtrecho FROM id_ensaio_cbr;")
    subtrecho = str(cursor.fetchall()); subtrecho = subtrecho.replace("(('", ""); subtrecho = subtrecho.replace("',),)", "")
    cursor.execute(f"SELECT trecho FROM id_ensaio_cbr;")
    trecho = str(cursor.fetchall()); trecho = trecho.replace("(('", ""); trecho = trecho.replace("',),)", "")
    cursor.close()
    #Cria o um grafico com os valores de força e deslocamento e salva em uma imagem
    plt.plot(eixo_x_deslocamento, eixo_y_forca, ls='-', lw=2, marker='o')
    plt.axis('tight')
    plt.grid(True)
    plt.ylabel('FORÇA (Kg/F)')
    plt.xlabel('DESLOCAMENTO (mm)')
    plt.title('GRAFICO: FORÇA(Kg/f) x DESLOCAMENTO(mm) ')
    plt.savefig(r"Funcionalidades\grafico_relatorio_cbr.png", dpi=150)                       
    #Escreve dados e imagens no pdf
    cnv = canvas.Canvas(pastaApp + f'\{data_str}.pdf',
                        pagesize=A4)                                                                                                #pasta,nome e tamanho do pdf 
    cnv.drawImage(r"Funcionalidades\relatorio_cbr_individual.png",                                   #coloca a imagem no ponto especolhido e no tamanho escolhido
                  F_Auxiliares.mm_ponto(0), F_Auxiliares.mm_ponto(0), width = F_Auxiliares.mm_ponto(210), height = F_Auxiliares.mm_ponto(297))
    cnv.drawImage(r"Funcionalidades\grafico_relatorio_cbr.png",                                     #coloca a imagem no ponto especolhido e no tamanho escolhido
                  F_Auxiliares.mm_ponto(0), F_Auxiliares.mm_ponto(0), width = F_Auxiliares.mm_ponto(230), height = F_Auxiliares.mm_ponto(120))
    cnv.drawString(F_Auxiliares.mm_ponto(26), F_Auxiliares.mm_ponto(278), f'REGISTRO')                                    #escreve no pdf no ponto escolhido
    cnv.drawString(F_Auxiliares.mm_ponto(86), F_Auxiliares.mm_ponto(278), f'{dia}')        
    cnv.drawString(F_Auxiliares.mm_ponto(154), F_Auxiliares.mm_ponto(278), f'{id_molde}') 
    if int(energia) == 12: x = 'Normal' 
    elif int(energia) == 26: x = 'Intermediária'
    else: x= 'Modificada'      
    cnv.drawString(F_Auxiliares.mm_ponto(23), F_Auxiliares.mm_ponto(270), f'{x}')       
    cnv.drawString(F_Auxiliares.mm_ponto(90), F_Auxiliares.mm_ponto(270), f'{energia}')        
    cnv.drawString(F_Auxiliares.mm_ponto(134), F_Auxiliares.mm_ponto(270), f'{amostra}')        
    cnv.drawString(F_Auxiliares.mm_ponto(29), F_Auxiliares.mm_ponto(260), f'{material}')       
    cnv.drawString(F_Auxiliares.mm_ponto(138), F_Auxiliares.mm_ponto(260), f'{furo}')       
    cnv.drawString(F_Auxiliares.mm_ponto(28), F_Auxiliares.mm_ponto(251), f'{operador}')      
    cnv.drawString(F_Auxiliares.mm_ponto(121), F_Auxiliares.mm_ponto(251), f'{obra}')        
    cnv.drawString(F_Auxiliares.mm_ponto(23), F_Auxiliares.mm_ponto(243), f'{trecho}')       
    cnv.drawString(F_Auxiliares.mm_ponto(135), F_Auxiliares.mm_ponto(243), f'{subtrecho}')        
    cnv.drawString(F_Auxiliares.mm_ponto(83), F_Auxiliares.mm_ponto(230), f'{massa_amostra_cilindro}')        
    cnv.drawString(F_Auxiliares.mm_ponto(83), F_Auxiliares.mm_ponto(224), f'{massa_cilindro}')      
    cnv.drawString(F_Auxiliares.mm_ponto(83), F_Auxiliares.mm_ponto(217), f'{massa_esp_ap_seca}')        
    cnv.drawString(F_Auxiliares.mm_ponto(83), F_Auxiliares.mm_ponto(210), f'{volume}')        
    cnv.drawString(F_Auxiliares.mm_ponto(83), F_Auxiliares.mm_ponto(204), f'{peso_esp_umido}')       
    cnv.drawString(F_Auxiliares.mm_ponto(83), F_Auxiliares.mm_ponto(197), f'{teor_umidade_media}')   
    cnv.drawString(F_Auxiliares.mm_ponto(83), F_Auxiliares.mm_ponto(190), f'{massa_amosta}')     
    cnv.drawString(F_Auxiliares.mm_ponto(41), F_Auxiliares.mm_ponto(163), f'{leitura_exp0}')     
    cnv.drawString(F_Auxiliares.mm_ponto(41), F_Auxiliares.mm_ponto(156), f'{leitura_exp1}')    
    cnv.drawString(F_Auxiliares.mm_ponto(41), F_Auxiliares.mm_ponto(149), f'{leitura_exp2}')  
    cnv.drawString(F_Auxiliares.mm_ponto(41), F_Auxiliares.mm_ponto(142), f'{leitura_exp3}')  
    cnv.drawString(F_Auxiliares.mm_ponto(41), F_Auxiliares.mm_ponto(136), f'{leitura_exp4}')  
    cnv.drawString(F_Auxiliares.mm_ponto(42), F_Auxiliares.mm_ponto(127), f'{altura_inicial}') 
    cnv.drawString(F_Auxiliares.mm_ponto(84), F_Auxiliares.mm_ponto(127), f'{exp_umidade_otima}') 
    cnv.drawString(F_Auxiliares.mm_ponto(71), F_Auxiliares.mm_ponto(156), f'{float(altura_inicial) - float(leitura_exp1)}')   
    cnv.drawString(F_Auxiliares.mm_ponto(71), F_Auxiliares.mm_ponto(149), f'{float(altura_inicial) - float(leitura_exp2)}') 
    cnv.drawString(F_Auxiliares.mm_ponto(71), F_Auxiliares.mm_ponto(142), f'{float(altura_inicial) - float(leitura_exp3)}')
    cnv.drawString(F_Auxiliares.mm_ponto(71), F_Auxiliares.mm_ponto(136), f'{float(altura_inicial) - float(leitura_exp4)}')
    #Esse loop mostra apenas os valores de força maiores que 0 para exibir no relatorio
    for cont in eixo_y_forca: 
        if cont > 0:
            forca_relatorio.append(cont)
    cnv.drawString(F_Auxiliares.mm_ponto(139), F_Auxiliares.mm_ponto(218), f'{str(forca_relatorio[0])}')
    cnv.drawString(F_Auxiliares.mm_ponto(139), F_Auxiliares.mm_ponto(211), f'{str(forca_relatorio[1])}')
    cnv.drawString(F_Auxiliares.mm_ponto(139), F_Auxiliares.mm_ponto(204), f'{str(forca_relatorio[2])}')
    cnv.drawString(F_Auxiliares.mm_ponto(139), F_Auxiliares.mm_ponto(198), f'{str(forca_relatorio[3])}')  
    cnv.drawString(F_Auxiliares.mm_ponto(139), F_Auxiliares.mm_ponto(191), f'{str(forca_relatorio[4])}')  
    cnv.drawString(F_Auxiliares.mm_ponto(139), F_Auxiliares.mm_ponto(184), f'{str(forca_relatorio[5])}')  
    cnv.drawString(F_Auxiliares.mm_ponto(139), F_Auxiliares.mm_ponto(177), f'{str(forca_relatorio[6])}')  
    cnv.drawString(F_Auxiliares.mm_ponto(139), F_Auxiliares.mm_ponto(171), f'{str(forca_relatorio[7])}')
    cnv.drawString(F_Auxiliares.mm_ponto(139), F_Auxiliares.mm_ponto(164), f'{str(forca_relatorio[8])}')
    cnv.drawString(F_Auxiliares.mm_ponto(139), F_Auxiliares.mm_ponto(157), f'{str(forca_relatorio[9])}')
    cnv.drawString(F_Auxiliares.mm_ponto(139), F_Auxiliares.mm_ponto(150), f'{str(forca_relatorio[10])}')
    cnv.drawString(F_Auxiliares.mm_ponto(139), F_Auxiliares.mm_ponto(144), f'{str(forca_relatorio[11])}')
    cnv.drawString(F_Auxiliares.mm_ponto(139), F_Auxiliares.mm_ponto(137), f'{str(forca_relatorio[12])}')
    cnv.drawString(F_Auxiliares.mm_ponto(167), F_Auxiliares.mm_ponto(198), f'{str(forca_relatorio[4])}')
    cnv.drawString(F_Auxiliares.mm_ponto(167), F_Auxiliares.mm_ponto(178), f'{str(forca_relatorio[7])}') 
    cnv.drawString(F_Auxiliares.mm_ponto(188), F_Auxiliares.mm_ponto(198), f'{round((((float(forca_relatorio[4]))/70.31)*100),3)}')
    cnv.drawString(F_Auxiliares.mm_ponto(188), F_Auxiliares.mm_ponto(178), f'{round((((float(forca_relatorio[7]))/105.46)*100),3)}')
    cnv.save()
    messagebox.showwarning("Fim do ensaio",
                           "O relatorio foi criado com sucesso e se encontra na pasta de destino")
    tela5.destroy()
 
"""=============================================================================================================================================================
                                             CRIAÇÃO DE WIDGETS,LAYOUT DA TELA E CONECÇÃO COM O BD
============================================================================================================================================================="""
#CRIA JANELA DO TKINTER
tela5 = Tk()
tela5.iconbitmap(default=r"Funcionalidades\tela1.ico"); tela5.title("Ensaio CBR"); tela5.geometry('1366x705+-11+1')
img_fundo = PhotoImage(file=r"Funcionalidades\tela_ensaio_cbr.png"); label_fundo = Label(tela5, image=img_fundo); label_fundo.place(x=0, y=0)

messagem = F_Auxiliares.Messege1(tela5)                           #CONECÇÃO COM AS LABELS DE EXIBIÇÃO DE DADOS DO ENSAIO

#CRIA OS BOTOES DA TELA
B_Buscar = Button(tela5, text="Buscar", bd=4, bg="orange", font=("Arial", 18), command = botao_buscar)
B_Buscar.place(width=122, height=34, x=91, y=344)
B_Conectar = Button(tela5, text="Conectar", bd=4, bg="orange", font=("Arial", 18), command = botao_conectar)
B_Conectar.place(width=122, height=34, x=91, y=390)
B_Iniciar = Button(tela5, text="INICIAR ENSAIO", bg="dark green", bd=4, font=("Arial", 18), command = iniciar_ensaio)
B_Iniciar.place(width=211, height=53, x=45, y=458)
B_Parar = Button(tela5, text="PARAR ENSAIO", bg="dark red", bd=4, font=("Arial", 18), command = parar_ensaio)
B_Parar.place(width=211, height=53, x=45, y=532)
B_Voltar = Button(tela5, text="VOLTAR", bg="gold", bd=4, font=("Arial", 18), command = voltar_pagina)
B_Voltar.place(width=211, height=53, x=45, y=606)

#CRIA LISTA CLICAVEL PARA O USUARIO ESCOLHER A COM PORT
lista_ComPorts = Listbox(tela5, height=1, width=7, bd=10, font="Arial 10", bg="black",
                    fg="green", highlightcolor="black", highlightthickness=0, highlightbackground="black")
lista_ComPorts.place(width=122, height=99, x=90, y=233); lista_ComPorts.insert(END, "------")
lista_ComPorts.bind('<Double-Button>', lambda e: messagem.port("orange", lista_ComPorts.get(ANCHOR)))

#VARREDURA PARA BUSCAR PORTAS ENQUANTO A VARIAVEL FOR 'TRUE'
Buscar_ports = threading.Thread(target=buscar_ComPorts); Buscar_ports.daemon = True; Buscar_ports.start()
#VARREDURA PARA VER SE A DADOS A RECEBER/CONECÇÃO COM A PORTA SERIAL
recebendo_serial = threading.Thread(target=recebe_dados_serial); recebendo_serial.daemon = True

tela5.mainloop()
"""============================================================================================================================================================ 
                                                               FIM DO PROGRAMA
============================================================================================================================================================="""