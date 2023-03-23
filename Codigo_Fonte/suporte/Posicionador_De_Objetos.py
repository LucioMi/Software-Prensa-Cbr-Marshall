# -------------------------------------------------------------------
# PosicionandoObjetos wplace.py
# @author: Nivaldo Mattos
# @email:  ulabchannel@gmail.com
# @Data:   26/07/2020

# Coloque essas linhas no seu código:
'''
# Comandos do mouse para o posicionador de Widgets
Master.bind('<Button-1>', lambda e: ulwplace1.m_btn1(e, Master))
Master.bind('<Button-3>', lambda e: ulwplace1.m_btn3(e, Master))
Master.bind('<ButtonRelease-1>', lambda e: ulwplace1.m_btn1_release(e, Master))
'''
# -------------------------------------------------------------------
import os

xOld = 0
yOld = 0
ClickState = 0


def copystr(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)


def m_btn1(event, Master):
    global xOld, yOld
    xOld = event.x
    yOld = event.y
    Master.title("ulWplace1: Passo 2:    Arraste até a pos 'Inf.Direita'")


def m_btn1_release(event, Master):
    global xOld, yOld
    my_width = str(event.x - xOld)
    my_height = str(event.y - yOld)
    str1 = "place(width=" + my_width
    str2 = ", height=" + my_height
    str3 = ", x=" + str(xOld)
    str4 = ", y=" + str(yOld) + ")"
    copystr(str1 + str2 + str3 + str4)
    print("Salvo na área de transferência!")
    Master.title("ulWplace1: Passo 1:    Clique na posição 'Sup.Esq'")


def m_btn3(event, Master):
    print('Salvo na área de transferência!')
    copystr(Master.geometry())
    #copystr('.geometry("' + Master.geometry() + '")')

# -------------------------------------------------------------------
# E.O.F
# -------------------------------------------------------------------
