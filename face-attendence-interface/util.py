import customtkinter as ctk
from PIL import Image, ImageTk

def get_img_label(master):
    label = ctk.CTkLabel(master=master)  # Não defina texto aqui
    label.pack()  # Use pack ou grid conforme necessário
    return label