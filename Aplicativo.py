from subprocess import run
import pymysql

try:                                                                      #Verifica se existe o BD se não tiver ele cria
    conexao = pymysql.connect(host='localhost', user='root', passwd='', database='db_prensa_software')
    cursor = conexao.cursor()                                               #CONEXÃO COM O BANCO DE DADOS DESCRITO ACIMA
    cursor.close()                                                                      #desconecta com o banco de dados
except:
    conexao = pymysql.connect(host='localhost', user='root', passwd='')
    cursor = conexao.cursor()
    cursor.execute("CREATE DATABASE db_prensa_software")
    conexao = pymysql.connect(host='localhost', user='root', passwd='', database='db_prensa_software')
    cursor = conexao.cursor()                                               #CONEXÃO COM O BANCO DE DADOS DESCRITO ACIMA
    cursor.execute("CREATE TABLE Grafico ("                                  #cria uma tabela para os valores de entrada
                   "M_Aparente float not null,"
                   "M_Max float not null,"
                   "Vazio float not null,"
                   "Agregado float not null,"
                   "Betume float not null,"
                   "Estabilidade float not null,"
                   "Teor_Asfalto float not null);")
    cursor.execute("CREATE TABLE teste ("                                  #cria uma tabela para os valores dos sensores
                   "deslocamento_t float not null,"
                   "forca_t float not null);")
    cursor.close()

run(r"Funcionalidades\P1_TelaPrincipal.exe", shell=True)