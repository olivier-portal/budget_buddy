import customtkinter as ctk


class FrameManager():
    def __init__(self, controller):
        
        self.controller = controller
        
    def switch_to_login(self):
        """Switch to the login frame and update the header."""
        self.controller.add_header_label("Home")
        self.controller.show_frame("LoginFrame")
    
    def switch_to_registration(self):
        """Switch to the registration frame and update the header."""
        self.controller.add_header_label("Register")
        self.controller.show_frame("RegistrationFrame")
        
    def switch_to_dashboard(self):
        """Switch to the registration frame and update the header."""
        self.controller.add_header_label("Dasboard")
        self.controller.show_frame("DashboardFrame")
        
    def switch_to_accounts(self):
        """Switch to the accounts frame and update the header."""
        self.controller.add_header_label("Accounts")
        self.controller.show_frame("AccountsFrame")

    def switch_to_new_transaction(self):
        """Switch to the new transaction frame and update the header."""
        self.controller.add_header_label("New Transaction")
        self.controller.show_frame("NewTransactionFrame")