import tkinter as tk
from tkinter import filedialog
import os

import ttkbootstrap as ttk
# IMPORTANTE! pip install ttkbootstrap, better than tkinter
import mysql.connector
# IMPORTANTE! pip install mysql-connector-python


def criar_conexão_com_MYSQL():
    mydb = mysql.connector.connect( 
    host="localhost", # Por favor, adapte para seu MYSQL
    user="root", # Por favor, adapte para seu MYSQL
    password="", # Por favor, adapte para seu MYSQL
    database="face_recognition" # Por favor, adapte para seu MYSQL
    )

    mycursor = mydb.cursor()
    return mydb, mycursor

def setWindowSize(window, dimensions):
    x = y = 0
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 400) // 2

    window.geometry(f'{dimensions}+{x}+{y}')

def destroy_widgets(window):
    for widget in window.winfo_children():
        widget.destroy()

def cadastro(window, failure_name = False):
    destroy_widgets(window)
    
    if failure_name: # se o usuario escolher nome invalido, a gente escolhe as regras de restrição, coloquei em relação tamanho de VARCHAR(100) do sql
        erro_window = ttk.Window()
        setWindowSize(window, '300x200')
        
        label = ttk.Label(window, text="No máximo 100 caracteres para o nome!")
        label.pack()
        erro_window.mainloop()
    else:
        box = ttk.Frame(window)
        label_nome = ttk.Label(box, text="Seu nome: ")
        user_name = ttk.Entry(box)

        box2 = ttk.Frame(window)
        button_send_file = ttk.Button(box2, text="Enviar foto", width=20, command=lambda: cadastrar_foto(window, user_name.get()))

        box.pack()
        label_nome.pack()
        user_name.pack()

        box2.pack()
        button_send_file.pack(pady=(20,0))

def cadastrar_foto(window, user_name):
    if (not user_name) or (len(user_name) > 99): # Se não colocou vazio, da para encher de restrição aqui se quiser
        cadastro(window, True)
    else:
        filepath = filedialog.askopenfilename() # Abrir a janela de escolher arquivo
        if not filepath: # se for vazio ele não faz nada
            return
        filename = os.path.basename(filepath)
        file_extension = os.path.splitext(filename)[1]

        if (file_extension != ".jpg") and (file_extension != ".jpeg") and (file_extension != ".png"):
            print('ATENÇÃO!')
            print('As extensões de foto aceitáveis são: jpg, jpeg e png')
        else: 
            # Processo de inserção de novo usuário no mysql (id + nome)
            sql = "INSERT INTO users (nome) VALUES (%s)"
            val = (str(user_name),)
            sql_exec.execute(sql, val)
            mydb.commit() 

            SAVE_FOLDER = os.path.dirname(os.path.abspath(__file__)) # Pega o path do diretorio atual
            pasta_arquivos = os.path.join(SAVE_FOLDER, f'imagens_de_face_usuario').replace('\\\\','\\')
            if not os.path.exists(pasta_arquivos):
                os.makedirs(pasta_arquivos)

            id_new_user = sql_exec.lastrowid # Pega o id no sql, conforme a linha que adicionamos do novo usuario
            path_img_usuario = os.path.join(pasta_arquivos, str(id_new_user)+file_extension)
            try:
                with open(filepath, 'rb') as source_file:
                    with open(path_img_usuario, 'wb') as dest_file:
                        dest_file.write(source_file.read())
            except Exception as e:
                print(e)


mydb, sql_exec = criar_conexão_com_MYSQL() # Por favor, adapte para seu MYSQL

window = ttk.Window() # cria janela
setWindowSize(window, '300x200') # seta dimensoes

box = ttk.Frame(window)
button_register = ttk.Button(box, text="Cadastrar", width=20, command=lambda: cadastro(window))

box.pack()
button_register.pack(pady=(80,0))

window.mainloop()