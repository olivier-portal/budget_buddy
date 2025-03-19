import customtkinter as ctk
from frames.home_frame import HomeFrame
from frames.registration_frame import RegistrationFrame
from models import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Budget Buddy")
        self.geometry("350x600")
        
        self.budget_db = Database()
        self.version = '1.0.0'
        
        self.frame = {} # Stock frames in dictionary
        
        # Init frames
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        for F in (HomeFrame, RegistrationFrame):
            frame = F(database=self.budget_db, parent=container, controller=self)
            self.frame[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("HomeFrame")
        
    def show_frame(self, frame_name):
        frame = self.frame[frame_name]
        frame.tkraise()
        