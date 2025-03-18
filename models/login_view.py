import customtkinter as ctk
from models.login_model import LoginModel

class LoginView(ctk.CTkFrame):
    def __init__(self, main_view):
        super().__init__(main_view)
        self.main_view = main_view
        self.login_model = LoginModel(main_view.database, main_view)
        self.draw_login_screen()

    def create_login_screen(self):
        self.main_view.clear_screen()
        self.login_frame = ctk.CTkFrame(self.main_view)
        self.login_frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.email_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Email")
        self.email_entry.pack(pady=12, padx=10)
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=12, padx=10)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login_model.login)
        self.login_button.pack(pady=12, padx=10)

        self.register_button = ctk.CTkButton(self.login_frame, text="Register", command=self.main_view.register_view.draw_registration_screen)
        self.register_button.pack(pady=12, padx=10)

