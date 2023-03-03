"""=====================================================================================================================
                                          IMPORTAÇÃO DE MODULOS
====================================================================================================================="""
from tkinter import *        #importa o modulo
from subprocess import run
from tkinter import messagebox
import Posicionador_De_Objetos
import pymysql
"""=====================================================================================================================
                                                  FUNÇÕES
====================================================================================================================="""
def Salvar():

        #conecção com o bd e reset do banco
        conexao = pymysql.connect(host='localhost', user='root', passwd='', database='db_prensa_software')
        cursor = conexao.cursor()
        cursor.execute("TRUNCATE TABLE id_amostra_cbr;"); cursor.execute("TRUNCATE TABLE id_cp_cbr;")
        #variaveis temporarias para guardar os valores digitados pelo usuario
        x1 = str(operador.get()); x2 = str(obra.get()); x3 = str(trecho.get()); x4 = str(subtrecho.get())
        x5 = str(data.get()); x6 = str(material.get()); x7 = str(n_molde.get()); x8 = float(exp_0.get())
        x9 = float(exp_1.get()); x10 = float(exp_2.get()); x11 = float(exp_3.get()); x12 = float(exp_4.get())
        x13 = float(m_cilindro.get()); x14 = float(m_amostra.get()); x15 = float(volume.get())
        x16 = float(expansao.get()); x17 = float(m_amostra_m_cilindro.get()); x18 = float(peso_exp_umido.get())
        x19 = float(m_esp_seca.get()); x20 = float(altura.get()); x21 = float(amostra.get()); x22 = int(ener.get());
        x23 = float(teor_umidade_media.get())
        sql = 'INSERT INTO id_amostra_cbr (amostra, dia, energia, material, obra, operador, subtrecho, trecho) ' \
              'VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'  # CHAMADA PARA SALVAR OS NOVOS VALORES DO RELATORIO NO BD
        sql_data = [x21, x5, x22, x6, x2, x1, x4, x3]
        cursor.execute(sql, sql_data)
        conexao.commit()

        #DAQUI PRA CIMA TA MEC
        sql = 'INSERT INTO id_amostra_cbr (altura_inicial, exp_umidade_otima, id_molde, leitura_exp0, leitura_exp1,' \
              'leitura_exp2, leitura_exp3, leitura_exp4, massa_amosta, massa_amostra_cilindro, massa_cilindro, ' \
              'massa_esp_ap_seca, peso_esp_umido, teor_umidade_media, volume) ' \
              'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        sql_data = [x20, x16, x7, x8, x9, x10, x11, x12, x14, x17, x13, x19, x18, x23, x15]
        cursor.execute(sql, sql_data)
        conexao.commit()
        cursor.close()
        tela3.destroy()
        #run(r"Funcionalidades\P4_TelaDeEnsaioMarshall.exe", shell=True)       #esta indo pra tela marshall a titulo de teste


def Voltar():
    tela3.destroy()
    run(r"Funcionalidades\P1_TelaPrincipal.exe", shell=True)
"""=====================================================================================================================
                            CRIAÇÃO DE WIDGETS,LAYOUT DA TELA E CONECÇÃO COM O BD
====================================================================================================================="""
#definindo janela tkinter e suas respectivas imagens
tela3 = Tk()
#tela3.iconbitmap(default=r"Funcionalidades\tela1.ico")         ESTA AQUI A TITULO DE TESTE MUDAR APÓS TERMINAR
tela3.iconbitmap(default="tela1.ico")
tela3.title("Formulario Ensaio CBR")
tela3.geometry('1366x705+-11+1')
#img_fundo = PhotoImage(file=r"Funcionalidades\tela_formulario_cbr.png") ESTA AQUI A TITULO DE TESTE MUDAR APÓS TERMINAR
img_fundo = PhotoImage(file="tela_formulario_cbr.png")
label_fundo = Label(tela3, image=img_fundo)
label_fundo.place(x=0, y=0)

