import customtkinter as ctk
from tkinter import messagebox
import bcrypt
from mysql.connector import Error

class LoginModel:
    def __init__(self, database, main_view):
        self.database = database
        self.main_view = main_view

    def create_login_screen(self):
        self.main_view.clear_screen()  # to improve
        self.login_frame = ctk.CTkFrame(self.main_view)
        self.login_frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.email_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Email")
        self.email_entry.pack(pady=12, padx=10)
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=12, padx=10)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=12, padx=10)

        self.register_button = ctk.CTkButton(self.login_frame, text="Register", command=self.main_view.register_model.create_registration_screen)
        self.register_button.pack(pady=12, padx=10)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if self.verify_user(email, password):
            messagebox.showinfo("Login", "Login successful!")
            self.main_view.create_main_screen()
        else:
            messagebox.showerror("Login", "Invalid email or password")

    def verify_user(self, email, password):
        """
        Get client from database using entered email and password (encrypt entered password and compare with encrypted stored password).
        :return: True if such client is in database
        :return: False otherwise
        """
        try:
            with self.database.connect("budget_buddy") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT password FROM client WHERE email = %s", (email,))
                result = cursor.fetchone()
                if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                    return True
        except Error as e:
            print(f"Error verifying user: {e}")
        return False
