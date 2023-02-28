"""=====================================================================================================================
                                                 IMPORTAÇÕES
====================================================================================================================="""
import pymysql
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from datetime import datetime
"""=====================================================================================================================
                                                 VARIAVEIS
====================================================================================================================="""
forca = []
forca1 = []
deslocamento = []
deslocamento1 = []
data_atual = datetime.now()
data_str = data_atual.strftime('Relatorio_%d-%m-%Y_%H-%M')                   #transforma a data atual no nome do arquivo
pastaApp = os.path.dirname(f'Relatorios\{data_str}.pdf')                                        #caminho da pasta do pdf
"""=====================================================================================================================
                                                  FUNÇÕES
====================================================================================================================="""
def mm_ponto(mm):                                                          #converte o tamanha de pontos para milimetros
    return mm/0.352777

def criar_pdf():
    cnv = canvas.Canvas(pastaApp + f'\{data_str}.pdf',
                        pagesize=A4)  # pasta,nome e tamanho do pdf (aqui muda qual pdf vai salvar)
    cnv.drawImage(r"Funcionalidades\grafico1_relatorio.png",#coloca a imagem no ponto especolhido e no tamanho escolhido
                  mm_ponto(0), mm_ponto(140), width=mm_ponto(150), height=mm_ponto(100))
    cnv.drawString(mm_ponto(10), mm_ponto(290), f'MASSA ESPECIFICA APARENTE:....{M_Esp_Aparente}')        #escreve no pdf
    cnv.drawString(mm_ponto(10), mm_ponto(283), f'MASSA ESPECIFICA MAXIMA:.........{M_Esp_Max}')
    cnv.drawString(mm_ponto(10), mm_ponto(276), f'VOLUME DE VAZIOS:...........{Vazios}')
    cnv.drawString(mm_ponto(10), mm_ponto(269), f'VAZIOS AGREGADO MINEIRAL:......{V_Agragado}')
    cnv.drawString(mm_ponto(10), mm_ponto(262), f'RELAÇÃO BETUME/VAZIOS:.....{Betume_v} ')
    cnv.drawString(mm_ponto(10), mm_ponto(255), f'ESTABILIDADE:.............{Estabilidad} ')
    cnv.drawString(mm_ponto(10), mm_ponto(248), f'TEOR DE ASFALTO:.......{Teor_Asfalt} ')
    cnv.save()                                                                                             #salva no pdf
"""=====================================================================================================================
                                    CONEXÃO COM BD E TRATAMENTO DE DADOS
====================================================================================================================="""
conexao = pymysql.connect ( host='localhost',
                            user='root', passwd='',database='db_prensa_software')
cursor = conexao.cursor()

cursor.execute(f"SELECT forca_t FROM teste;")                                        #Seleciona os dados da tabela do BD
forca1 = cursor.fetchall()                        #Salva os valores selecionados em uma variavel(a variavel é uma tupla)
cursor.execute(f"SELECT deslocamento_t FROM teste;")
deslocamento1 = cursor.fetchall()
Cont = len(forca1)                                                             #Pega o tamanho da tupla para usar no for

for y in range(0, Cont):                                             #Salva os dados string do BD como float em uma lista
    var = str(forca1[y])                                              #Transforma em string para poder manipular a tupla
    var = var.replace("(", "")                        #Tira os dados desnecessarios da string para ela poder virar float
    var = float(var.replace(",)", ""))
    forca.append(var)                                                                      #Cria a lista definitivamente
    var = str(deslocamento1[y])
    var = var.replace("(", "")
    var = float(var.replace(",)", ""))
    deslocamento.append(var)

cursor.execute(f"SELECT M_Aparente FROM grafico;")              #salvando valores do banco em uma variavel para exibição
M_Esp_Aparente = str(cursor.fetchall())
M_Esp_Aparente = M_Esp_Aparente.replace("(('", "")                                                   #Manipulando String
M_Esp_Aparente = float(M_Esp_Aparente.replace("',),)", ""))

cursor.execute(f"SELECT M_Max FROM grafico;")
M_Esp_Max = str(cursor.fetchall())
M_Esp_Max = M_Esp_Max.replace("(('", "")
M_Esp_Max = float(M_Esp_Max.replace("',),)", ""))

cursor.execute(f"SELECT Vazio FROM grafico;")
Vazios = str(cursor.fetchall())
Vazios = Vazios.replace("(('", "")
Vazios = float(Vazios.replace("',),)", ""))

cursor.execute(f"SELECT Agregado FROM grafico;")
V_Agragado = str(cursor.fetchall())
V_Agragado = V_Agragado.replace("(('", "")
V_Agragado = float(V_Agragado.replace("',),)", ""))

cursor.execute(f"SELECT Betume FROM grafico;")
Betume_v = str(cursor.fetchall())
Betume_v = Betume_v.replace("(('", "")
Betume_v = float(Betume_v.replace("',),)", ""))

cursor.execute(f"SELECT Estabilidade FROM grafico;")
Estabilidad = str(cursor.fetchall())
Estabilidad = Estabilidad.replace("(('", "")
Estabilidad = float(Estabilidad.replace("',),)", ""))

cursor.execute(f"SELECT Teor_Asfalto FROM grafico;")
Teor_Asfalt = str(cursor.fetchall())
Teor_Asfalt = Teor_Asfalt.replace("(('", "")
Teor_Asfalt = float(Teor_Asfalt.replace("',),)", ""))

plt.plot(deslocamento, forca, ls='-', lw=2, marker='o')
plt.axis([0, 25.5, 0, 5100])
plt.grid(True)
plt.ylabel('FORÇA (Kg/F)')
plt.xlabel('DESLOCAMENTO (mm)')
plt.title('GRAFICO: FORÇA(Kg/f) x DESLOCAMENTO(mm) ')
plt.savefig(r"Funcionalidades\grafico1_relatorio.png", dpi=150)                                         #salva o grafico como uma imagem

criar_pdf()                                                                          #Chama a função que vai criar o pdf
"""=====================================================================================================================            
                                               FIM DO PROGRAMA
====================================================================================================================="""




