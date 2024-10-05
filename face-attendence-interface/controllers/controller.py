# Handle interactions between view and controller

class Controller:
    def __init__(self, view):
        self.view = view


    def show_auth(self):
        self.view.destroy_widgets()
        self.view.create_auth_screen(self.login, self.register)

    def login(self):
        self.view.destroy_widgets()
        self.view.create_login_screen(self.show_auth)

    def register(self):
        self.view.destroy_widgets()
        self.view.create_register_screen(self.show_auth)


