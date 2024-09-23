import tkinter as tk
from tkinter import filedialog
import os

import ttkbootstrap as ttk
# IMPORTANTE! pip install ttkbootstrap, better than tkinter
import mysql.connector
# IMPORTANTE! pip install mysql-connector-python


def setWindowSize(dimensions):
    x = y = 0
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 400) // 2

    window.geometry(f'{dimensions}+{x}+{y}')

def destroy_widgets(window):
    for widget in window.winfo_children():
        widget.destroy()

def cadastro(window):
    destroy_widgets(window)
    
    box = ttk.Frame(window)
    button_send_file = ttk.Button(box, text="Enviar foto", width=20, command=lambda: cadastrar_foto())

    box.pack()
    button_send_file.pack(pady=(80,0))

def cadastrar_foto():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    filename = os.path.basename(filepath)
    file_extension = os.path.splitext(filename)[1]

    if (file_extension != ".jpg") and (file_extension != ".jpeg") and (file_extension != ".png"):
        print('ATENÇÃO!')
        print('As extensões de foto aceitáveis são: jpg, jpeg e png')
    else: 
        SAVE_FOLDER = os.path.dirname(os.path.abspath(__file__)) #Pega o path do diretorio atual
        pasta_arquivos = os.path.join(SAVE_FOLDER, f'imagens_de_face_usuario').replace('\\\\','\\')
        if not os.path.exists(pasta_arquivos):
            os.makedirs(pasta_arquivos)

        id_new_user = 1
        pasta_arquivos_usuario = os.path.join(pasta_arquivos,str(id_new_user))
        if not os.path.exists(pasta_arquivos_usuario):
            os.makedirs(pasta_arquivos_usuario)

def criar_conexão_com_MYSQL():
    mydb = mysql.connector.connect( 
    host="localhost", # Por favor, adapte para seu MYSQL
    user="root", # Por favor, adapte para seu MYSQL
    password="", # Por favor, adapte para seu MYSQL
    database="face_recognition" # Por favor, adapte para seu MYSQL
    )

    mycursor = mydb.cursor()


criar_conexão_com_MYSQL() # Por favor, adapte para seu MYSQL

window = ttk.Window()
setWindowSize('300x200')

box = ttk.Frame(window)
button_register = ttk.Button(box, text="Cadastrar", width=20, command=lambda: cadastro(window))

box.pack()
button_register.pack(pady=(80,0))

window.mainloop()