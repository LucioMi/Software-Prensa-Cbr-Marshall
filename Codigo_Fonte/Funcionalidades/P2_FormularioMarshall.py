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
#salva os valores digitados pelo usuario no db, fecha a janela atual e abre a tela de ensaio
def Salvar():                                                  
    try:
        #conecção com o bd e reset do banco
        conexao = pymysql.connect(host='localhost', user='root', passwd='', database='db_prensa_software'); cursor = conexao.cursor()
        cursor.execute("TRUNCATE TABLE ensaio_marshall;")
        #variaveis temporarias para guardar os valores digitados pelo usuario
        x1 = str(registro.get()); x2 = str(dia.get()); x3 = str(id_cp.get()); x4 = str(material.get()); x5 = str(obra.get()); 
        x6 = str(operador.get()); x7 = str(trecho.get()); x8 = str(subtrecho.get()); x9 = float(peso_ar.get()); x10 = float(peso_imerso.get()); 
        x11 = float(volume.get()); x12 = float(densi_aparent.get()); x13 = float(densi_teorica.get()); x14 = float(temperatura.get());
        x15 = float(vazios.get()); x16 = float(v_c_b.get()); x17 = float(v_a_m.get()); x18 = float(r_v_b.get()); x19 = float(amostra_antes.get());
        x20 = float(amostra_depois.get()); x21 = float(peso_betume.get()); x22 = float(teor_betume.get()); x23 = float(area.get()); 
        x24 = float(leit_defle.get()); x25 = float(estab_corrigida.get())
        sql = 'INSERT INTO ensaio_marshall (registro, dia, id_cp, material, obra, operador, trecho, subtrecho, peso_ar, peso_imerso, volume, densi_aparente, densi_teorica, temperatura, vazios, v_c_b, v_a_m, r_v_b, amostra_antes, amostra_depois, peso_betume, teor_betume, area, leit_deflet,estab_corrigida) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        sql_data = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23, x24, x25]
        cursor.execute(sql, sql_data); conexao.commit(); cursor.close()   
        tela2.destroy(); run(r"Funcionalidades\P4_TelaDeEnsaioMarshall.exe", shell=True)
    except:
        messagebox.showwarning("ERRO!!!!!","Verifique se os dados foram preenchidos corretamente:\n\n    Todos os campos devem ser "
        "preenchidos\n\n    Apenas os campos registro, data, identificação do cp, material, obra, operador, trecho e subtrecho admitem letras e " "numeros os demais valores são numericos\n\n    Os valores numericos devem ser separados usando o  ponto final (.) como separador decimal")

#volta para a janela anterior (tela P1)
def Voltar():
    tela2.destroy(); run(r"Funcionalidades\P1_TelaPrincipal.exe", shell=True)
"""==================================================================================================================================================
                                                   CRIAÇÃO DA TELA, WIDGETS E BOTÕES
=================================================================================================================================================="""
#definindo janela tkinter e suas configurações
tela2 = Tk(); tela2.iconbitmap(default=r"Funcionalidades\tela1.ico"); tela2.title("Formulario Ensaio Marshall"); tela2.geometry('1366x705+-11+1')
img_fundo=PhotoImage(file=r"Funcionalidades\tela_formulario_marshall.png"); label_fundo = Label(tela2, image=img_fundo); label_fundo.place(x=0, y=0)

#definindo as caixas de entrada e suas repectivas posições
registro = Entry(tela2, width=20); registro.place(width=102, height=26, x=135, y=123)
dia = Entry(tela2, width=20); dia.place(width=100, height=29, x=347, y=119)
id_cp = Entry(tela2, width=20); id_cp.place(width=110, height=29, x=698, y=122)
material = Entry(tela2, width=20); material.place(width=298, height=20, x=967, y=123)
obra = Entry(tela2, width=20); obra.place(width=287, height=27, x=102, y=178)
operador = Entry(tela2, width=20); operador.place(width=284, height=28, x=531, y=179)
trecho = Entry(tela2, width=20); trecho.place(width=287, height=29, x=989, y=178)
subtrecho = Entry(tela2, width=20); subtrecho.place(width=292, height=27, x=138, y=229)
peso_ar = Entry(tela2, width=20); peso_ar.place(width=102, height=28, x=169, y=287)
peso_imerso = Entry(tela2, width=20); peso_imerso.place(width=102, height=22, x=166, y=363)
volume = Entry(tela2, width=20); volume.place(width=103, height=26, x=169, y=425)
densi_aparent = Entry(tela2, width=20); densi_aparent.place(width=101, height=28, x=171, y=504)
densi_teorica = Entry(tela2, width=20); densi_teorica.place(width=105, height=28, x=166, y=573)
temperatura = Entry(tela2, width=20); temperatura.place(width=101, height=27, x=172, y=627)
vazios = Entry(tela2, width=20); vazios.place(width=99, height=31, x=438, y=283)
v_c_b = Entry(tela2, width=20); v_c_b.place(width=102, height=28, x=436, y=350)
v_a_m = Entry(tela2, width=20); v_a_m.place(width=101, height=28, x=440, y=404)
r_v_b = Entry(tela2, width=20); r_v_b.place(width=103, height=27, x=435, y=458)
amostra_antes = Entry(tela2, width=20); amostra_antes.place(width=95, height=30, x=502, y=512)
amostra_depois = Entry(tela2, width=20); amostra_depois.place(width=102, height=28, x=779, y=285)
peso_betume = Entry(tela2, width=20); peso_betume.place(width=99, height=29, x=782, y=340)
teor_betume = Entry(tela2, width=20); teor_betume.place(width=100, height=26, x=782, y=397)
area = Entry(tela2, width=20); area.place(width=103, height=27, x=779, y=450)
leit_defle = Entry(tela2, width=20); leit_defle.place(width=100, height=27, x=781, y=513)
estab_corrigida = Entry(tela2, width=20); estab_corrigida.place(width=102, height=28, x=1188, y=283)

#definindo botôes
B_Salvar = Button(tela2,text="SALVAR",bg="green", command=Salvar, font=("Arial",20)); B_Salvar.place(width=137, height=50, x=535, y=638)
B_Voltar = Button(tela2,text="VOLTAR",bg="yellow",command=Voltar, font=("Arial",20)); B_Voltar.place(width=137, height=50, x=735, y=638)

tela2.mainloop()
"""==================================================================================================================================================
                                                           FIM DO PROGRAMA
=================================================================================================================================================="""
