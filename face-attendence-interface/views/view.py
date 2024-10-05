# Code Visual, "Front-End"

import tkinter as tk
import ttkbootstrap as ttk

class Interface():

    def __init__(self, titleName):
        self.window = ttk.Window()
        self.window.title(titleName)
        self.setWindowSize('300x127')

        #Creation of styles / Design
        style = ttk.Style()
        style.configure('Back.TButton', background='#f59b25', foreground='#000000', borderwidth=0, padding=[0,8])
        style.map('Back.TButton', background=[('active', '#f5b625')], foreground=[('active', '#000000')])
        

    def start(self): # Window Looping / No error when close the window
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.window.quit())
        self.window.mainloop()


    def setWindowSize(self, dimensions):
        x = y = 0
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 400) // 2

        self.window.geometry(f'{dimensions}+{x}+{y}')

    def destroy_widgets(self):
        for widget in self.window.winfo_children():
            widget.destroy()


    def create_auth_screen(self, login, register):
        box = tk.Frame(self.window)
        login_btn = ttk.Button(box, text='Login', command=login, width=20)
        register_btn = ttk.Button(box, text='Cadastrar', command=register, width=20)

        box.pack()
        login_btn.pack(pady=(27,15))
        register_btn.pack()

    def create_login_screen(self, back):
        self.window.title('Login')
        self.setWindowSize('300x150')

        box = tk.Frame(self.window)
        box2 = tk.Frame(self.window)
        back_box = tk.Frame(self.window)
        email_label = ttk.Label(box, text='Email: ')
        emailInput = ttk.Entry(box)
        auth_button = ttk.Button(box2, text='Fazer Autentificação',width=26)
        back_button = ttk.Button(back_box, text='Voltar', comman=back, style='Back.TButton')

        box.pack(pady=(20,16))
        box2.pack()
        back_box.pack(side='bottom',fill='x')
        email_label.pack(side='left', padx=5)
        emailInput.pack(side='left')
        auth_button.pack()
        back_button.pack(fill='x')
        
        emailInput.focus_set()
        emailInput.bind("<Return>", lambda event: auth_button.invoke())
        
    def create_register_screen(self, back):
        self.window.title('Cadastro')
        self.setWindowSize('300x150')

        box = tk.Frame(self.window)
        box2 = tk.Frame(self.window)
        back_box = tk.Frame(self.window)
        email_label = ttk.Label(box, text='Email: ')
        emailInput = ttk.Entry(box)
        auth_button = ttk.Button(box2, text='Cadastrar Biometria Facial',width=26)
        back_button = ttk.Button(back_box, text='Voltar', comman=back, style='Back.TButton')

        box.pack(pady=(20,16))
        box2.pack()
        back_box.pack(side='bottom',fill='x')
        email_label.pack(side='left', padx=5)
        emailInput.pack(side='left')
        auth_button.pack()
        back_button.pack(fill='x')
        
        emailInput.focus_set()
        emailInput.bind("<Return>", lambda event: auth_button.invoke())
