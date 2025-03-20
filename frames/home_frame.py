import customtkinter as ctk
from tkinter import messagebox

class HomeFrame(ctk.CTkFrame):
    def __init__(self, database, parent, controller):
        super().__init__(parent)
        
        self.controller = controller
        self.database = database
        
        # Force HomeFrame to have white background
        self.configure(fg_color="white")
        
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        
        self.login_frame = ctk.CTkFrame(self, fg_color="white")
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        
        self.login_frame.grid_rowconfigure(0, weight=1)
        self.login_frame.grid_columnconfigure(0, weight=1)
        
        # Create a container inside login_frame to hold widgets
        self.inner_frame = ctk.CTkFrame(self.login_frame, fg_color="white")
        self.inner_frame.pack(expand=True, padx=10, pady=10)

        self.email_entry = ctk.CTkEntry(self.inner_frame, placeholder_text="Email")
        self.email_entry.pack(padx=10, pady=5)
        
        self.password_entry = ctk.CTkEntry(self.inner_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(padx=10, pady=50)

        self.login_button = ctk.CTkButton(self.inner_frame, text="Login", command=self.login)
        self.login_button.pack(padx=10, pady=5)

        self.register_button = ctk.CTkButton(self.inner_frame, text="Register", command=lambda: controller.show_frame("RegistrationFrame"))
        self.register_button.pack(padx=10, pady=5)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if self.database.verify_user(email, password):
            messagebox.showinfo("Login", "Login successful!")
            self.create_main_screen()
        else:
            messagebox.showerror("Login", "Invalid email or password")
    