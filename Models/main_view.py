import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import re

class MainView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Budget Buddy")
        self.geometry("350x600")  # width x height
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.email_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Email")
        self.email_entry.pack(pady=12, padx=10)
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=12, padx=10)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=12, padx=10)

        self.register_button = ctk.CTkButton(self.login_frame, text="Register", command=self.create_registration_screen)
        self.register_button.pack(pady=12, padx=10)

    def create_registration_screen(self):
        self.clear_screen()
        self.register_frame = ctk.CTkFrame(self)
        self.register_frame.pack(pady=20, padx=60, fill="both", expand=True)

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

        self.back_to_login_button = ctk.CTkButton(self.register_frame, text="Back to Login", command=self.create_login_screen)
        self.back_to_login_button.pack(pady=12, padx=10)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if self.controller.verify_user(email, password):
            messagebox.showinfo("Login", "Login successful!")
            self.create_main_screen()
        else:
            messagebox.showerror("Login", "Invalid email or password")

    def register(self):
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not self.validate_password(password):
            messagebox.showerror("Registration", "Password must contain at least one uppercase letter, one lowercase letter, one special character, one digit, and be at least ten characters long.")
            return

        if self.controller.add_user(last_name, first_name, email, password):
            messagebox.showinfo("Registration", "Registration successful!")
            self.create_login_screen()
        else:
            messagebox.showerror("Registration", "Registration failed. Email may already be in use.")

    def validate_password(self, password):
        if (len(password) >= 10 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"[0-9]", password) and
            re.search(r"[\W_]", password)):
            return True
        return False

    def create_main_screen(self):
        self.clear_screen()
        # ...existing code for main screen...