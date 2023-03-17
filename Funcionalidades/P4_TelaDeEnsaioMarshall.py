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
buscar_ComPorts = False                                              #variavel que controla a busca por comunicação serial
eixo_y_forca = []; eixo_x_deslocamento = []                          #listas que guardam os valores de força e deslocamento
serial_forca = 0.0 ; serial_deslocamento = 0.0                       #valor de força e deslocamento em tempo real
prensa_ligada = False                                                #variavel que diz se o ensaio esta em andamento
porcentagem_rompimento = 0.35                                         #porcentagem que a força pode cair no rompimento para finalizar o ensaio
data_atual = datetime.now()
data_str = data_atual.strftime('Relatorio_Marshall_%d-%m-%Y_%H-%M')  #transforma a data atual no nome do arquivo
pastaApp = os.path.dirname(f'Relatorios\{data_str}.pdf')             #caminho da pasta do pdf
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
    global eixo_y_forca, eixo_x_deslocamento, serial_forca, serial_deslocamento
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
def iniciar_ensaio():       
    global serial_deslocamento, ax, animar, prensa_ligada
    if float(serial_deslocamento) < 0.1 or b == True:          
        if F_Auxiliares.comport.is_open:
            if prensa_ligada == False:
                F_Auxiliares.comport.write((F_Auxiliares.Liga_Marshall, ))         #envia o byte que é o comando de ligar em modo CBR (251) na serial
                prensa_ligada = True
            #Cria uma figura na tela que é o grafico de força x deslocamento
            figura = plt.Figure(figsize=(8, 4), dpi=60,facecolor='orange')
            ax = figura.add_subplot(facecolor=(.0, .50, .0))
            canva = FigureCanvasTkAgg(figura, tela4)
            canva.get_tk_widget().place(width=1052, height=410, x=290, y=173)
            animar = animation.FuncAnimation(figura, plotar, interval=1000, frames=10)        #gera a animação e chama a função que a "comandara"
            messagem.botton('Ensaio em andamento!', "green")
        else:
            messagebox.showwarning("ERRO!!!!!", "O computador não esta conectado com a prensa")
            messagem.botton('ATENÇÃO: Conecte o seu computador com a prensa...', "red")
    else:
        messagebox.showwarning("ERRO!!!!!", "Para iniciar o ensaio o deslocamento deve ser igual a 0, ajuste o sensor de deslocamento")
        messagem.botton('ATENÇÃO: Ajuste o sensor de deslocamento para a posição 0', "red")
  
#Grafico em tempo real até que deslocamento maximo, quando atingido retorna a prensa para a posição inicial e chama a função de criar o relatorio
def plotar(i):
    global eixo_y_forca, eixo_x_deslocamento, prensa_ligada, serial_forca, porcentagem_rompimento, forca_max_atual
    forca_max_atual = None
    for num in eixo_y_forca:
        if (forca_max_atual is None or num > forca_max_atual):         
            forca_max_atual = num  
    if (serial_forca + (forca_max_atual * porcentagem_rompimento)) >= forca_max_atual:           
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
        gerar_relatorio_marshall()                                                             #função de criar o relatorio
 
#Para a prensa imediatamente se o ensaio for interrompido, informa o usuario
def parar_ensaio():
    global prensa_ligada
    if prensa_ligada == True:
        F_Auxiliares.comport.write((F_Auxiliares.Desliga_Prensa,))          #Escreve na porta serial o byte que desliga a prensa (254)
        messagem.botton('PARADA MANUAL!!!. O ensaio foi interrempido durante sua execução', "red")
        messagebox.showwarning("PARADA MANUAL!!!",
                               "Amostra comprometida os dados do formulario seram apagados e você sera redirecionado para a tela inicial")
        tela4.destroy()
        run(r"Funcionalidades\P1_TelaPrincipal.exe", shell=True)
    elif prensa_ligada == False:
        messagem.botton('Conecte-se a prensa para iniciar o ensaio ou volte para a pagina anterior', "yellow")
        messagebox.showwarning("ERRO!!!!!!!!!!","O ensaio ainda não foi iniciado")

