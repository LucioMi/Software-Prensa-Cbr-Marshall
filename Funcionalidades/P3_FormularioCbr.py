"""=====================================================================================================================
                                          IMPORTAÇÃO DE MODULOS
====================================================================================================================="""
from tkinter import *        #importa o modulo
from subprocess import run
from tkinter import messagebox
import pymysql
"""=====================================================================================================================
                                                  FUNÇÕES
====================================================================================================================="""
def Salvar():
    try:
        #conecção com o bd e reset do banco
        conexao = pymysql.connect(host='localhost', user='root', passwd='', database='db_prensa_software')
        cursor = conexao.cursor()
        cursor.execute("TRUNCATE TABLE id_ensaio_cbr;"); cursor.execute("TRUNCATE TABLE id_cp_cbr;")
        #variaveis temporarias para guardar os valores digitados pelo usuario
        x1 = str(operador.get()); x2 = str(obra.get()); x3 = str(trecho.get()); x4 = str(subtrecho.get())
        x5 = str(data.get()); x6 = str(material.get()); x7 = str(n_molde.get()); x8 = float(exp_0.get())
        x9 = float(exp_1.get()); x10 = float(exp_2.get()); x11 = float(exp_3.get()); x12 = float(exp_4.get())
        x13 = float(m_cilindro.get()); x14 = float(m_amostra.get()); x15 = float(volume.get())
        x16 = float(expansao.get()); x17 = float(m_amostra_m_cilindro.get()); x18 = float(peso_exp_umido.get())
        x19 = float(m_esp_seca.get()); x20 = float(altura.get()); x21 = float(amostra.get()); x22 = int(ener.get());
        x23 = float(teor_umidade_media.get()); x24 = str(furo.get())
        sql = 'INSERT INTO id_ensaio_cbr (amostra, dia, energia, material, obra, operador, subtrecho, trecho,furo) ' \
              'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'  # CHAMADA PARA SALVAR OS NOVOS VALORES DO RELATORIO NO BD
        sql_data = [x21, x5, x22, x6, x2, x1, x4, x3, x24]
        cursor.execute(sql, sql_data)
        conexao.commit()
        sql = 'INSERT INTO id_cp_cbr (altura_inicial, exp_umidade_otima, id_molde, leitura_exp0, leitura_exp1,' \
              'leitura_exp2, leitura_exp3, leitura_exp4, massa_amosta, massa_amostra_cilindro, massa_cilindro, ' \
              'massa_esp_ap_seca, peso_esp_umido, teor_umidade_media, volume) ' \
              'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        sql_data = [x20, x16, x7, x8, x9, x10, x11, x12, x14, x17, x13, x19, x18, x23, x15]
        cursor.execute(sql, sql_data)
        conexao.commit()   
        cursor.close()   
        tela3.destroy()
        run(r"Funcionalidades\P5_TelaDeEnsaioCbr.exe", shell=True)
    except:
        messagebox.showwarning("ERRO!!!!!",
                               "Verifique se os dados foram preenchidos corretamente")

def Voltar():
    tela3.destroy()
    run(r"Funcionalidades\P1_TelaPrincipal.exe", shell=True)
"""=====================================================================================================================
                            CRIAÇÃO DE WIDGETS,LAYOUT DA TELA E CONECÇÃO COM O BD
====================================================================================================================="""
#definindo janela tkinter e suas respectivas imagens
tela3 = Tk()
tela3.iconbitmap(default=r"Funcionalidades\tela1.ico")
tela3.title("Formulario Ensaio CBR")
tela3.geometry('1366x705+-11+1')
img_fundo = PhotoImage(file=r"Funcionalidades\tela_formulario_cbr.png")
label_fundo = Label(tela3, image=img_fundo)
label_fundo.place(x=0, y=0)

#definindo as caixas de entrada e suas repectivas posições
operador = Entry(tela3, width=20); operador.place(width=477, height=29, x=137, y=128)
obra = Entry(tela3, width=20); obra.place(width=478, height=27, x=138, y=186)
trecho = Entry(tela3, width=20); trecho.place(width=471, height=28, x=140, y=245)
subtrecho = Entry(tela3, width=20); subtrecho.place(width=470, height=30, x=138, y=302)
data = Entry(tela3, width=20); data.place(width=112, height=26, x=754, y=132)
amostra = Entry(tela3, width=20) ; amostra.place(width=161, height=27, x=755, y=242)
furo = Entry(tela3, width=20); furo.place(width=156, height=25, x=756, y=299)
material = Entry(tela3, width=20); material.place(width=156, height=30, x=1068, y=130)
n_molde = Entry(tela3, width=20); n_molde.place(width=110, height=24, x=1134, y=192)
teor_umidade_media = Entry(tela3, width=20); teor_umidade_media.place(width=105, height=26, x=1178, y=254)
exp_0 = Entry(tela3, width=20); exp_0.place(width=110, height=22, x=232, y=367)
exp_1 = Entry(tela3, width=20); exp_1.place(width=110, height=27, x=228, y=425)
exp_2 = Entry(tela3, width=20); exp_2.place(width=112, height=26, x=227, y=486)
exp_3 = Entry(tela3, width=20); exp_3.place(width=110, height=26, x=225, y=547)
exp_4 = Entry(tela3, width=20); exp_4.place(width=114, height=24, x=228, y=608)
m_cilindro = Entry(tela3, width=20); m_cilindro.place(width=119, height=26, x=580, y=357)
m_amostra = Entry(tela3, width=20); m_amostra.place(width=118, height=26, x=580, y=407)
volume = Entry(tela3, width=20); volume.place(width=119, height=23, x=581, y=468)
expansao = Entry(tela3, width=20); expansao.place(width=116, height=30, x=584, y=524)
m_amostra_m_cilindro = Entry(tela3, width=20); m_amostra_m_cilindro.place(width=109, height=25, x=1077, y=359)
peso_exp_umido = Entry(tela3, width=20); peso_exp_umido.place(width=109, height=26, x=1080, y=410)
m_esp_seca = Entry(tela3, width=20); m_esp_seca.place(width=112, height=24, x=1081, y=458)
altura = Entry(tela3, width=20); altura.place(width=107, height=25, x=1081, y=506)

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
ener_12.place(width=54, height=52, x=746, y=174); ener_35.place(width=56, height=52, x=798, y=174);
ener_56.place(width=56, height=52, x=850, y=174);

tela3.mainloop()
"""=====================================================================================================================            
                                               FIM DO PROGRAMA
====================================================================================================================="""

