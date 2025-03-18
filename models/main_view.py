import customtkinter as ctk
from models.login_model import LoginModel
from models.register_model import RegisterModel

class MainView(ctk.CTk):
    def __init__(self, database):
        super().__init__()
        self.login_model = LoginModel(database, self)
        self.register_model = RegisterModel(database, self)
        self.title("Budget Buddy")
        self.geometry("350x600")  # width x height
        self.login_model.create_login_screen()

    def clear_screen(self):
        """remove all ctkinter widget from the screen (empty the window)"""
        for widget in self.winfo_children():
            widget.destroy()

    def create_main_screen(self):
        self.clear_screen()
        # ...existing code for main screen...