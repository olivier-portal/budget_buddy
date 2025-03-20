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
        
        # Ensure consistent proportions by defining min sizes
        total_height = 600  # Total app height
        header_height = int(total_height * 0.05)  # 20%
        container_height = int(total_height * 0.9)  # 60%
        footer_height = int(total_height * 0.05)  # 20%

        # Configure grid layout for main window
        self.grid_rowconfigure(0, weight=1, minsize=header_height)  # Header (20%)
        self.grid_rowconfigure(1, weight=8, minsize=container_height)  # Container (60%)
        self.grid_rowconfigure(2, weight=1, minsize=footer_height)  # Footer (20%)
        self.grid_columnconfigure(0, weight=1)  # Single column layout

        # Init frames
        self.header = ctk.CTkFrame(self, fg_color="darkblue")
        self.container = ctk.CTkFrame(self, fg_color="white")
        self.footer = ctk.CTkFrame(self, fg_color="darkblue")
        
        # Ensure frames do not shrink smaller than expected
        self.header.grid(row=0, column=0, sticky="nsew")
        self.container.grid(row=1, column=0, sticky="nsew")
        self.footer.grid(row=2, column=0, sticky="nsew")
        
        # Force white background in case of UI issue
        self.container.configure(fg_color="white")

        # Configure grid inside container
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Debugging (Check actual height allocation)
        print(f"Expected Heights: Header={header_height}px, Container={container_height}px, Footer={footer_height}px")
        
        for F in (HomeFrame, RegistrationFrame):
            frame = F(database=self.budget_db, parent=self.container, controller=self)
            self.frame[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("HomeFrame")
        
    def show_frame(self, frame_name):
        frame = self.frame[frame_name]
        frame.tkraise()
        