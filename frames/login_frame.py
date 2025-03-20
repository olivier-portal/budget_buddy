import customtkinter as ctk
from tkinter import messagebox

class LoginFrame(ctk.CTkFrame):
    def __init__(self, database, parent, controller, client):
        super().__init__(parent)
        
        self.controller = controller
        self.database = database
        self.client = client
        
        # define label in header
        self.controller.add_header_label("Home")
        
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        
        self.login_frame = ctk.CTkFrame(self, fg_color="white")
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        
        self.login_frame.grid_rowconfigure(0, weight=1)
        self.login_frame.grid_columnconfigure(0, weight=1)
        
        # Create a container inside login_frame to hold widgets
        self.inner_frame = ctk.CTkFrame(self.login_frame, fg_color="white")
        self.inner_frame.pack(expand=True, padx=20, pady=20)
        
        self.label = ctk.CTkLabel(self.inner_frame, text="Log to your account", font=("Arial", 24))
        self.label.pack(padx=20, pady=20)

        self.email_entry = ctk.CTkEntry(self.inner_frame, placeholder_text="Email")
        self.email_entry.pack(padx=20, pady=20)
        
        self.password_entry = ctk.CTkEntry(self.inner_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(padx=20, pady=20)

        self.login_button = ctk.CTkButton(self.inner_frame, text="Login", command=self.login)
        self.login_button.pack(padx=20, pady=20)

        self.register_button = ctk.CTkButton(self.inner_frame, text="Register",  command=lambda: self.controller.show_frame("RegistrationFrame"))
        self.register_button.pack(padx=20, pady=20)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if self.database.verify_user(email, password):
            messagebox.showinfo("Login", f"Login successful! Welcome {email}")
            self.client = self.database.get_client_by_email(email)
            print(self.client)
            self.switch_to_dashboard()
            print(self.client)
            return self.client
        else:
            messagebox.showerror("Login", "Invalid email or password")
            
    def switch_to_registration(self):
        """Switch to the registration frame and update the header."""
        self.controller.add_header_label("Register")
        self.controller.show_frame("RegistrationFrame")
        
    def switch_to_dashboard(self):
        """Switch to the registration frame and update the header."""
        self.controller.add_header_label("Dasboard")
        self.controller.show_frame("DashboardFrame")
    