#definindo as caixas de entrada e suas repectivas posições
operador = Entry(tela3, width=20); operador.place(width=477, height=29, x=137, y=128)
obra = Entry(tela3, width=20); obra.place(width=478, height=27, x=138, y=186)
trecho = Entry(tela3, width=20); trecho.place(width=471, height=28, x=140, y=245)
subtrecho = Entry(tela3, width=20); subtrecho.place(width=470, height=30, x=138, y=302)
data = Entry(tela3, width=20); data.place(width=113, height=26, x=852, y=128)
material = Entry(tela3, width=20); material.place(width=160, height=25, x=1185, y=152)
amostra = Entry(tela3, width=20) ; amostra.place(width=157, height=29, x=1189, y=237)
n_molde = Entry(tela3, width=20); n_molde.place(width=110, height=26, x=928, y=290)
exp_0 = Entry(tela3, width=20); exp_0.place(width=110, height=22, x=232, y=367)
exp_1 = Entry(tela3, width=20); exp_1.place(width=110, height=27, x=228, y=425)
exp_2 = Entry(tela3, width=20); exp_2.place(width=112, height=26, x=227, y=486)
exp_3 = Entry(tela3, width=20); exp_3.place(width=110, height=26, x=225, y=547)
exp_4 = Entry(tela3, width=20); exp_4.place(width=114, height=24, x=228, y=608)
m_cilindro = Entry(tela3, width=20); m_cilindro.place(width=125, height=27, x=687, y=353)
m_amostra = Entry(tela3, width=20); m_amostra.place(width=122, height=27, x=688, y=404)
volume = Entry(tela3, width=20); volume.place(width=123, height=28, x=686, y=464)
expansao = Entry(tela3, width=20); expansao.place(width=122, height=27, x=686, y=522)
m_amostra_m_cilindro = Entry(tela3, width=20); m_amostra_m_cilindro.place(width=110, height=28, x=1225, y=354)
peso_exp_umido = Entry(tela3, width=20); peso_exp_umido.place(width=108, height=27, x=1227, y=412)
m_esp_seca = Entry(tela3, width=20); m_esp_seca.place(width=108, height=30, x=1225, y=471)
altura = Entry(tela3, width=20); altura.place(width=113, height=27, x=1222, y=533)
teor_umidade_media = Entry(tela3, width=20); teor_umidade_media.place(width=111, height=29, x=1224, y=590)

#definindo botôes
B_Salvar = Button(tela3,text="SALVAR",bg="green", command=Salvar, font=("Arial",20))
B_Salvar.place(width=137, height=50, x=1000, y=643)
B_Voltar = Button(tela3,text="VOLTAR",bg="yellow",command=Voltar, font=("Arial",20))
B_Voltar.place(width=137, height=50, x=1200, y=643)
#Cria radiobuton para escolher "energia" que ja tem valores pre definidos pela norma
ener = IntVar()
ener_12 = Radiobutton(tela3, text="12", value=12, variable=ener); ener_12.pack()
ener_35 = Radiobutton(tela3, text="35", value=35, variable=ener); ener_35.pack()
ener_56 = Radiobutton(tela3, text="56", value=56, variable=ener); ener_56.pack()
ener_12.place(width=56, height=52, x=845, y=200); ener_35.place(width=56, height=52, x=897, y=200);
ener_56.place(width=56, height=52, x=949, y=200);
"""
tela3.bind('<Button-1>', lambda e: Posicionador_De_Objetos.m_btn1(e, tela3))
tela3.bind('<Button-3>', lambda e: Posicionador_De_Objetos.m_btn3(e, tela3))
tela3.bind('<ButtonRelease-1>', lambda e: Posicionador_De_Objetos.m_btn1_release(e, tela3))
"""
tela3.mainloop()
"""=====================================================================================================================            
                                               FIM DO PROGRAMA
====================================================================================================================="""

