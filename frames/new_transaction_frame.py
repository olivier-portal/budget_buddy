import customtkinter as ctk
from tkinter import messagebox
import re

from frames.login_frame import *
from frames.frame_manager import *

class NewTransactionFrame(ctk.CTkFrame, FrameManager):
    def __init__(self, database, parent, controller, client):
        super().__init__(parent)
        
        self.controller = controller
        self.database = database
        self.client = client
        self.client_accounts = self.get_client_accounts()
        
        #Use FrameManager to switch between frames
        self.frame_manager = FrameManager(controller)
        
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        
        self.register_frame = ctk.CTkFrame(self, fg_color="white")
        self.register_frame.grid(row=0, column=0, sticky="nsew")
        
        self.register_frame.grid_rowconfigure(0, weight=1)
        self.register_frame.grid_columnconfigure(0, weight=1)
        
        # Create a container inside login_frame to hold widgets
        self.inner_frame = ctk.CTkFrame(self.register_frame, fg_color="white")
        self.inner_frame.pack(expand=True, padx=20, pady=10)
        
        self.label = ctk.CTkLabel(self.inner_frame, text="Create a new transaction", font=("Arial", 24))
        self.label.pack(padx=10, pady=10)

        self.origin_label = ctk.CTkLabel(self, text="From Bank Account")
        self.origin_label.pack(pady=5)
        self.origin_var = ctk.StringVar(self)
        self.origin_menu = ctk.CTkOptionMenu(self, variable=self.origin_var, values=self.client_accounts)
        self.origin_menu.pack(pady=5)

        self.type_label = ctk.CTkLabel(self, text="Transaction Type")
        self.type_label.pack(pady=5)
        self.type_var = ctk.StringVar(self)
        self.type_menu = ctk.CTkOptionMenu(self, variable=self.type_var, values=["deposit", "withdrawal", "transfer"])
        self.type_menu.pack(pady=5)

        self.target_label = ctk.CTkLabel(self, text="To Bank Account")
        self.target_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Target Account")
        self.target_entry.pack(pady=12, padx=10)
        
        self.amount_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Transaction Amount")
        self.amount_entry.pack(pady=12, padx=10)

        self.confirm_button = ctk.CTkButton(self.register_frame, text="Register", command=self.confirm_transaction)
        self.confirm_button.pack(pady=12, padx=10)

        self.back_to_login_button = ctk.CTkButton(self.register_frame, text="Back to Login", command=lambda: self.switch_to_login())
        self.back_to_login_button.pack(pady=12, padx=10)

    def confirm_transaction(self):
        transaction_type = self.type_var.get()
        source = self.origin_var.get()
        target = self.target_entry.get()
        amount = self.amount_entry.get()

        if not self.validate_amount(amount):
            messagebox.showerror("Transaction", "Amount must be a positive number.")
            return

        if transaction_type == "transfer" and not self.validate_target(target):
            messagebox.showerror("Transaction", "Target account must be an existing account (IBAN).")
            return

        target_account = None if transaction_type in ["deposit", "withdrawal"] else target

        if self.database.save_transaction(transaction_type, amount, source, target_account):
            messagebox.showinfo("Transaction", "Transaction successful!")
            self.switch_to_dashboard()
        else:
            messagebox.showerror("Transaction", "Transaction failed. Target account may not exist.")

    def validate_amount(self, amount):
        """
        Validate if the amount is a positive number.
        :param amount: The amount to validate.
        :return: True if valid, False otherwise.
        """
        try:
            return float(amount) > 0
        except ValueError:
            return False
        
    def validate_target(self, target):
        """
        Validate if the target account exists.
        :param target: The target account (IBAN) to validate.
        :return: True if the account exists, False otherwise.
        """
        account = self.database.get_account_by_iban(target)
        return account is not None

    def get_client_accounts(self):
        """
        Fetch the IBANs of the client's accounts from the database.
        :return: List of IBANs.
        """
        if self.client:
            accounts = self.database.get_client_ibans(self.client[0])
            return [account[0] for account in accounts] if accounts else []
        return []

