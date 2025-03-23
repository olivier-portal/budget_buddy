import customtkinter as ctk
import os

from tkinter import messagebox
from frames.frame_manager import *
from PIL import Image

class LoginFrame(ctk.CTkFrame, FrameManager):
    def __init__(self, database, parent, controller, client, selected_account):
        super().__init__(parent)
        
        self.controller = controller
        self.database = database
        self.client = client
        self.selected_account = selected_account
        
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        LOGO_PATH = os.path.join(BASE_DIR, "assets", "icons", "Logo.png")

        #Use FrameManager to switch between frames
        self.frame_manager = FrameManager(controller)
        
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
        
        image = Image.open(LOGO_PATH)
        self.my_image = ctk.CTkImage(light_image=image, dark_image=image, size=(180, 180))
        self.image_label = ctk.CTkLabel(self.inner_frame, image=self.my_image, text="")
        self.image_label.pack(pady=10)


        self.label = ctk.CTkLabel(self.inner_frame, text="Log to your account", font=("Arial", 24))
        self.label.pack(padx=20, pady=20)

        self.email_entry = ctk.CTkEntry(self.inner_frame, placeholder_text="Email")
        self.email_entry.pack(padx=20, pady=20)
        
        self.password_entry = ctk.CTkEntry(self.inner_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(padx=20, pady=20)

        self.login_button = ctk.CTkButton(self.inner_frame, text="Login", command=self.login)
        self.login_button.pack(padx=20, pady=20)

        self.register_button = ctk.CTkButton(self.inner_frame, text="Register",  command=lambda: self.switch_to_registration())
        self.register_button.pack(padx=20, pady=20)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if self.database.verify_user(email, password):
            self.client = self.database.get_client_by_email(email)
            self.controller.set_client(self.client)  # Update the client in the App class
            messagebox.showinfo("Login", f"Login successful! Welcome {self.client[2]}")
            self.controller.frame['DashboardFrame'].load_transactions()
            self.controller.frame['AccountsFrame'].load_accounts()
            self.switch_to_dashboard()
        else:
            messagebox.showerror("Login", "Invalid email or password")
