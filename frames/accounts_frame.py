import customtkinter as ctk
from tkinter import messagebox
import re

from frames.login_frame import *

class AccountsFrame(ctk.CTkFrame):
    def __init__(self, database, parent, controller, client, selected_account):
        super().__init__(parent)
        
        self.controller = controller
        self.database = database
        self.client = client
        self.client_accounts = self.controller.get_client_accounts()
        self.selected_account = selected_account
        
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        
        self.account_frame = ctk.CTkFrame(self, fg_color="white")
        self.account_frame.grid(row=0, column=0, sticky="nsew")
        
        self.account_frame.grid_rowconfigure(0, weight=1)
        self.account_frame.grid_columnconfigure(0, weight=1)
        
        # Create a container inside account_frame to hold widgets
        self.inner_frame = ctk.CTkFrame(self.account_frame, fg_color="white")
        self.inner_frame.pack(expand=True, padx=20, pady=20)
        
        self.label = ctk.CTkLabel(self.inner_frame, text="Accounts", font=("Arial", 24))
        self.label.pack(padx=20, pady=20)

        # Create a textbox to display the accounts
        self.accounts_textbox = ctk.CTkTextbox(self.account_frame, height=10, width=50)
        self.accounts_textbox.pack(padx=10, pady=10, fill="both", expand=True)

        # Add widgets to the frame
        self.add_account_button = ctk.CTkButton(self.account_frame, text="Add Account", command=self.add_account)
        self.add_account_button.pack(pady=12, padx=10)

        self.back_to_login_button = ctk.CTkButton(self.account_frame, text="Logout", command=self.logout)
        self.back_to_login_button.pack(pady=12, padx=10)

    def add_account(self):
        """
        Add a new account for the current client.
        """
        if self.client:
            success = self.database.create_account(self.client[0])
            if success:
                messagebox.showinfo("Add Account", "Account successfully created!")
                self.update_client_data()  # Refresh client accounts
            else:
                messagebox.showerror("Add Account", "Failed to create account.")
        else:
            messagebox.showerror("Add Account", "No client is logged in.")
        
    def update_client_data(self):
        """
        Update the client data.
        """
        self.client = self.controller.client
        self.client_accounts = self.controller.get_client_accounts()

    def logout(self):
        self.client = None
        self.controller.show_frame("LoginFrame")
        print(self.client)

    def load_accounts(self):
        """
        Load the accounts associated with the client and display them in the textbox.
        """
        if self.client:
            client_accounts = self.database.get_client_accounts(self.client[0])

            if client_accounts:
                account_text = "\n".join(
                    [f"Account IBAN: {account[0]}, Amount: {account[1]}, Creation Date : {account[2]}, C" for account in client_accounts])
                self.accounts_textbox.delete(1.0, ctk.END)
                self.accounts_textbox.insert(ctk.END, account_text)
            else:
                self.accounts_textbox.delete(1.0, ctk.END)
                self.accounts_textbox.insert(ctk.END, "No accounts found for this client.")
