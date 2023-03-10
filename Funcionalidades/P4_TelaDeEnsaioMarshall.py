"""=====================================================================================================================
                                          IMPORTAÇÃO DE MODULOS
====================================================================================================================="""
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
from subprocess import run                                            #biblioteca para mudar de pagina usando diretorios

"""=====================================================================================================================
                                          VARIAVEIS DO PROGRAMA
====================================================================================================================="""
tela4 = Tk()
SearchingPorts = True
GetForcaFlag = False
Grafico_Forca = float()
Grafico_Deslocamento = float()
cont = 0
x = []
y = []
x1 = []
y2 = []
max = 0                                                                                 #valor de pico inicial da prensa
"""=====================================================================================================================
                                                  FUNÇÕES
====================================================================================================================="""
def send_byte(byte):
    if F_Auxiliares.is_open():
        F_Auxiliares.write_byte(byte)
    else:
        messagem.botton("Por favor, abra a porta serial!", "yellow")

def send_Funcionamento():
    if F_Auxiliares.is_open():
        DadosTx = int(F_Auxiliares.Funcionamento_Modo)
        for idx in range(0, len(DadosTx)):
            F_Auxiliares.write_byte(DadosTx[idx])
        else:
            messagem.botton("Por favor, abra a porta serial!", "yellow")

def f_searching_ports():
    global SearchingPorts
    while True:
        sleep(0.3)
        if SearchingPorts:
            messagem.botton('AGUARDE, procurando COM PORT...', "red")
            ports = serial.tools.list_ports.comports(include_links=False)
            port_list.delete('0', 'end')
            idx = 0
            for port in sorted(ports):
                port_list.insert(idx, port.device)
                idx = idx + 1
                port_list["height"] = idx
                SearchingPorts = False
                messagem.botton('BUSCA FINALIZADA, escolha a COM PORT...', "yellow")

def f_receiving_serial():
    global Grafico_Forca
    global Grafico_Deslocamento
    global x
    global y
    while True:
        sleep(0.3)
        if F_Auxiliares.is_open():
            F_Auxiliares.reset_input_buffer()
            try:
                serial_data = F_Auxiliares.read_line()
                serial_data = str(serial_data)
                serial_data = serial_data.replace("b'", "")
                serial_data = serial_data.replace("r", "")
                serial_data = serial_data.replace("\\", "")
                serial_data = serial_data.replace("n'", "")
                serial_data = serial_data.replace(".00", "")
                serial_data = float(serial_data) / 100
                Grafico_Forca = float(serial_data)
                x.append(Grafico_Forca)
                messagem.forca(str(serial_data))
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

def LigaMar():
    global ax
    global anima
    global Grafico_Deslocamento
    if Grafico_Deslocamento <= 0.1:
        if F_Auxiliares.is_open():
            send_byte(251)                                #Liga a prensa em estado marshall(envia 251 pela porta serial)
            figura = plt.Figure(figsize=(8, 4), dpi=60)
            ax = figura.add_subplot(111)
            canva = FigureCanvasTkAgg(figura, tela4)
            canva.get_tk_widget().place(width=1068, height=482, x=250, y=130)
            anima = animation.FuncAnimation(figura, animar, interval=1000, frames=10)
        else:
            messagebox.showwarning("ERRO!!!!!", "O computador não esta conectado com a prensa")
            messagem.botton('ATENÇÃO: Conecte o seu computador com a prensa...', "red")
    else:
        messagebox.showwarning("ERRO!!!!!", "Para iniciar o ensaio o deslocamento deve ser igual a 0, "
                                            "ajuste o sensor de deslocamento")
        messagem.botton('ATENÇÃO: Ajuste o sensor de deslocamento para a posição 0', "red")

def ParaMar():
    send_byte(254)                                         #Desliga a prensa imediatamente (envia 254 pela porta serial)
    messagebox.showwarning("ENSAIO ENCERRADO",                                  #CRIA UMA CAIXA COM UMA MENSAGEM DE ERRO
                           "O ensaio foi encerrado manualmente")
    tela4.destroy()                                                                                  #Apaga a tela atual
    run(r"Funcionalidades\P1_TelaPrincipal.exe", shell=True)

def Voltar():
    global cont
    if cont == 0:
        tela4.destroy()
        run(r"Funcionalidades\P2_FormularioMarshall.exe", shell=True)
    else:
        messagem.botton('O ensaio esta em andamento, aperte o botão "PARAR" encerrar o ensaio', "yellow")

