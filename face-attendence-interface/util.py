import os
import pickle
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import face_recognition

def get_img_label(master):
    label = ctk.CTkLabel(master=master)  # Não defina texto aqui
    label.pack()  
    return label

def msg_box(title, description):
    messagebox.showinfo(title, description)

#proccura dentro do banco, algum match de face_encodings baseado na imagem recebida como parametro
def recognize(img, db_path):

    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found'
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))

    match = False
    j = 0
    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])

        file = open(path_, 'rb')
        embeddings = pickle.load(file)

        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]
        j += 1

    if match:
        return db_dir[j - 1][:-7]
    else:
        return 'unknown_person'

