import customtkinter as ctk
from tkinter import messagebox
import re

from frames.login_frame import *

class OperationsListFrame(ctk.CTkFrame):
    def __init__(self, database, parent, controller, client):
        super().__init__(parent)
        
        self.controller = controller
        self.database = database
        self.client = client
        
        self.register_frame = ctk.CTkFrame(self)
        self.register_frame.pack(fill="both", expand=True)

       

    def display_if_type(self, type):
        pass