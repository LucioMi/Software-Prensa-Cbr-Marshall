"""=====================================================================================================================
                                          IMPORTAÇÃO DE MODULOS
====================================================================================================================="""
from tkinter import *        #importa o modulo
from subprocess import run
"""=====================================================================================================================
                                                  FUNÇÕES
====================================================================================================================="""
def Salvar():
    tela3.destroy()
    run(r"Funcionalidades\P4_TelaDeEnsaioMarshall.exe", shell=True)       #esta indo pra tela marshall a titulo de teste

def Voltar():
    tela3.destroy()
    run(r"Funcionalidades\P1_TelaPrincipal.exe", shell=True)
"""=====================================================================================================================
                            CRIAÇÃO DE WIDGETS,LAYOUT DA TELA E CONECÇÃO COM O BD
====================================================================================================================="""
tela3 = Tk()                #cria uma 'variavel' tipo tk
tela3.iconbitmap(default=r"Funcionalidades\tela1.ico")  #define o icone do aplicativo (formato ico 16x16 px)
tela3.title("Formulario Ensaio CBR")    #cria o titulo da janela
tela3.geometry('1366x705+-11+1')           #define o tamanho da janela

B_Salvar = Button(tela3,text="SALVAR",bg="green", command=Salvar, font=("Arial",20))
B_Salvar.grid(row=8,column=0)

B_Voltar = Button(tela3,text="VOLTAR",bg="red",command=Voltar, font=("Arial",20))
B_Voltar.grid(row=8,column=2)

tela3.mainloop()
"""=====================================================================================================================            
                                               FIM DO PROGRAMA
====================================================================================================================="""

