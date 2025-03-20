import customtkinter as ctk
from tkinter import messagebox
import re

from frames.login_frame import *

class RegistrationFrame(ctk.CTkFrame):
    def __init__(self, database, parent, controller):
        super().__init__(parent)
        
        self.controller = controller
        
        self.database = database
        
        self.register_frame = ctk.CTkFrame(self)
        self.register_frame.pack(fill="both", expand=True)

        self.last_name_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Last Name")
        self.last_name_entry.pack(pady=12, padx=10)
        self.first_name_entry = ctk.CTkEntry(self.register_frame, placeholder_text="First Name")
        self.first_name_entry.pack(pady=12, padx=10)
        self.email_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Email")
        self.email_entry.pack(pady=12, padx=10)
        self.password_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=12, padx=10)

        self.register_button = ctk.CTkButton(self.register_frame, text="Register", command=self.register)
        self.register_button.pack(pady=12, padx=10)

        self.back_to_login_button = ctk.CTkButton(self.register_frame, text="Back to Login", command=lambda: controller.show_frame("LoginFrame"))
        self.back_to_login_button.pack(pady=12, padx=10)

    def register(self):
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not self.validate_password(password):
            messagebox.showerror("Registration", "Password must contain at least one uppercase letter, one lowercase letter, one special character, one digit, and be at least ten characters long.")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Registration", "Your email adress must be under the format name@example.com")
            return

        if self.database.add_user(last_name, first_name, email, password):
            messagebox.showinfo("Registration", "Registration successful!")
            self.create_login_screen()
        else:
            messagebox.showerror("Registration", "Registration failed. Email may already be in use.")

    def validate_password(self, password):
        password_format = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{10,}$'
        return bool(re.match(password_format, password))

    def validate_email(self, email):
        email_format = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_format, email))