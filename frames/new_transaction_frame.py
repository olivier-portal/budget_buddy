import customtkinter as ctk
from tkinter import messagebox
from decimal import Decimal, InvalidOperation

from frames.login_frame import *
from frames.frame_manager import *

class NewTransactionFrame(ctk.CTkFrame, FrameManager):
    def __init__(self, database, parent, controller, client, selected_account): 
        super().__init__(parent)
        self.controller = controller
        self.database = database
        self.client = client
        self.selected_account = selected_account
        self.client_accounts = self.controller.get_client_accounts()

        # Use FrameManager to switch between frames
        self.frame_manager = FrameManager(controller)

        # Configure grid system for the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a container inside the frame
        self.register_frame = ctk.CTkFrame(self, fg_color="white")
        self.register_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid system for the register_frame
        self.register_frame.grid_rowconfigure(list(range(10)), weight=1)
        self.register_frame.grid_columnconfigure(0, weight=1)

        # Add widgets using grid
        self.label = ctk.CTkLabel(self.register_frame, text="Create a new transaction", font=("Arial", 24))
        self.label.grid(row=0, column=0, pady=10, padx=10)

        self.origin_label = ctk.CTkLabel(self.register_frame, text="From Bank Account")
        self.origin_label.grid(row=1, column=0, pady=0, padx=10)

        self.origin_var = ctk.StringVar(self)
        self.origin_menu = ctk.CTkOptionMenu(self.register_frame, variable=self.origin_var, values=self.client_accounts)
        self.origin_menu.grid(row=2, column=0, pady=5, padx=10)

        self.type_label = ctk.CTkLabel(self.register_frame, text="Transaction Type")
        self.type_label.grid(row=3, column=0, pady=0, padx=10)

        self.type_var = ctk.StringVar(self)
        self.type_menu = ctk.CTkOptionMenu(self.register_frame, variable=self.type_var, values=["deposit", "withdrawal", "transfer"])
        self.type_menu.grid(row=4, column=0, pady=5, padx=10)

        self.target_label = ctk.CTkLabel(self.register_frame, text="To Bank Account")
        self.target_label.grid(row=5, column=0, pady=0, padx=10)

        self.target_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Target Account")
        self.target_entry.grid(row=6, column=0, pady=5, padx=10)

        self.amount_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Transaction Amount")
        self.amount_entry.grid(row=7, column=0, pady=5, padx=10)

        self.confirm_button = ctk.CTkButton(self.register_frame, text="Confirm", command=self.confirm_transaction)
        self.confirm_button.grid(row=8, column=0, pady=5, padx=10)

        self.back_to_login_button = ctk.CTkButton(self.register_frame, text="Back to Login", command=lambda: self.switch_to_login())
        self.back_to_login_button.grid(row=9, column=0, pady=5, padx=10)

    def confirm_transaction(self):
        transaction_type = self.type_var.get()
        source = self.origin_var.get()
        target = self.target_entry.get()
        amount = self.amount_entry.get()

        if not self.validate_amount(amount):
            messagebox.showerror("Transaction", "Amount must be a positive number.")

        if transaction_type == "transfer":
            target_account = self.database.get_account_by_iban(target)
            if target_account is None:
                messagebox.showerror("Transaction", "Target account must be an existing account (IBAN).")
                return
            else:
                target = target_account[0]
        elif transaction_type in ["deposit", "withdrawal"]:
            target = None
        else:
            messagebox.showerror("Transaction", "Invalid transaction type.")
            return

        source_account = self.database.get_account_by_iban(source)
        if source_account is None:
            messagebox.showerror("Transaction", "Source account (IBAN) does not exist.")
            return
        source = source_account[0]

        if self.database.save_transaction(transaction_type, amount, source, target):
            messagebox.showinfo("Transaction", f"Transaction saved: {transaction_type}, {amount}, {source}, {target}")
            print(f"Transaction saved: {transaction_type}, {amount}, {source}, {target}")
            try:
                self.update_accounts(transaction_type, amount, source, target)
                self.switch_to_dashboard()
            except Exception as e:
                messagebox.showerror("Transaction", f"Transaction failed: {e}")
        else:
            messagebox.showerror("Transaction", "Transaction failed. Target account may not exist.")

    def update_accounts(self, transaction_type, amount, source, target):
        """
        Update the account balances based on the transaction type.
        :param transaction_type: The type of transaction.
        :param amount: The amount of the transaction.
        :param source: The source account ID.
        :param target: The target account ID.
        """
        try:
            amount = Decimal(amount)  # Convert amount to Decimal for precise arithmetic
            if transaction_type == "transfer":
                # Deduct from source and add to target
                if not self.database.update_account_balance(source, -amount):
                    raise Exception(f"Failed to update source account: {source}")
                if not self.database.update_account_balance(target, amount):
                    raise Exception(f"Failed to update target account: {target}")
            elif transaction_type == "deposit":
                # Add to source
                if not self.database.update_account_balance(source, amount):
                    raise Exception(f"Failed to update source account: {source}")
            elif transaction_type == "withdrawal":
                # Deduct from source
                if not self.database.update_account_balance(source, -amount):
                    raise Exception(f"Failed to update source account: {source}")
            else:
                raise ValueError("Invalid transaction type.")
        except Exception as e:
            print(f"Error in update_accounts: {e}")
            messagebox.showerror("Transaction", f"Failed to update accounts: {e}")

    def validate_amount(self, amount):
        """
        Validate if the amount is a positive number.
        :param amount: The amount to validate.
        :return: True if valid, False otherwise.
        """
        try:
            return Decimal(amount) > 0  # Convert to Decimal for validation
        except (ValueError, InvalidOperation):
            return False
        
    def validate_target(self, target):
        """
        Validate if the target account exists.
        :param target: The target account (IBAN) to validate.
        :return: True if the account exists, False otherwise.
        """
        account = self.database.get_account_by_iban(target)
        return account is not None

    def update_client_data(self):
        """
        Update the client data and refresh client accounts.
        """
        self.client = self.controller.client
        self.client_accounts = self.controller.get_client_accounts()
        self.origin_menu.configure(values=self.client_accounts)
        print(f"Updated client in NewTransactionFrame: {self.client}")