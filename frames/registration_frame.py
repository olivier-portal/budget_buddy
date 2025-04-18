import customtkinter as ctk
from tkinter import messagebox
import re
from PIL import Image

from frames.login_frame import *
from frames.frame_manager import *

class RegistrationFrame(ctk.CTkFrame, FrameManager):
    def __init__(self, database, parent, controller, client, selected_account):
        super().__init__(parent)
        
        self.controller = controller
        self.database = database
        
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        LOGO_PATH = os.path.join(BASE_DIR, "assets", "icons", "Logo.png")
        
        #Use FrameManager to switch between frames
        self.frame_manager = FrameManager(controller)
        
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        
        self.register_frame = ctk.CTkFrame(self, fg_color="white")
        self.register_frame.grid(row=0, column=0, sticky="nsew")
        
        self.register_frame.grid_rowconfigure(0, weight=1)
        self.register_frame.grid_columnconfigure(0, weight=1)
        
        # Create a container inside login_frame to hold widgets
        self.inner_frame = ctk.CTkFrame(self.register_frame, fg_color="white")
        self.inner_frame.pack(expand=True, padx=20, pady=10)
        
        image = Image.open(LOGO_PATH)
        self.my_image = ctk.CTkImage(light_image=image, dark_image=image, size=(180, 180))
        self.image_label = ctk.CTkLabel(self.inner_frame, image=self.my_image, text="")
        self.image_label.pack(pady=10)
        
        self.label = ctk.CTkLabel(self.inner_frame, text="Create an account", font=("Arial", 24))
        self.label.pack(padx=10, pady=10)

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

        self.back_to_login_button = ctk.CTkButton(self.register_frame, text="Back to Login", command=lambda: self.switch_to_login())
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
            self.controller.show_frame("LoginFrame")
        else:
            messagebox.showerror("Registration", "Registration failed. Email may already be in use.")

    def validate_password(self, password):
        password_format = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{10,}$'
        return bool(re.match(password_format, password))

    def validate_email(self, email):
        email_format = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_format, email))