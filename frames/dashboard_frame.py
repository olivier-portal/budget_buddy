import customtkinter as ctk
from tkinter import messagebox
import re

from frames.home_frame import *

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, database, parent, controller):
        super().__init__(parent)
        
        self.controller = controller
        self.database = database
        
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        
        self.dashboard_frame = ctk.CTkFrame(self, fg_color="white")
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")
        
        self.dashboard_frame.grid_rowconfigure(0, weight=1)
        self.dashboard_frame.grid_columnconfigure(0, weight=1)
        
        # Create a container inside login_frame to hold widgets
        self.inner_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="white")
        self.inner_frame.pack(expand=True, padx=20, pady=20)
        
        self.label = ctk.CTkLabel(self.inner_frame, text="Dashboard", font=("Arial", 24))
        self.label.pack(padx=20, pady=20)

        # Add widgets to the frame
        """"""

        self.back_to_login_button = ctk.CTkButton(self.register_frame, text="Back to Login", command=lambda: controller.show_frame("HomeFrame"))
        self.back_to_login_button.pack(pady=12, padx=10)