"""==================================================================================================================================================
                                                     IMPORTAÇÃO DE MODULOS
=================================================================================================================================================="""
from tkinter import *
from subprocess import run                                                           
"""==================================================================================================================================================
                                                             FUNÇÕES
=================================================================================================================================================="""
#As funcoes fecham a janela atual e abre a janela de formulario do teste que foi escolhido
def MAR():
    tela1.destroy(); run(r"Funcionalidades\P2_FormularioMarshall.exe", shell=True)

def CBR():
    tela1.destroy(); run(r"Funcionalidades\P3_FormularioCbr.exe", shell=True)
"""==================================================================================================================================================
                                                    CRIAÇÃO DA TELA E DOS BOTÕES
=================================================================================================================================================="""
tela1 = Tk()                                                               
FundoTela1 = PhotoImage(file=r"Funcionalidades\tela1_app1.png"); LabelFundo=Label(tela1, image = FundoTela1); LabelFundo.place(x=0,y=0) 
tela1.title("Prensa CBR e MARSHALL"); tela1.iconbitmap(default=r"Funcionalidades\tela1.ico"); tela1.geometry('1366x705+-11+1')
#tela1.wm_resizable(width=FALSE,height=FALSE)          #define que não é possivel alterar ou maximizar o tamanho da tela

B_CBR=Button(tela1,text="CBR",bg="green",activebackground="yellow",font=("Arial",35),width="9",height='0',command=CBR); B_CBR.place(x=260,y=310)
B_MAR=Button(tela1,text="MARSHALL",bg="green",activebackground="yellow",font=("Arial",34),width="10",height='1',command=MAR);B_MAR.place(x=800,y=310)

tela1.mainloop()
"""==================================================================================================================================================
                                                         FIM DO PROGRAMA
=================================================================================================================================================="""
