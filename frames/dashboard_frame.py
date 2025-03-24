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
        print(client)
        self.parent_frame = parent
        
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
        
        # Create a container inside dashboard_frame to hold widgets
        self.inner_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="white")
        self.inner_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        
        self.inner_frame.grid_rowconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(0, weight=1)

        # Show client transactions
        self.transactions_frame = ctk.CTkScrollableFrame(master=self.inner_frame, width=600, height=300, fg_color="white")
        self.transactions_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # self.textbox = ctk.CTkTextbox(self.dashboard_frame, height=10, width=50)
        # self.textbox.grid(row=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        # self.textbox.insert("0.0", "Some example text!\n" * 50, "top")
        
        self.new_transaction_button = ctk.CTkButton(self.dashboard_frame, text="New transaction", height=40, command=lambda: self.switch_to_new_transaction())
        self.new_transaction_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.back_to_login_button = ctk.CTkButton(self.dashboard_frame, text="Logout", height=40, command=self.logout)
        self.back_to_login_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
    def logout(self):
        self.client = None
        self.switch_to_login()
        print(self.client)

    def update_client_data(self):
        """
        Update the client data.
        """
        self.client = self.controller.client
        self.client_accounts = self.controller.get_client_accounts()
        self.load_transactions()

    def load_transactions(self):
        """
        Method to load and display transactions for the client.
        """
        # Clear previous widgets
        for widget in self.transactions_frame.winfo_children():
            widget.destroy()
            
        client_transactions = []
        
        if self.client:
            client_transactions = self.database.get_client_transactions(self.client[0])

        if client_transactions:
            for idx, tx in enumerate(client_transactions):
                tx_label = ctk.CTkLabel(
                    master=self.transactions_frame,
                    text=f"{tx[3]} | {tx[4]} € | Date: {tx[5]}",
                    anchor="w",
                    font=ctk.CTkFont(size=13)
                )
                tx_label.grid(row=idx, column=0, sticky="w", padx=10, pady=5)
        else:
            empty_label = ctk.CTkLabel(
                master=self.transactions_frame,
                text="No transactions found for this client.",
                font=ctk.CTkFont(size=13, weight="bold")
            )
            empty_label.grid(row=0, column=0, padx=10, pady=10)