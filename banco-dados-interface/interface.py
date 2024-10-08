import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import re
import model


janela = ctk.CTk()

class Application():
    def __init__(self):
        self.janela=janela
        self.tema() 
        self.tela()
        self.tela_login()
        janela.mainloop()


    def tema(self):
        #configuração do tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

    def tela(self):
        # dimenções da janela
        largura_janela = 700
        altura_janela = 400
        
        # Obter largura e altura da tela do usuário
        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()
        
        # Calcular a posição x e y para centralizar a janela
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        
        # Configurar a geometria da janela e centralizar
        self.janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        janela.title("Sistema de Login")
        
        janela.resizable(False, False)

    def tela_login(self):
        #configurações da imagem
        original_image = Image.open("./icons/main-image3.png")
        resized_image = original_image.resize((350, 320))  # Defina o tamanho desejado
        img = ImageTk.PhotoImage(resized_image)
        #trabalhando a imagem ( posicionamento )
        label_img = ctk.CTkButton(master=janela, image=img, text=None, hover=None, fg_color=None)
        label_img.place(x=28, y=100)

        label_tt = ctk.CTkLabel(master=janela, text="Realize a sua autenticação", font=("Roboto", 20), text_color="#00B0F0")
        label_tt.place(x=40, y=45)

        #frame (caixa onde o login vai estar localizado)
        login_frame = ctk.CTkFrame(master=janela, width=350, height=400)
        login_frame.pack(side=RIGHT)

        #frame widgets
        label = ctk.CTkLabel(master=login_frame, text="Sistema de Login", font=("Arial", 20))
        label.place(x=25, y=45)
        #caixa de input para o login
        self.user_entry = ctk.CTkEntry(master=login_frame, placeholder_text="E-mail Cadastrado", width=300, font=("Roboto", 14))
        self.user_entry.place(x=25, y=145)
        self.user_label = ctk.CTkLabel(master=login_frame, text="E-mail Cadastrado", font=("Roboto", 12)).place(x=30, y=115)
        #caixa do input para a senha
        self.password_entry = ctk.CTkEntry(master=login_frame, placeholder_text="Senha do usuario", width=300, font=("Roboto", 14), show="*")
        self.password_entry.place(x=25, y=205)
        self.password_label = ctk.CTkLabel(master=login_frame, text="Senha", font=("Roboto", 12)).place(x=30, y=175)

        # Função para mostrar/ocultar senha
        def toggle_password_visibility():
            current_show = self.password_entry.cget('show')
            print(f"Valor atual de 'show': {current_show}")
            if current_show == '*':
                self.password_entry.configure(show='')
            else:
                self.password_entry.configure(show='*')

        checkbox = ctk.CTkCheckBox(master=login_frame, text="Mostrar Senha", font=("Roboto", 12), command=toggle_password_visibility).place(x=30, y=245)

        login_button = ctk.CTkButton(master=login_frame, text="Entrar", font=("Roboto", 14), width=300, height=14, command=self.validate_login).place(x=25, y=290)
        
        register_span = ctk.CTkLabel(master=login_frame, text="Ainda não possui uma conta?", font=("Roboto", 10)).place(x=25, y=326)

        def tela_register():
            #remover o frame de login
            login_frame.pack_forget()

            #Criando a tela de registro
            self.register_frame = ctk.CTkFrame(master=janela, width=350, height=400)
            self.register_frame.pack(side=RIGHT)

            label = ctk.CTkLabel(master=self.register_frame, text="Cadastre-se", font=("Arial", 20))
            label.place(x=25, y=35)

            span = ctk.CTkLabel(master=self.register_frame, text="Preencha os campos abaixo para se cadastrar", font=("Roboto", 12), text_color="gray").place(x=25, y=65)

            self.email_entry = ctk.CTkEntry(master=self.register_frame, placeholder_text="E-mail", width=300, font=("Roboto", 14))
            self.email_entry.place(x=25, y=95)
            
            self.user_entry = ctk.CTkEntry(master=self.register_frame, placeholder_text="Nome de usuario", width=300, font=("Roboto", 14))
            self.user_entry.place(x=25, y=135)

            self.password_entry = ctk.CTkEntry(master=self.register_frame, placeholder_text="Escoha uma senha", width=300, font=("Roboto", 14), show="*")
            self.password_entry.place(x=25, y=175)

            self.confirm_password_entry = ctk.CTkEntry(master=self.register_frame, placeholder_text="Confirme sua senha", width=300, font=("Roboto", 14), show="*")
            self.confirm_password_entry.place(x=25, y=215)

            self.register_auth_button = ctk.CTkButton(master=self.register_frame, text="Registrar Biometria Facial", font=("Roboto", 14), width=300, height=14)
            self.register_auth_button.place(x=25, y=255)

            self.register_checkbox = ctk.CTkCheckBox(master=self.register_frame, text="Aceitar Termos e Politicas ", font=("Roboto", 12))
            self.register_checkbox.place(x=30, y=290)

            self.register_button = ctk.CTkButton(master=self.register_frame, text="Registrar", font=("Roboto", 14), width=145, height=14, fg_color="#038238", hover_color="#02632b", command=self.validate_cadastro)
            self.register_button.place(x=175, y=325)
 
            self.back_button = ctk.CTkButton(master=self.register_frame, text="Voltar", font=("Roboto", 14), width=145, height=14, fg_color="#d91204", hover_color="#b50d02",command=self.back)
            self.back_button.place(x=25, y=325)

            
        self.register_button = ctk.CTkButton(master=login_frame, text="Cadastre-se", font=("Roboto", 11), width=150, height=8,
        fg_color="#038238", hover_color="#02632b", command=tela_register)
        self.register_button.place(x=180, y=328)

    def back(self):
                #remover o frame de registro
                self.register_frame.pack_forget()
                #recriar a tela de login
                self.tela_login()

    def validate_login(self):
        global user
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
            # Continue with login process
            messagebox.showinfo("Sucesso", "Usuario logado com sucesso")
            pass
    
    def validate_cadastro(self):
        
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
            messagebox.showinfo("Sucesso", "Usuario cadastrado com sucesso")
            
            user_password = new_user.generate_password(password)
            user_image_name = new_user.save_bd_new_user_and_return_id_of_user(user, email, user_password)
            print("Imagem pode ser salva com o nome:",user_image_name)
            pass


        
Application()