"""=====================================================================================================================
                                          IMPORTAÇÃO DE MODULOS
====================================================================================================================="""
import tkinter
from tkinter import *
from subprocess import run                                                               #biblioteca para passar paginas
"""=====================================================================================================================
                                                  FUNÇÕES
====================================================================================================================="""
def MAR():
    tela1.destroy()
    run("P2_FormularioMarshall.py", shell=True)

def CBR():
    pass


"""=====================================================================================================================
                                          CRIAÇÃO DE WIDGETS E LAYOUT DA TELA
====================================================================================================================="""
tela1 = Tk()                                                                #tela de inicio é uma instancia da classe tk

FundoTela1 = PhotoImage(file='tela1_app1.png')                                 #guarda a imagem de fundo em uma variavel
LabelFundo = Label(tela1, image = FundoTela1)     #cria uma label(imagem ou texto) para a imagem ficar no fundo da tela1
LabelFundo.place(x=0,y=0)                                        #coordenadas cartesianas para o inicio do fundo de tela

B_CBR = Button(tela1,text="CBR",bg="green",activebackground="yellow",                                  #Cria o botão cbr
               font=("Arial",35),width="9",height='0',command=CBR)
B_CBR.place(x=260,y=310)                                                                      #Define a posição do botão
B_MAR = Button(tela1,text="MARSHALL",bg="green",activebackground="yellow",
               font=("Arial",34),width="10",height='1',command=MAR)
B_MAR.place(x=800,y=310)

tela1.title("Prensa CBR e MARSHALL")                                           #define o titulo da janela que foi criada
tela1.iconbitmap(default="tela1.ico")                               #define o icone do aplicativo (formato ico 16x16 px)
tela1.geometry('1366x705+-11+1')                                               #define o tamanho que a tela1 vai começar
#tela1.wm_resizable(width=FALSE,height=FALSE)          #define que não é possivel alterar ou maximizar o tamanho da tela
#tela1.bind('<Button-1>', mouseBtnEsquerdo)          #cria uma conecção entre o envento de clicar o botão e a sua função
"""
frame1 = Frame(tela1)
frame1.place(width=1366,height=705)

frame2 = Frame(tela1)
frame2.place(width=1366,height=705)
"""
tela1.mainloop()
"""=====================================================================================================================            
                                               FIM DO PROGRAMA
====================================================================================================================="""
