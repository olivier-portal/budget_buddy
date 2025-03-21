import customtkinter as ctk

from frames.frame_manager import *
from frames.login_frame import *

class DashboardFrame(ctk.CTkFrame, FrameManager):
    def __init__(self, database, parent, controller, client, selected_account):
        super().__init__(parent)
        
        self.controller = controller
        self.database = database
        self.client = client
        self.selected_account = selected_account
        
        #Use FrameManager to switch between frames
        self.frame_manager = FrameManager(controller)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.dashboard_frame = ctk.CTkFrame(self, fg_color="white")
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")
        
        self.dashboard_frame.grid_rowconfigure(0, weight=5)  # Main container
        self.dashboard_frame.grid_rowconfigure(1, weight=1)  # Buttons
        self.dashboard_frame.grid_columnconfigure(0, weight=1)
        self.dashboard_frame.grid_columnconfigure(1, weight=1)
        
        # Create a container inside login_frame to hold widgets
        self.inner_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="white")
        self.inner_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        
        self.inner_frame.grid_rowconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(0, weight=1)
        
        self.label = ctk.CTkLabel(self.inner_frame, text="Dashboard", font=("Arial", 24))
        self.label.pack(padx=20, pady=20)

        # Add widgets to the frame
        """"""
        self.new_transaction_button = ctk.CTkButton(self.dashboard_frame, text="New transaction", height=40, command=None)
        self.new_transaction_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.back_to_login_button = ctk.CTkButton(self.dashboard_frame, text="Logout", height=40, command=self.logout)
        self.back_to_login_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
    def logout(self):
        self.client = None
        self.switch_to_login()
        print(self.client)