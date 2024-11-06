import os
import re
import cv2
import pickle
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import util
import face_recognition
import model
import numpy as np
# - os: para manipulação de diretórios e arquivos.
# - re: para operações com expressões regulares (validação de e-mail).
# - cv2: para captura de vídeo e manipulação de imagens.
# - pickle: para serialização de dados.
# - customtkinter: para a criação de interfaces gráficas modernas.
# - messagebox do tkinter: para exibir mensagens de diálogo.
# - PIL (Python Imaging Library): para manipulação de imagens.
# - util: um módulo personalizado com funções auxiliares.
# - face_recognition: biblioteca para reconhecimento facial.
# - model: módulo personalizado para interagir com o banco de dados.
# - numpy: para operações com arrays numéricos.

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
        self.webcam_label.pack(side='top', fill='both', expand=True)  
        self.webcam_label.configure(text="")
        # Adicionar a captura da webcam
        self.add_webcam(self.webcam_label)

        # Criar um frame para os widgets de login à direita
        self.login_frame = ctk.CTkFrame(master=self.janela, width=600, height=800)  # Ajuste conforme necessário
        self.login_frame.pack(side='right', fill='both', expand=True)  # Fica à direita

        # Inicializar a tela de login
        self.tela_login()
        #busca o diretório pra salvar as imagens e caso não esteja criado, cria um
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.janela.mainloop()
        
    #adiciona a captura de webcam
    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()
        
    #define o comportamento da webcam
    def process_webcam(self):
        ret, frame = self.cap.read()
        if ret:
            img_ = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.most_recent_capture_pil = Image.fromarray(img_)
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            self._label.imgtk = imgtk
            self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)
        
    #define o tema do programa para "dark"
    def tema(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
    #cria a janela principal
    def tela(self):
        self.janela.geometry("1000x800")
        self.janela.title("Sistema de Login")
        self.janela.resizable(False, False)

        # Carregar a imagem PNG e definir como ícone
        icon_image = Image.open("/home/lcavalhero/projects/biometria/face-attendance-system/face-attendence-interface/icons/LogoIcon.png")
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.janela.iconphoto(True, icon_photo)
        
    #cria a janela de login
    def tela_login(self):
        label_tt = ctk.CTkLabel(master=self.login_frame, text="Realize a sua autenticação", font=("Roboto", 20), text_color="#00B0F0")
        label_tt.pack(side='top', pady=(10, 20))  

        # Frame (caixa onde o login vai estar localizado)
        login_container = ctk.CTkFrame(master=self.login_frame, width=350, height=394)
        login_container.pack(pady=100)

        # Frame widgets
        label = ctk.CTkLabel(master=login_container, text="Sistema de Login", font=("Arial", 20))
        label.pack(pady=(15, 10))  

        # Caixa de input para o login
        self.user_entry = ctk.CTkEntry(master=login_container, placeholder_text="E-mail Cadastrado", width=300, font=("Roboto", 14))
        self.user_entry.pack(pady=(10, 10))  
        self.user_label = ctk.CTkLabel(master=login_container, text="E-mail Cadastrado", font=("Roboto", 12))
        self.user_label.pack(pady=(0, 5))  

        # Caixa do input para a senha
        self.password_entry = ctk.CTkEntry(master=login_container, placeholder_text="Senha do usuário", width=300, font=("Roboto", 14), show="*")
        self.password_entry.pack(pady=(10, 10))  
        self.password_label = ctk.CTkLabel(master=login_container, text="Senha", font=("Roboto", 12))
        self.password_label.pack(pady=(0, 5)) 

        # Função para mostrar/ocultar senha
        def toggle_password_visibility():
            current_show = self.password_entry.cget('show')
            if current_show == '*':
                self.password_entry.configure(show='')
            else:
                self.password_entry.configure(show='*')

        checkbox = ctk.CTkCheckBox(master=login_container, text="Mostrar Senha", font=("Roboto", 12), command=toggle_password_visibility)
        checkbox.pack(pady=(5, 10)) 

        login_button = ctk.CTkButton(master=login_container, text="Entrar", font=("Roboto", 14), width=300, height=14, command=self.validate_login)
        login_button.pack(pady=(5, 10)) 

        register_span = ctk.CTkLabel(master=login_container, text="Ainda não possui uma conta?", font=("Roboto", 10))
        register_span.pack(pady=(10, 5))  

        self.register_button = ctk.CTkButton(master=login_container, text="Cadastre-se", font=("Roboto", 11), width=150, height=8, fg_color="green", hover_color="#2D9334", command=self.tela_register)
        self.register_button.pack(pady=(5, 10))  
        
    #cria a tela de registro
    def tela_register(self):
        # Remover o frame de login
        for widget in self.login_frame.winfo_children():
            widget.pack_forget()  # Limpar todos os widgets do frame de login

        # Criando a tela de registro
        self.register_frame = ctk.CTkFrame(master=self.login_frame, width=350, height=394)
        self.register_frame.pack(pady=160) 

        label = ctk.CTkLabel(master=self.register_frame, text="Cadastre-se", font=("Arial", 20))
        label.pack(pady=(15, 10))  

        span = ctk.CTkLabel(master=self.register_frame, text="Preencha os campos abaixo para se cadastrar", font=("Roboto", 12), text_color="gray")
        span.pack(pady=(0, 10))  

        self.email_entry = ctk.CTkEntry(master=self.register_frame, placeholder_text="E-mail", width=300, font=("Roboto", 14))
        self.email_entry.pack(pady=(10, 10))  

        self.user_entry = ctk.CTkEntry(master=self.register_frame, placeholder_text="Nome de usuário", width=300, font=("Roboto", 14))
        self.user_entry.pack(pady=(10, 10))  

        self.password_entry = ctk.CTkEntry(master=self.register_frame, placeholder_text="Escolha uma senha", width=300, font=("Roboto", 14), show="*")
        self.password_entry.pack(pady=(10, 10))  

        self.confirm_password_entry = ctk.CTkEntry(master=self.register_frame, placeholder_text="Confirme sua senha", width=300, font=("Roboto", 14), show="*")
        self.confirm_password_entry.pack(pady=(10, 10))  

        self.register_checkbox = ctk.CTkCheckBox(master=self.register_frame, text="Aceitar Termos e Políticas", font=("Roboto", 12))
        self.register_checkbox.pack(pady=(5, 10))  

        self.register_button = ctk.CTkButton(master=self.register_frame, text="Registrar", font=("Roboto", 14), command=self.validate_register)
        self.register_button.pack(pady=(5, 10))  
        
        self.back_button = ctk.CTkButton(master=self.register_frame, text="Voltar", font=("Roboto", 14), width=145, height=14, fg_color="red", hover_color="#2D9334",command=self.back)
        self.back_button.pack(pady=(5, 10))
        
    #define a função do botão "camcelar" e "voltar"
    def back(self):
        #remover o frame de registro
        self.register_frame.pack_forget()
        #recriar a tela de login
        self.tela_login()
        
    #valida o login baseado nos dados armazenados no bd usando o "email" inserido como parâmetro
    def validate_login(self):
        global user_data
        user = model.userDAO()
        email = str(self.user_entry.get())
        password = str(self.password_entry.get())

        # Regex para validar o e-mail
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        user_data = user.get_user_info_based_on_email(email) # Dados do usuário recebido pelo BD
        
        if not email.strip() or not password.strip():
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        elif not re.match(email_regex, email):
            messagebox.showerror("Erro", "E-mail inválido")
        elif not user_data:
            messagebox.showerror("Erro", "Não há cadastro com esse email")
        elif not user.check_password(password, user_data[5]):
            messagebox.showerror("Erro", "Senha incorreta!")
        else:
            # Continue to login recognition
            self.open_webcam_capture_login()
            
    #abre a janela para reconhecimento facial do login
    def open_webcam_capture_login(self):
        # Criar uma nova janela para a captura da webcam
        self.capture_window = ctk.CTkToplevel(self.janela)
        self.capture_window.title("Captura de Webcam")
        self.capture_window.geometry("700x600")

        # Criar um frame para a captura
        self.capture_frame = ctk.CTkFrame(master=self.capture_window, width=700, height=600)
        self.capture_frame.pack()

        # Adicionar o label da webcam
        self.capture_label = util.get_img_label(self.capture_frame)
        self.capture_label.pack()  

        self.add_img_to_label(self.capture_label)

        # Botões para aceitar e cancelar
        self.accept_button = ctk.CTkButton(master=self.capture_window, text="Login", command=self.login_recognition)
        self.accept_button.pack(pady=(10, 5))  

        self.cancel_button = ctk.CTkButton(master=self.capture_window, text="Cancelar", command=self.cancel_capture)
        self.cancel_button.pack(pady=(5, 10))  
        
    #realiza o reconhecimento facial para login
    def login_recognition(self):
        # Converte a imagem capturada da webcam em array para o reconhecimento
        face_image = np.array(self.most_recent_capture_pil)
        
        # Chama a função de reconhecimento facial
        name = util.recognize(face_image, self.db_dir)
        
        # Tratamento de retorno para casos específicos
        if name == 'no_persons_found':
            util.msg_box('Ops...', 'Nenhum rosto detectado na imagem. Tente novamente!')
            return
        elif name == 'unknown_person':
            util.msg_box('Ops...', 'Usuário não reconhecido. Cadastre-se ou tente novamente!')
            return
        if (user_data[6]=='usuário'):
        # Se o nome for reconhecido, exibe a mensagem de boas-vindas
            util.msg_box('Bem-vindo!', f'Olá, {user_data[1]}!')
        else:
            util.msg_box('Bem-vindo!', f'Olá, {user_data[1]}, ({user_data[6]})!')


    #valida os dados para prosseguir para o registro de novo usuário
    def validate_register(self):
        global new_user,email,user,user_password
        new_user = model.userDAO()
        email = str(self.email_entry.get())
        user = str(self.user_entry.get())
        password = str(self.password_entry.get())

        # Regex para validar o e-mail
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Regex para validar a senha
        password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
        
        confirm_password = self.confirm_password_entry.get()
        if not email.strip() or not user.strip() or not password.strip() or not confirm_password.strip():
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        elif not re.match(email_regex, email):
            messagebox.showerror("Erro", "E-mail inválido")
        elif not re.match(password_regex, password):
            messagebox.showerror("Erro", "A senha deve ter no mínimo 8 caracteres, incluindo pelo menos um número, uma letra e um caractere especial")
        elif password != confirm_password:
            messagebox.showerror("Erro", "As senhas devem ser iguais")
        elif not self.register_checkbox.get():
            messagebox.showerror("Erro", "Você deve aceitar os termos e políticas")
        elif new_user.get_user_info_based_on_email(email):
            messagebox.showerror("Erro", "Email já cadastrado!")
        else:
            
            user_password = new_user.generate_password(password)
            # Se todas as validações estiverem corretas, abrir a tela de captura
            self.open_webcam_capture()

    #função que adiciona a última imagem retirada da webcam para a label solicitada
    def add_img_to_label(self, label):
        if self.most_recent_capture_pil:
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            label.imgtk = imgtk  # Guarde a referência da imagem
            label.configure(image=imgtk, text="")

    #cria a janela de registro de biometria facial
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
        self.capture_label.pack()  

        self.add_img_to_label(self.capture_label)

        # Botões para aceitar e cancelar
        self.accept_button = ctk.CTkButton(master=self.capture_window, text="Aceitar", command=self.register_new_user_face)
        self.accept_button.pack(pady=(10, 5))  

        self.cancel_button = ctk.CTkButton(master=self.capture_window, text="Cancelar", command=self.cancel_capture)
        self.cancel_button.pack(pady=(5, 10))  

    #salva o registro da biometria facial após verificação
    def register_new_user_face(self):
        # Converte a imagem PIL mais recente em numpy.ndarray
        face_image = np.array(self.most_recent_capture_pil)
        
        # Obtém as codificações faciais
        new_user_encodings = face_recognition.face_encodings(face_image)

        if not new_user_encodings:
            messagebox.showinfo('Erro!', 'Não foi possível detectar um rosto. Tente novamente.')
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
            messagebox.showinfo('Erro!', 'Usuário já cadastrado. Tente registrar um rosto diferente.')
            return

        # Salva a nova codificação facial
        user_image_name = new_user.save_bd_new_user_and_return_id_of_user(user, email,user_password)
        with open(os.path.join(self.db_dir, f'{user_image_name}.pickle'), 'wb') as file:
            pickle.dump(new_user_encoding, file)

        messagebox.showinfo("Sucesso", "Usuario cadastrado com sucesso")
        self.capture_window.destroy()  # Fechar a janela de captura
        
    def cancel_capture(self):
        self.capture_window.destroy()  # Destruir a janela de captura
    
if __name__ == "__main__":
    app = Application()
