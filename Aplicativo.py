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
    #TABELAS DO BD PARA O ENSAIO MARSHALL
    cursor.execute("CREATE TABLE ensaio_marshall ("                                  #cria uma tabela para os valores de entrada
                   "registro varchar(255),"
                   "dia varchar(255),"
                   "id_cp varchar(255),"
                   "material varchar(255),"
                   "obra varchar(255),"
                   "operador varchar(255),"
                   "trecho varchar(255),"
                   "subtrecho varchar(255),"
                   "peso_ar float,"
                   "peso_imerso float,"
                   "volume float,"
                   "densi_aparente float,"
                   "densi_teorica float,"
                   "temperatura float,"
                   "vazios float,"
                   "v_c_b float,"
                   "v_a_m float,"
                   "r_v_b float,"
                   "amostra_antes float,"
                   "amostra_depois float,"
                   "peso_betume float,"
                   "teor_betume float,"
                   "comp_diame float,"
                   "leit_deflet float);")
    #TABELAS DO BD PARA O ENSAIO CBR:
    cursor.execute("create TABLE id_ensaio_cbr (" 
        "registro int not null primary key auto_increment,"
        "dia varchar(255),"
        "obra varchar(255),"
        "operador varchar(255),"
        "material varchar(255),"
        "trecho varchar(255),"
        "subtrecho varchar(255),"
        "energia int,"
        "furo varchar(255),"
        "amostra varchar(255));")
    cursor.execute("CREATE table id_cp_cbr ("
        "id_molde varchar(5) not null,"
        "massa_amostra_cilindro float not null,"
        "massa_cilindro float not null,"
        "volume float not null,"
        "massa_amosta float not null,"
        "peso_esp_umido float not null,"
        "teor_umidade_media float not null,"
        "massa_esp_ap_seca float not null,"
        "altura_inicial float not null,"
        "leitura_exp0 float not null,"             
        "leitura_exp1 float not null,"
        "leitura_exp2 float not null,"
        "leitura_exp3 float not null,"
        "leitura_exp4 float not null,"
        "exp_umidade_otima float not null);")
    cursor.execute("CREATE table ensaio_cbr ("
        "carga1 float not null,"
        "Carga2 float not null,"
        "Carga3 float not null,"
        "Carga4 float not null,"
        "Carga5 float not null,"
        "Carga6 float not null,"
        "Carga7 float not null,"
        "Carga8 float not null,"
        "Carga9 float not null,"
        "Carga10 float not null,"
        "Carga11 float not null,"
        "Carga12 float not null,"
        "Carga13 float not null,"
        "isc_254 float not null,"
        "isc_508 float not null);")
    cursor.close()

run(r"Funcionalidades\P1_TelaPrincipal.exe", shell=True)                  #para funconar no executavel tem de ser assim