def Relatorio():
    global x1
    global y2
    conexao = pymysql.connect(host='localhost', user='root', passwd='', database='db_prensa_software')
    cursor = conexao.cursor()
    cursor.execute("TRUNCATE TABLE teste;")
    for r in range(0, len(x1)):
        sql = f'INSERT INTO teste(forca_t,deslocamento_t) VALUES (%s,%s)'
        sql_data = [x1[r], y2[r]]
        cursor.execute(sql, sql_data)
        conexao.commit()
    cursor.close()
    messagebox.showwarning("RELATORIO GERADO COM SUCESSO",                     # CRIA UMA CAIXA COM UMA MENSAGEM DE ERRO
                           "O relatorio foi criado e se encontra na pasta de destino")
    run(r"Funcionalidades\P6_Relatorio.exe", shell=True)
    tela4.destroy()                                                                                  #Apaga a tela atual
    run(r"Funcionalidades\P1_TelaPrincipal.exe", shell=True)

def Buscar():
    global SearchingPorts
    SearchingPorts = True

def Conectar():
    global GetForcaFlag
    if F_Auxiliares.Port == 'COMx':
        messagem.botton('BUSCA FINALIZADA, escolha a COM PORT...', "yellow")
        return None
    if not F_Auxiliares.is_open():
        F_Auxiliares.open()
        if F_Auxiliares.is_open():
            messagem.botton("CONECTADO!", "green")
            sleep(2.5)
            GetForcaFlag = True
            if not receiving_serial.is_alive():
                receiving_serial.start()
    else:
        F_Auxiliares.comport.close()
        messagem.botton("DESCONECTADO!", "red")

def animar(i):
    global x, y, cont, x1, y2, max, tam
    if cont == 0:
        x.clear()
        y.clear()
        x = [0]
        y = [0]
        cont = 1
    if len(x) == len(y):
        ax.clear()
        ax.plot(y, x, ls='-', lw=2, marker='o')
        ax.axis([0, 25.5, 0, 5500])
        ax.grid(True)
        ax.set_title('GRAFICO: FORÇA(Kg/f) x DESLOCAMENTO(mm)', fontsize=28)
        ax.set_xlabel('DESLOCAMENTO (mm)', fontsize=22)
        ax.set_ylabel('FORÇA (Kg/F)', fontsize=22)
        x1 = x
        y2 = y
    max = None
    for num in x1:
        if (max is None or num > max):                                   #pega o valor maximo da lista e manda pra "max"
            max = num
    tam = len(x1)                                                             #pega o tamanho do vetor e manda pra "tam"
    pararAutomatico()

def pararAutomatico():
    global max
    global tam
    global x1
    if max > (x1[tam-1]+1500):
        send_byte(253)
        Relatorio()
"""=====================================================================================================================
                     CRIAÇÃO DE WIDGETS, LAYOUT DA TELA, CONEXÃO COM O BD E COMUNICAÇÃO SERIAL
====================================================================================================================="""
img_fundo = PhotoImage(file=r"Funcionalidades\Tela_Ensaio_Marshall.png")
label_fundo = Label(tela4, image=img_fundo)
label_fundo.place(x=0, y=0)

B_LigaMar = Button(tela4, text="INICIAR ENSAIO", bg="dark green", bd=4, font=("Arial", 18), command=LigaMar)    #botoes
B_LigaMar.place(x=19, y=507)
B_ParaMar = Button(tela4, text="PARAR ENSAIO", bg="red", font=("Arial", 18), bd=5, command=ParaMar)
B_ParaMar.place(x=19, y=569)
B_Voltar = Button(tela4, text="      VOLTAR      ", bd=4, bg="yellow", font=("Arial", 18), command=Voltar)
B_Voltar.place(x=19, y=631)
B_Buscar = Button(tela4, text="Buscar", bd=4, bg="blue", font=("Arial", 18), command=Buscar)
B_Buscar.place(width=108, height=38, x=71, y=397)
B_Conectar = Button(tela4, text="Conectar", bd=4, bg="blue", font=("Arial", 16), command=Conectar)
B_Conectar.place(width=108, height=39, x=71, y=441)

port_list = Listbox(tela4, height=1, width=7, bd=10, font="Arial 10", bg="black",             #Cria widget do tipo lista
                    fg="#008000", highlightcolor="black", highlightthickness=0, highlightbackground="black")
port_list.place(width=104, height=132, x=71, y=253)
port_list.insert(END, "----")                                     #Define oque vai aparecer quando a lista estiver vazia
port_list.bind('<Double-Button>', lambda e: messagem.port("green", port_list.get(ANCHOR)))

searching_ports = threading.Thread(target=f_searching_ports)                             #Busca por dispositivos seriais
searching_ports.daemon = True
searching_ports.start()

receiving_serial = threading.Thread(target=f_receiving_serial)                    #Verifica se a dados seriais à receber
receiving_serial.daemon = True

messagem = F_Auxiliares.Messege1(tela4)

tela4.title("Ensaio Marshall")
tela4.iconbitmap(default=r"Funcionalidades\tela1.ico")
tela4.geometry('1366x705+-11+1')

mainloop()
"""=====================================================================================================================            
                                               FIM DO PROGRAMA
====================================================================================================================="""