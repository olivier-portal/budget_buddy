import customtkinter as ctk
from tkinter import messagebox
import re
import bcrypt
from mysql.connector import Error

class RegisterModel:
    def __init__(self, database, main_view):
        self.database = database
        self.main_view = main_view

    def create_registration_screen(self):
        self.main_view.clear_screen()
        self.register_frame = ctk.CTkFrame(self.main_view)
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

        self.back_to_login_button = ctk.CTkButton(self.register_frame, text="Back to Login", command=self.main_view.login_model.create_login_screen)
        self.back_to_login_button.pack(pady=12, padx=10)

    def validate_password(self, password):
        """use regex (by importing .re) to verify password meets requirements"""
        if (len(password) >= 10 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"[0-9]", password) and
            re.search(r"[\W_]", password)):
            return True
        return False

    def register(self):
        """get user input from registration screen, verify password complexity and add user to database"""
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not self.validate_password(password):
            messagebox.showerror("Registration", "Password must contain at least one uppercase letter, one lowercase letter, one special character, one digit, and be at least ten characters long.")
            return

        if self.add_user(last_name, first_name, email, password):
            messagebox.showinfo("Registration", "Registration successful!")
            self.main_view.login_model.create_login_screen()
        else:
            messagebox.showerror("Registration", "Registration failed. Email may already be in use.")

    def add_user(self, last_name, first_name, email, password):
        """
        Hash the password and add the user to the database.
        :return: True if the user is added to the database
        :return: False otherwise
        """
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            with self.database.connect("budget_buddy") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                       INSERT INTO client (last_name, first_name, email, password)
                       VALUES (%s, %s, %s, %s)
                   """, (last_name, first_name, email, hashed_password))
                conn.commit()
                return True
        except Error as e:
            print(f"Error adding user: {e}")
            return False
