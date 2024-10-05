import os
import re
import cv2
import pickle
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import util
import face_recognition

class Application:
    def __init__(self):
        self.janela = ctk.CTk()
        self.tema()
        self.tela()

        # Criar um frame para a webcam à esquerda
        self.webcam_frame = ctk.CTkFrame(master=self.janela, width=400, height=800)  # Defina a largura que desejar
        self.webcam_frame.pack(side='left', fill='both', expand=False)  # Fica à esquerda

        # Adicionar a label da webcam ao frame da webcam
        self.webcam_label = util.get_img_label(self.webcam_frame)
        self.webcam_label.pack(side='top', fill='both', expand=True)  # Use pack aqui
        self.webcam_label.configure(text="")
        # Adicionar a captura da webcam
        self.add_webcam(self.webcam_label)

        # Criar um frame para os widgets de login à direita
        self.login_frame = ctk.CTkFrame(master=self.janela, width=600, height=800)  # Ajuste conforme necessário
        self.login_frame.pack(side='right', fill='both', expand=True)  # Fica à direita

        # Inicializar a tela de login
        self.tela_login()

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.janela.mainloop()

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        if ret:
            img_ = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.most_recent_capture_pil = Image.fromarray(img_)
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            self._label.imgtk = imgtk
            self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def tema(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

    def tela(self):
        self.janela.geometry("1000x800")
        self.janela.title("Sistema de Login")
        self.janela.resizable(False, False)

        # Carregar a imagem PNG e definir como ícone
        icon_image = Image.open("/home/lcavalhero/projects/biometria/face-attendance-system/face-attendence-interface/icons/LogoIcon.png")
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.janela.iconphoto(True, icon_photo)

    def tela_login(self):
        label_tt = ctk.CTkLabel(master=self.login_frame, text="Realize a sua autenticação", font=("Roboto", 20), text_color="#00B0F0")
        label_tt.pack(side='top', pady=(10, 20))  # Use pack aqui

        # Frame (caixa onde o login vai estar localizado)
        login_container = ctk.CTkFrame(master=self.login_frame, width=350, height=394)
        login_container.pack(pady=100)# Use pack aqui

        # Frame widgets
        label = ctk.CTkLabel(master=login_container, text="Sistema de Login", font=("Arial", 20))
        label.pack(pady=(15, 10))  # Use pack aqui

        # Caixa de input para o login
        self.user_entry = ctk.CTkEntry(master=login_container, placeholder_text="E-mail Cadastrado", width=300, font=("Roboto", 14))
        self.user_entry.pack(pady=(10, 10))  # Use pack aqui
        self.user_label = ctk.CTkLabel(master=login_container, text="E-mail Cadastrado", font=("Roboto", 12))
        self.user_label.pack(pady=(0, 5))  # Use pack aqui

        # Caixa do input para a senha
        self.password_entry = ctk.CTkEntry(master=login_container, placeholder_text="Senha do usuário", width=300, font=("Roboto", 14), show="*")
        self.password_entry.pack(pady=(10, 10))  # Use pack aqui
        self.password_label = ctk.CTkLabel(master=login_container, text="Senha", font=("Roboto", 12))
        self.password_label.pack(pady=(0, 5))  # Use pack aqui

        # Função para mostrar/ocultar senha
        def toggle_password_visibility():
            current_show = self.password_entry.cget('show')
            if current_show == '*':
                self.password_entry.configure(show='')
            else:
                self.password_entry.configure(show='*')

        checkbox = ctk.CTkCheckBox(master=login_container, text="Mostrar Senha", font=("Roboto", 12), command=toggle_password_visibility)
        checkbox.pack(pady=(5, 10))  # Use pack aqui

        login_button = ctk.CTkButton(master=login_container, text="Entrar", font=("Roboto", 14), width=300, height=14, command=self.validate_login)
        login_button.pack(pady=(5, 10))  # Use pack aqui

        register_span = ctk.CTkLabel(master=login_container, text="Ainda não possui uma conta?", font=("Roboto", 10))
        register_span.pack(pady=(10, 5))  # Use pack aqui

        self.register_button = ctk.CTkButton(master=login_container, text="Cadastre-se", font=("Roboto", 11), width=150, height=8, fg_color="green", hover_color="#2D9334", command=self.tela_register)
        self.register_button.pack(pady=(5, 10))  # Use pack aqui

    def tela_register(self):
        # Remover o frame de login
        for widget in self.login_frame.winfo_children():
            widget.pack_forget()  # Limpar todos os widgets do frame de login

        # Criando a tela de registro
        self.register_frame = ctk.CTkFrame(master=self.login_frame, width=350, height=394)
        self.register_frame.pack(pady=160)  # Use pack aqui

        label = ctk.CTkLabel(master=self.register_frame, text="Cadastre-se", font=("Arial", 20))
        label.pack(pady=(15, 10))  # Use pack aqui

        span = ctk.CTkLabel(master=self.register_frame, text="Preencha os campos abaixo para se cadastrar", font=("Roboto", 12), text_color="gray")
        span.pack(pady=(0, 10))  # Use pack aqui

        self.email_entry = ctk.CTkEntry(master=self.register_frame, placeholder_text="E-mail", width=300, font=("Roboto", 14))
        self.email_entry.pack(pady=(10, 10))  # Use pack aqui

        self.user_entry = ctk.CTkEntry(master=self.register_frame, placeholder_text="Nome de usuário", width=300, font=("Roboto", 14))
        self.user_entry.pack(pady=(10, 10))  # Use pack aqui

        self.password_entry = ctk.CTkEntry(master=self.register_frame, placeholder_text="Escolha uma senha", width=300, font=("Roboto", 14), show="*")
        self.password_entry.pack(pady=(10, 10))  # Use pack aqui

        self.confirm_password_entry = ctk.CTkEntry(master=self.register_frame, placeholder_text="Confirme sua senha", width=300, font=("Roboto", 14), show="*")
        self.confirm_password_entry.pack(pady=(10, 10))  # Use pack aqui

        self.register_checkbox = ctk.CTkCheckBox(master=self.register_frame, text="Aceitar Termos e Políticas", font=("Roboto", 12))
        self.register_checkbox.pack(pady=(5, 10))  # Use pack aqui

        self.register_button = ctk.CTkButton(master=self.register_frame, text="Registrar", font=("Roboto", 14), command=self.validate_register)
        self.register_button.pack(pady=(5, 10))  # Use pack aqui
        
        self.back_button = ctk.CTkButton(master=self.register_frame, text="Voltar", font=("Roboto", 14), width=145, height=14, fg_color="red", hover_color="#2D9334",command=self.back)
        self.back_button.pack(pady=(5, 10))
        
    def back(self):
        #remover o frame de registro
        self.register_frame.pack_forget()
        #recriar a tela de login
        self.tela_login()

    def validate_login(self):
        email = self.user_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            util.msg_box('Erro!', 'Por favor, preencha todos os campos.')
            return

        # Verifique aqui se o login é válido (exemplo, verificando no banco de dados)

        # Se o login for bem-sucedido
        util.msg_box('Sucesso!', 'Login realizado com sucesso!')

    def validate_register(self):
        email = self.email_entry.get()
        username = self.user_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not email or not username or not password or not confirm_password:
            util.msg_box('Erro!', 'Por favor, preencha todos os campos.')
            return

        if password != confirm_password:
            util.msg_box('Erro!', 'As senhas não coincidem.')
            return

        if not self.register_checkbox.get():
            messagebox.showerror("Erro", "Você deve aceitar os termos e políticas")
            return

        # Se todas as validações estiverem corretas, abrir a tela de captura
        self.open_webcam_capture()

    def add_img_to_label(self, label):
        if self.most_recent_capture_pil:
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            label.imgtk = imgtk  # Guarde a referência da imagem
            label.configure(image=imgtk, text="")

    def open_webcam_capture(self):
        # Criar uma nova janela para a captura da webcam
        self.capture_window = ctk.CTkToplevel(self.janela)
        self.capture_window.title("Captura de Webcam")
        self.capture_window.geometry("700x600")

        # Criar um frame para a captura
        self.capture_frame = ctk.CTkFrame(master=self.capture_window, width=700, height=600)
        self.capture_frame.pack()

        # Adicionar o label da webcam
        self.capture_label = util.get_img_label(self.capture_frame)
        self.capture_label.pack()  # Use pack aqui

        self.add_img_to_label(self.capture_label)

        # Botões para aceitar e cancelar
        self.accept_button = ctk.CTkButton(master=self.capture_frame, text="Aceitar", command=self.register_new_user_face)
        self.accept_button.pack(pady=(10, 5))  # Use pack aqui

        self.cancel_button = ctk.CTkButton(master=self.capture_frame, text="Cancelar", command=self.cancel_capture)
        self.cancel_button.pack(pady=(5, 10))  # Use pack aqui

        # Iniciar a captura da webcam
        self.add_webcam(self.capture_label)

    def register_new_user_face(self):
        new_user_encodings = face_recognition.face_encodings(self.register_new_user_capture)

        if not new_user_encodings:
            util.msg_box('Erro!', 'Não foi possível detectar um rosto. Tente novamente.')
            return

        new_user_encoding = new_user_encodings[0]

        # Carregar todas as codificações existentes
        existing_encodings = []
        for filename in os.listdir(self.db_dir):
            if filename.endswith('.pickle'):
                with open(os.path.join(self.db_dir, filename), 'rb') as file:
                    existing_encodings.append(pickle.load(file))

        # Verificar se a nova codificação já existe
        matches = face_recognition.compare_faces(existing_encodings, new_user_encoding)

        if any(matches):
            util.msg_box('Erro!', 'Usuário já cadastrado. Tente registrar um rosto diferente.')
            return

        # Salva a nova codificação facial
        name = self.user_entry.get().strip()  # Obter nome do usuário a partir do campo
        with open(os.path.join(self.db_dir, f'{name}.pickle'), 'wb') as file:
            pickle.dump(new_user_encoding, file)

        util.msg_box('Sucesso!', 'Usuário registrado com sucesso!')
        self.capture_window.destroy()  # Fechar a janela de captura

    def cancel_capture(self):
        # Limpar a captura e liberar a câmera
        if 'cap' in self.__dict__:
            self.cap.release()
            del self.cap
        
        # Destruir a janela de captura
        if hasattr(self, 'capture_window'):
            self.capture_window.destroy()  # Destruir a janela de captura
    
        # Chamar a tela de registro
        self.tela_register()  # Voltar à tela de cadastro



if __name__ == "__main__":
    app = Application()
