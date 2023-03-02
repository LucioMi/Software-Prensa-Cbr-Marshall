"""=====================================================================================================================
                                          IMPORTAÇÃO DE MODULOS
====================================================================================================================="""
from tkinter import *        #importa o modulo
from subprocess import run
import Posicionador_De_Objetos
import pymysql
"""=====================================================================================================================
                                                  FUNÇÕES
====================================================================================================================="""
def Salvar():
    conexao = pymysql.connect(host='localhost', user='root', passwd='', database='db_prensa_software')
    cursor = conexao.cursor()
    cursor.execute("TRUNCATE TABLE id_amostra_cbr; TRUNCATE TABLE id_cp_cbr;")
    tela3.destroy()
    run(r"Funcionalidades\P4_TelaDeEnsaioMarshall.exe", shell=True)       #esta indo pra tela marshall a titulo de teste

def Voltar():
    tela3.destroy()
    run(r"Funcionalidades\P1_TelaPrincipal.exe", shell=True)
"""=====================================================================================================================
                            CRIAÇÃO DE WIDGETS,LAYOUT DA TELA E CONECÇÃO COM O BD
====================================================================================================================="""
tela3 = Tk()
#tela3.iconbitmap(default=r"Funcionalidades\tela1.ico")         ESTA AQUI A TITULO DE TESTE MUDAR APÓS TERMINAR
tela3.iconbitmap(default="tela1.ico")
tela3.title("Formulario Ensaio CBR")
tela3.geometry('1366x705+-11+1')
#img_fundo = PhotoImage(file=r"Funcionalidades\tela_formulario_cbr.png") ESTA AQUI A TITULO DE TESTE MUDAR APÓS TERMINAR
img_fundo = PhotoImage(file="tela_formulario_cbr.png")
label_fundo = Label(tela3, image=img_fundo)
label_fundo.place(x=0, y=0)

operador = Entry(tela3, width=20)
operador.place(width=477, height=29, x=137, y=128)
obra = Entry(tela3, width=20)
obra.place(width=478, height=27, x=138, y=186)
trecho = Entry(tela3, width=20)
trecho.place(width=471, height=28, x=140, y=245)
subtrecho = Entry(tela3, width=20)
subtrecho.place(width=470, height=30, x=138, y=302)
data = Entry(tela3, width=20)
data.place(width=113, height=26, x=852, y=128)
material = Entry(tela3, width=20)
material.place(width=160, height=25, x=1185, y=152)
amostra = Entry(tela3, width=20)
amostra.place(width=157, height=29, x=1189, y=237)
n_molde = Entry(tela3, width=20)
n_molde.place(width=110, height=26, x=928, y=290)
exp_0 = Entry(tela3, width=20)
exp_0.place(width=110, height=22, x=232, y=367)
exp_1 = Entry(tela3, width=20)
exp_1.place(width=110, height=27, x=228, y=425)
exp_2 = Entry(tela3, width=20)

exp_3 = Entry(tela3, width=20)

exp_4 = Entry(tela3, width=20)





B_Salvar = Button(tela3,text="SALVAR",bg="green", command=Salvar, font=("Arial",20))
B_Salvar.place(width=137, height=50, x=1000, y=643)
B_Voltar = Button(tela3,text="VOLTAR",bg="yellow",command=Voltar, font=("Arial",20))
B_Voltar.place(width=137, height=50, x=1200, y=643)


tela3.bind('<Button-1>', lambda e: Posicionador_De_Objetos.m_btn1(e, tela3))
tela3.bind('<Button-3>', lambda e: Posicionador_De_Objetos.m_btn3(e, tela3))
tela3.bind('<ButtonRelease-1>', lambda e: Posicionador_De_Objetos.m_btn1_release(e, tela3))

tela3.mainloop()
"""=====================================================================================================================            
                                               FIM DO PROGRAMA
====================================================================================================================="""

