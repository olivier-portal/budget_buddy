import customtkinter as ctk
from frames import *
from models import *
from frames.frame_manager import FrameManager
from PIL import Image
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Budget Buddy")
        self.geometry("350x700")
        
        self.budget_db = Database()
        self.version = '1.0.0'
        self.client = None
        self.selected_account = None
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ICON_PATH = os.path.join(BASE_DIR, "assets", "icons")
        
        self.frame = {} # Stock frames in dictionary
        
        #Use FrameManager to switch between frames
        self.frame_manager = FrameManager(self)
        
        # Ensure consistent proportions by defining min sizes
        total_height = 700  # Total app height
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
        
        # Set footer grid layout
        self.footer.grid_rowconfigure(0, weight=1)
        for i in range(3):
            self.footer.grid_columnconfigure(i, weight=1)
        
        # Add buttons to the footer
        self.home_icon = ctk.CTkImage(Image.open(os.path.join(ICON_PATH, "home_icon.png")), size=(26, 26))
        self.transaction_icon = ctk.CTkImage(Image.open(os.path.join(ICON_PATH, "transaction_icon.png")), size=(26, 26))
        self.account_icon = ctk.CTkImage(Image.open(os.path.join(ICON_PATH, "account_icon.png")), size=(26, 26))
        
        self.home_button = ctk.CTkButton(self.footer, width=80, fg_color="transparent", text="Home", compound="top", image=self.home_icon, command=lambda: self.frame_manager.switch_to_login())
        self.home_button.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        self.transaction_button = ctk.CTkButton(self.footer, width=80, fg_color="transparent", text="Transaction",  compound="top", image=self.transaction_icon, command=lambda: self.frame_manager.switch_to_dashboard())
        self.transaction_button.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        
        self.account_button = ctk.CTkButton(self.footer, width=80, fg_color="transparent", text="Accounts", compound="top",  image=self.account_icon, command=lambda: self.frame_manager.switch_to_accounts())
        self.account_button.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")

        self.account_button.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")

        # Configure grid inside container
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        for F in (LoginFrame, RegistrationFrame, DashboardFrame, AccountsFrame, NewTransactionFrame):
            frame = F(database=self.budget_db, parent=self.container, controller=self, client=self.client, selected_account=self.selected_account)
            self.frame[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("LoginFrame")
        
    def show_frame(self, frame_name):
        frame = self.frame[frame_name]
        frame.tkraise()
        
    def add_header_label(self, text):
        self.header_label.configure(text=text)

    def set_client(self, client):
        """
        Set the client variable and update it in all frames.
        :param client: The client data to set.
        """
        self.client = client
        for frame in self.frame.values():
            frame.client = self.client  # Update the client in all frames
            if hasattr(frame, "update_client_data"):
                frame.update_client_data()  # Call update method if it exists

    def get_client_accounts(self):
        """
        Fetch the IBANs of the client's accounts from the database.
        :return: List of IBANs.
        """
        if self.client:
            accounts = self.budget_db.get_client_ibans(self.client[0])
            return [account[0] for account in accounts] if accounts else []
        return []
    
if __name__ == '__main__':
    controller = App()

    if controller.budget_db.database_exists():
        controller.mainloop()
    else:
        controller.budget_db = CreateDatabase()
        controller.budget_db.create_database()
        controller.budget_db.create_table_client()
        controller.budget_db.create_table_account()
        controller.budget_db.create_table_transaction()
        controller.budget_db = Database()  # Reconnect to the newly created database

        controller.mainloop()