#Volta para a pagina inicial caso o ensaio não tenha ainda não tenha sido iniciado, informa o usuario
def voltar_pagina():
    global prensa_ligada
    if prensa_ligada == True:
        messagem.botton('Ensaio em andamento, se deseja parar o ensaio pressione o botão "PARAR"', "red")
    else: 
        tela4.destroy()       
        run(r"Funcionalidades\P2_FormularioMarshall.exe", shell=True)

#Cria o pdf do relatorio e fecha o aplicativo
def gerar_relatorio_marshall():
    global pastaApp, data_str, eixo_y_forca, eixo_x_deslocamento, forca_max_atual
    F_Auxiliares.comport.close()                                                                                #Fecha a comunicação serial
    #Connecta com o DB, pega os dados e manipula-os para usalos no relatorio
    conexao = pymysql.connect ( host='localhost', user='root', passwd='',database='db_prensa_software')
    cursor = conexao.cursor()
    cursor.execute(f"SELECT registro FROM ensaio_marshall;") 
    registro = str(cursor.fetchall()); registro = registro.replace("(('", ""); registro = registro.replace("',),)", "")
    cursor.execute(f"SELECT dia FROM ensaio_marshall;") 
    dia = str(cursor.fetchall()); dia = dia.replace("(('", ""); dia = dia.replace("',),)", "")
    cursor.execute(f"SELECT id_cp FROM ensaio_marshall;") 
    id_cp= str(cursor.fetchall()); id_cp = id_cp.replace("(('", ""); id_cp = id_cp.replace("',),)", "")
    cursor.execute(f"SELECT material FROM ensaio_marshall;") 
    material = str(cursor.fetchall()); material = material.replace("(('", ""); material = material.replace("',),)", "")
    cursor.execute(f"SELECT obra FROM ensaio_marshall;") 
    obra = str(cursor.fetchall()); obra = obra.replace("(('", ""); obra = obra.replace("',),)", "")
    cursor.execute(f"SELECT operador FROM ensaio_marshall;") 
    operador = str(cursor.fetchall()); operador = operador.replace("(('", ""); operador = operador.replace("',),)", "")
    cursor.execute(f"SELECT trecho FROM ensaio_marshall;") 
    trecho = str(cursor.fetchall()); trecho = trecho.replace("(('", ""); trecho = trecho.replace("',),)", "")
    cursor.execute(f"SELECT subtrecho FROM ensaio_marshall;") 
    subtrecho = str(cursor.fetchall()); subtrecho = subtrecho.replace("(('", ""); subtrecho = subtrecho.replace("',),)", "")
    cursor.execute(f"SELECT peso_ar FROM ensaio_marshall;") 
    peso_ar = str(cursor.fetchall()); peso_ar = peso_ar.replace("((", ""); peso_ar = peso_ar.replace(",),)", "")
    cursor.execute(f"SELECT peso_imerso FROM ensaio_marshall;") 
    peso_imerso = str(cursor.fetchall()); peso_imerso = peso_imerso.replace("((", ""); peso_imerso = peso_imerso.replace(",),)", "")
    cursor.execute(f"SELECT volume FROM ensaio_marshall;") 
    volume = str(cursor.fetchall()); volume = volume.replace("((", ""); volume = volume.replace(",),)", "")
    cursor.execute(f"SELECT densi_aparente FROM ensaio_marshall;") 
    densi_aparente = str(cursor.fetchall()); densi_aparente = densi_aparente.replace("((", ""); densi_aparente = densi_aparente.replace(",),)", "")
    cursor.execute(f"SELECT densi_teorica FROM ensaio_marshall;") 
    densi_teorica = str(cursor.fetchall()); densi_teorica = densi_teorica.replace("((", ""); densi_teorica = densi_teorica.replace(",),)", "")
    cursor.execute(f"SELECT temperatura FROM ensaio_marshall;") 
    temperatura = str(cursor.fetchall()); temperatura = temperatura.replace("((", ""); temperatura = temperatura.replace(",),)", "")
    cursor.execute(f"SELECT vazios FROM ensaio_marshall;") 
    vazios = str(cursor.fetchall()); vazios = vazios.replace("((", ""); vazios = vazios.replace(",),)", "")
    cursor.execute(f"SELECT v_c_b FROM ensaio_marshall;") 
    v_c_b = str(cursor.fetchall()); v_c_b = v_c_b.replace("((", ""); v_c_b = v_c_b.replace(",),)", "")
    cursor.execute(f"SELECT v_a_m FROM ensaio_marshall;") 
    v_a_m = str(cursor.fetchall()); v_a_m = v_a_m.replace("((", ""); v_a_m = v_a_m.replace(",),)", "")
    cursor.execute(f"SELECT r_v_b FROM ensaio_marshall;") 
    r_v_b = str(cursor.fetchall()); r_v_b = r_v_b.replace("((", ""); r_v_b = r_v_b.replace(",),)", "")
    cursor.execute(f"SELECT amostra_antes FROM ensaio_marshall;") 
    amostra_antes = str(cursor.fetchall()); amostra_antes = amostra_antes.replace("((", ""); amostra_antes = amostra_antes.replace(",),)", "")
    cursor.execute(f"SELECT amostra_depois FROM ensaio_marshall;") 
    amostra_depois = str(cursor.fetchall()); amostra_depois = amostra_depois.replace("((", ""); amostra_depois = amostra_depois.replace(",),)", "")
    cursor.execute(f"SELECT peso_betume FROM ensaio_marshall;") 
    peso_betume = str(cursor.fetchall()); peso_betume = peso_betume.replace("((", ""); peso_betume = peso_betume.replace(",),)", "")
    cursor.execute(f"SELECT teor_betume FROM ensaio_marshall;") 
    teor_betume = str(cursor.fetchall()); teor_betume = teor_betume.replace("((", ""); teor_betume = teor_betume.replace(",),)", "")
    cursor.execute(f"SELECT leit_deflet FROM ensaio_marshall;") 
    leit_deflet = str(cursor.fetchall()); leit_deflet = leit_deflet.replace("((", ""); leit_deflet = leit_deflet.replace(",),)", "")
    cursor.execute(f"SELECT area FROM ensaio_marshall;") 
    area = str(cursor.fetchall()); area = area.replace("((", ""); area = area.replace(",),)", "")
    cursor.execute(f"SELECT estab_corrigida FROM ensaio_marshall;") 
    estab_corrigida = str(cursor.fetchall()); estab_corrigida = estab_corrigida.replace("((","");estab_corrigida = estab_corrigida.replace(",),)","")
    #Cria o um grafico com os valores de força e deslocamento e salva em uma imagem
    plt.plot(eixo_x_deslocamento, eixo_y_forca, ls='-', lw=2, marker='o')
    plt.axis('tight')
    plt.grid(True)
    plt.ylabel('FORÇA (Kg/F)')
    plt.xlabel('DESLOCAMENTO (mm)')
    plt.title('GRAFICO: FORÇA(Kg/f) x DESLOCAMENTO(mm) ')
    plt.savefig(r"Funcionalidades\grafico_relatorio_marshall.png", dpi=150) 
    #Escreve dados e imagens no pdf
    cnv = canvas.Canvas(pastaApp + f'\{data_str}.pdf', pagesize=A4)            #pasta,nome e tamanho do pdf 
    cnv.drawImage(r"Funcionalidades\relatorio_marshall_individual.png",                #coloca a imagem no ponto especolhido e no tamanho escolhido
                  F_Auxiliares.mm_ponto(0), F_Auxiliares.mm_ponto(0), width = F_Auxiliares.mm_ponto(210), height = F_Auxiliares.mm_ponto(297))
    cnv.drawImage(r"Funcionalidades\grafico_relatorio_marshall.png",                   #coloca a imagem no ponto especolhido e no tamanho escolhido
                  F_Auxiliares.mm_ponto(0), F_Auxiliares.mm_ponto(0), width = F_Auxiliares.mm_ponto(230), height = F_Auxiliares.mm_ponto(126))
    cnv.drawString(F_Auxiliares.mm_ponto(26), F_Auxiliares.mm_ponto(278), f'{registro}')                 #escreve no pdf no ponto escolhido   
    cnv.drawString(F_Auxiliares.mm_ponto(70), F_Auxiliares.mm_ponto(278), f'{dia}')   
    cnv.drawString(F_Auxiliares.mm_ponto(140), F_Auxiliares.mm_ponto(278), f'{id_cp}') 
    cnv.drawString(F_Auxiliares.mm_ponto(28), F_Auxiliares.mm_ponto(270), f'{material}') 
    cnv.drawString(F_Auxiliares.mm_ponto(120), F_Auxiliares.mm_ponto(270), f'{obra}') 
    cnv.drawString(F_Auxiliares.mm_ponto(21), F_Auxiliares.mm_ponto(260), f'{trecho}') 
    cnv.drawString(F_Auxiliares.mm_ponto(134), F_Auxiliares.mm_ponto(260), f'{subtrecho}')
    cnv.drawString(F_Auxiliares.mm_ponto(26), F_Auxiliares.mm_ponto(251), f'{operador}')
    cnv.drawString(F_Auxiliares.mm_ponto(46), F_Auxiliares.mm_ponto(231), f'{peso_ar}')
    cnv.drawString(F_Auxiliares.mm_ponto(46), F_Auxiliares.mm_ponto(222), f'{peso_imerso}')    
    cnv.drawString(F_Auxiliares.mm_ponto(46), F_Auxiliares.mm_ponto(213), f'{volume}')  
    cnv.drawString(F_Auxiliares.mm_ponto(46), F_Auxiliares.mm_ponto(204), f'{densi_aparente}')  
    cnv.drawString(F_Auxiliares.mm_ponto(46), F_Auxiliares.mm_ponto(195), f'{densi_teorica}')  
    cnv.drawString(F_Auxiliares.mm_ponto(46), F_Auxiliares.mm_ponto(186), f'{vazios}') 
    cnv.drawString(F_Auxiliares.mm_ponto(46), F_Auxiliares.mm_ponto(177), f'{v_c_b}')
    cnv.drawString(F_Auxiliares.mm_ponto(46), F_Auxiliares.mm_ponto(168), f'{v_a_m}')
    cnv.drawString(F_Auxiliares.mm_ponto(46), F_Auxiliares.mm_ponto(159), f'{r_v_b}')
    cnv.drawString(F_Auxiliares.mm_ponto(46), F_Auxiliares.mm_ponto(150), f'{area}')
    cnv.drawString(F_Auxiliares.mm_ponto(46), F_Auxiliares.mm_ponto(141), f'{estab_corrigida}')
    cnv.drawString(F_Auxiliares.mm_ponto(46), F_Auxiliares.mm_ponto(132), f'{leit_deflet}')
    cnv.drawString(F_Auxiliares.mm_ponto(145), F_Auxiliares.mm_ponto(231), f'{amostra_antes}')
    cnv.drawString(F_Auxiliares.mm_ponto(145), F_Auxiliares.mm_ponto(221), f'{amostra_depois}')
    cnv.drawString(F_Auxiliares.mm_ponto(145), F_Auxiliares.mm_ponto(212), f'{peso_betume}')
    cnv.drawString(F_Auxiliares.mm_ponto(145), F_Auxiliares.mm_ponto(202), f'{teor_betume}')
    cnv.drawString(F_Auxiliares.mm_ponto(150), F_Auxiliares.mm_ponto(152), f'{temperatura}')
    cnv.drawString(F_Auxiliares.mm_ponto(150), F_Auxiliares.mm_ponto(142), f'{forca_max_atual}')
    cnv.drawString(F_Auxiliares.mm_ponto(150), F_Auxiliares.mm_ponto(133),f'{ (float(forca_max_atual) * 2) / float(area) }')
    cnv.save()
    messagebox.showwarning("Fim do ensaio", "O relatorio foi criado com sucesso e se encontra na pasta de destino")
    tela4.destroy()
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