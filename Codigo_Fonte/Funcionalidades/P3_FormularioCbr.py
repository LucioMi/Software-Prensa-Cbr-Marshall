"""==================================================================================================================================================
                                                        IMPORTAÇÃO DE MODULOS
=================================================================================================================================================="""
from tkinter import *      
from subprocess import run
from tkinter import messagebox
import pymysql
"""==================================================================================================================================================
                                                               FUNÇÕES
=================================================================================================================================================="""
def Salvar():
    try:
        #conecção com o bd e reset do banco
        conexao = pymysql.connect(host='localhost', user='root', passwd='', database='db_prensa_software')
        cursor = conexao.cursor()
        cursor.execute("TRUNCATE TABLE ensaio_cbr;")
        #variaveis temporarias para guardar os valores digitados pelo usuario
        x1 = str(registro.get()); x2 = str(data.get()); x3 = str(material.get()); x4 = str(n_molde.get()); x5 = str(amostra.get());
        x6 = str(furo.get()); x7 = int(ener.get()); x8 = str(obra.get()); x9 = str(operador.get()); x10 = str(trecho.get()); 
        x11 = str(subtrecho.get()); x12 = float(m_amostra_m_cilindro.get()); x13 = float(m_cilindro.get()); x14 = float(volume.get()); 
        x15 = float(m_amostra.get()); x16 = float(peso_exp_umido.get()); x17 = float(teor_umidade_media.get()); x18 = float(m_esp_seca.get());
        x19 = float(altura.get()); x20 = float(exp_0.get()); x21 = float(exp_1.get()); x22 = float(exp_2.get()); x23 = float(exp_3.get()); 
        x24 = float(exp_4.get()); x25 = float(expansao.get())
        sql = 'INSERT INTO ensaio_cbr (registro, dia, material, id_molde, amostra, furo, energia, obra, operador, trecho, subtrecho,massa_amostra_cilindro, massa_cilindro, volume, massa_amosta, peso_esp_umido, teor_umidade_media, massa_esp_ap_seca, altura_inicial,leitura_exp0, leitura_exp1, leitura_exp2, leitura_exp3, leitura_exp4, exp_umidade_otima) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        sql_data = [x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19,x20,x21,x22,x23,x24,x25]
        cursor.execute(sql, sql_data); conexao.commit(); cursor.close()   
        tela3.destroy()
        run(r"Funcionalidades\P5_TelaDeEnsaioCbr.exe", shell=True)
    except:
        messagebox.showwarning("ERRO!!!!!","Verifique se os dados foram preenchidos corretamente")

def Voltar():
    tela3.destroy()
    run(r"Funcionalidades\P1_TelaPrincipal.exe", shell=True)
"""==================================================================================================================================================
                                               CRIAÇÃO DE WIDGETS,LAYOUT DA TELA 
=================================================================================================================================================="""
#definindo janela tkinter e suas respectivas imagens
tela3 = Tk()
tela3.iconbitmap(default=r"Funcionalidades\tela1.ico"); tela3.title("Formulario Ensaio CBR"); tela3.geometry('1366x705+-11+1')
img_fundo = PhotoImage(file=r"Funcionalidades\tela_formulario_cbr.png")
label_fundo = Label(tela3, image=img_fundo); label_fundo.place(x=0, y=0)

#definindo as caixas de entrada e suas repectivas posições
registro = Entry(tela3, width=20); registro.place(width=113, height=26, x=151, y=138)
data = Entry(tela3, width=20); data.place(width=111, height=27, x=417, y=136)
material = Entry(tela3, width=20); material.place(width=162, height=28, x=745, y=137)
n_molde = Entry(tela3, width=20); n_molde.place(width=111, height=23, x=1182, y=139)
amostra = Entry(tela3, width=20) ; amostra.place(width=167, height=26, x=132, y=188)
furo = Entry(tela3, width=20); furo.place(width=161, height=27, x=417, y=186)
obra = Entry(tela3, width=20); obra.place(width=282, height=29, x=107, y=246)
operador = Entry(tela3, width=20); operador.place(width=285, height=26, x=546, y=246)
trecho = Entry(tela3, width=20); trecho.place(width=280, height=23, x=972, y=250)
subtrecho = Entry(tela3, width=20); subtrecho.place(width=287, height=26, x=137, y=307)
m_amostra_m_cilindro = Entry(tela3, width=20); m_amostra_m_cilindro.place(width=111, height=28, x=1078, y=358)
m_cilindro = Entry(tela3, width=20); m_cilindro.place(width=119, height=28, x=584, y=352)
volume = Entry(tela3, width=20); volume.place(width=119, height=24, x=584, y=468)
m_amostra = Entry(tela3, width=20); m_amostra.place(width=114, height=28, x=587, y=406)
peso_exp_umido = Entry(tela3, width=20); peso_exp_umido.place(width=111, height=27, x=1083, y=408)
teor_umidade_media = Entry(tela3, width=20); teor_umidade_media.place(width=111, height=27, x=619, y=573)
m_esp_seca = Entry(tela3, width=20); m_esp_seca.place(width=110, height=24, x=1081, y=457)
altura = Entry(tela3, width=20); altura.place(width=115, height=25, x=1078, y=508)
exp_0 = Entry(tela3, width=20); exp_0.place(width=110, height=22, x=240, y=367)
exp_1 = Entry(tela3, width=20); exp_1.place(width=110, height=27, x=238, y=425)
exp_2 = Entry(tela3, width=20); exp_2.place(width=112, height=26, x=242, y=486)
exp_3 = Entry(tela3, width=20); exp_3.place(width=110, height=26, x=244, y=547)
exp_4 = Entry(tela3, width=20); exp_4.place(width=114, height=24, x=246, y=608)
expansao = Entry(tela3, width=20); expansao.place(width=118, height=26, x=584, y=524)

#definindo botôes
B_Salvar = Button(tela3,text="SALVAR",bg="yellow", command=Salvar, font=("Arial",20)); B_Salvar.place(width=137, height=50, x=535, y=638)
B_Voltar = Button(tela3,text="VOLTAR",bg="red",command=Voltar, font=("Arial",20)); B_Voltar.place(width=137, height=50, x=735, y=638)
#Cria radiobuton para escolher "energia" que ja tem valores pre definidos pela norma
ener = IntVar()
ener_12 = Radiobutton(tela3, text="12", value=12, variable=ener); ener_12.pack()
ener_26 = Radiobutton(tela3, text="26", value=26, variable=ener); ener_26.pack()
ener_55 = Radiobutton(tela3, text="55", value=55, variable=ener); ener_55.pack()
ener_12.place(width=54, height=52, x=746, y=180); ener_26.place(width=56, height=52, x=798, y=180); ener_55.place(width=56, height=52, x=850, y=180);

tela3.mainloop()
"""==================================================================================================================================================
                                                            FIM DO PROGRAMA
=================================================================================================================================================="""