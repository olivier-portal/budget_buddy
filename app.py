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
        
        # Init frames
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        
        for F in (LoginFrame, RegistrationFrame, OperationsListFrame):
            frame = F(database=self.budget_db, parent=self.container, controller=self, client=self.client)
            self.frame[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("LoginFrame")
        
    def show_frame(self, frame_name):
        frame = self.frame[frame_name]
        frame.tkraise()
        
    
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