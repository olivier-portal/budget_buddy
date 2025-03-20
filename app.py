import customtkinter as ctk
from frames import *
from models import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Budget Buddy")
        self.geometry("350x600")
        
        self.budget_db = Database()
        self.version = '1.0.0'
        self.client = None
        
        self.frame = {} # Stock frames in dictionary
        
        # Ensure consistent proportions by defining min sizes
        total_height = 600  # Total app height
        header_height = int(total_height * 0.1)
        container_height = int(total_height * 0.8)
        footer_height = int(total_height * 0.1)

        # Configure grid layout for main window
        self.grid_rowconfigure(0, weight=1, minsize=header_height)  # Header (10%)
        self.grid_rowconfigure(1, weight=8, minsize=container_height)  # Container (80%)
        self.grid_rowconfigure(2, weight=1, minsize=footer_height)  # Footer (10%)
        self.grid_columnconfigure(0, weight=1)  # Single column layout

        # Init frames
        self.header = ctk.CTkFrame(self, fg_color="darkblue")
        self.container = ctk.CTkFrame(self, fg_color="white")
        self.footer = ctk.CTkFrame(self, fg_color="darkblue")
        
        self.header.grid(row=0, column=0, sticky="nsew")
        self.container.grid(row=1, column=0, sticky="nsew")
        self.footer.grid(row=2, column=0, sticky="nsew")
        
        # Add a label to the header
        self.header_label = ctk.CTkLabel(self.header, text="Budget Buddy", font=("Arial", 24), text_color="white")
        self.header_label.pack(pady=10)

        # Configure grid inside container
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        for F in (LoginFrame, RegistrationFrame, OperationsListFrame):
            frame = F(database=self.budget_db, parent=self.container, controller=self, client=self.client)
            self.frame[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("LoginFrame")
        
    def show_frame(self, frame_name):
        frame = self.frame[frame_name]
        frame.tkraise()
        
    def add_header_label(self, text):
        self.header_label.configure(text=text)
    
if __name__ == '__main__':
    app = App()

    if app.budget_db.database_exists():
        app.mainloop()
    else:
        app.budget_db = CreateDatabase()
        app.budget_db.create_database()
        app.budget_db.create_table_client()
        app.budget_db.create_table_account()
        app.budget_db.create_table_transaction()
        app.budget_db = Database()  # Reconnect to the newly created database

        app.mainloop()