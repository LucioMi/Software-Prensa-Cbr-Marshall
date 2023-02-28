"""=====================================================================================================================
                                          IMPORTAÇÃO DE MODULOS
====================================================================================================================="""
from tkinter import *
from tkinter import messagebox
import pymysql
from subprocess import run
"""=====================================================================================================================
                                                  FUNÇÕES
====================================================================================================================="""
def Salvar():                                                 #FUÇÃO PARA SALVAR OS VALORES DIGITADOS PELO USUARIO NO BD
    try:
        cursor.execute("TRUNCATE TABLE grafico;")                            #APAGA OS VALORES DO ULTIMO RELATORIO NO BD
        x1 = float(M_Aparent.get())
        x2 = float(M_Maxi.get())
        x3 = float(Vazios.get())
        x4 = float(Agregad.get())
        x5 = float(Betum.get())
        x6 = float(Estabilidad.get())
        x7 = float(Teor_Asfalt.get())
        sql = 'INSERT INTO grafico(M_Aparente,M_Max,Vazio,Agregado,Betume,Estabilidade,Teor_Asfalto) ' \
              'VALUES (%s,%s,%s,%s,%s,%s,%s)'                   #CHAMADA PARA SALVAR OS NOVOS VALORES DO RELATORIO NO BD
        sql_data = [x1, x2, x3, x4, x5, x6, x7]
        cursor.execute(sql,sql_data)
        conexao.commit()
        tela2.destroy()
        run(r"Funcionalidades\P4_TelaDeEnsaioMarshall.exe", shell=True)
    except:
        messagebox.showwarning("ERRO!!!!!",                                     #CRIA UMA CAIXA COM UMA MENSAGEM DE ERRO
                               "Verifique se os dados foram preenchidos corretamente")

def Voltar():
    tela2.destroy()
    run(r"Funcionalidades\P1_TelaPrincipal.exe", shell=True)
"""=====================================================================================================================
                            CRIAÇÃO DE WIDGETS,LAYOUT DA TELA E CONECÇÃO COM O BD
====================================================================================================================="""
conexao = pymysql.connect(host='localhost',user='root',passwd='',database='db_prensa_software')
cursor = conexao.cursor()                                                   #CONEXÃO COM O BANCO DE DADOS DESCRITO ACIMA

tela2 = Tk()
tela2.iconbitmap(default=r"Funcionalidades\tela1.ico")
tela2.title("Formulario Ensaio Marshall")
tela2.geometry('1366x705+-11+1')

label_Aparente = Label(tela2,font="Arial 12 bold",text="Massa especifica aparente (g/cm3): ")            #CRIA UM TEXTO
label_Aparente.grid(row=0,column=0)                                                #DEFINE A POSIÇÃO DO LABEL POR 'GRID'
M_Aparent = Entry(tela2, width=20)                                       #cria uma caixa de entrada como nome M_Aparent
M_Aparent.grid(row=0,column=1)

label_Max = Label(tela2, text="Massa especifica máxima (g/cm3): ",font="Arial 12 bold")
label_Max.grid(row=1,column=0)
M_Maxi = Entry(tela2, width=20)
M_Maxi.grid(row=1,column=1)

label_vazios = Label(tela2, text="Volume de vazios (%): ",font="Arial 12 bold")
label_vazios.grid(row=2,column=0)
Vazios = Entry(tela2, width=20)
Vazios.grid(row=2,column=1)

label_Agregado = Label(tela2, text="Vazios de agregado mineral (%): ",font="Arial 12 bold")
label_Agregado.grid(row=3,column=0)
Agregad = Entry(tela2, width=20)
Agregad.grid(row=3,column=1)

label_Betume = Label(tela2, text="Relação betume/vazio (%): ",font="Arial 12 bold")
label_Betume.grid(row=4,column=0)
Betum = Entry(tela2, width=20)
Betum.grid(row=4,column=1)

label_Estabilidade = Label(tela2, text="Estabilidade (N) ",font="Arial 12 bold")
label_Estabilidade.grid(row=5,column=0)
Estabilidad = Entry(tela2, width=20)
Estabilidad.grid(row=5,column=1)

label_Asfalto = Label(tela2, text="Teor de asfalto (%) ",font="Arial 12 bold")
label_Asfalto.grid(row=6,column=0)
Teor_Asfalt = Entry(tela2, width=20)
Teor_Asfalt.grid(row=6,column=1)

B_Salvar = Button(tela2,text="SALVAR",bg="green", command=Salvar, font=("Arial",20))
B_Salvar.grid(row=8,column=0)

B_Voltar = Button(tela2,text="VOLTAR",bg="red",command=Voltar, font=("Arial",20))
B_Voltar.grid(row=8,column=2)

tela2.mainloop()
"""=====================================================================================================================            
                                               FIM DO PROGRAMA
====================================================================================================================="""
