import customtkinter as ctk
from tkinter import messagebox

class HomeFrame(ctk.CTkFrame):
    def __init__(self, database, parent, controller):
        super().__init__(parent)
        
        self.controller = controller
        
        self.database = database
        
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.grid(row=0, column=0, sticky="nsew", padx=50)
        
        self.login_frame.grid_rowconfigure(0, weight=1)
        self.login_frame.grid_columnconfigure(0, weight=1)

        self.email_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Email")
        self.email_entry.pack(pady=12, padx=10)
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=12, padx=10)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=12, padx=10)

        self.register_button = ctk.CTkButton(self.login_frame, text="Register", command=lambda: controller.show_frame("RegistrationFrame"))
        self.register_button.pack(pady=12, padx=10)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if self.database.verify_user(email, password):
            messagebox.showinfo("Login", "Login successful!")
            self.create_main_screen()
        else:
            messagebox.showerror("Login", "Invalid email or password")
    