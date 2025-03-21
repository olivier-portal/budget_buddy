from .database_connect import ConnectDatabase
from mysql.connector import Error
import bcrypt
import random
import string
from datetime import datetime


class Database(ConnectDatabase):
    """ Class to manage the database. """
    
    def __init__(self):
        super().__init__()

    def database_exists(self):
        """
        Check if the database exists.
        :return: True if the database exists, False otherwise.
        """
        try:
            with self.connect() as conn:
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SHOW DATABASES LIKE 'budget_buddy'")
                    database = cursor.fetchone()
                    if database:
                        return True
                    else:
                        return False
        except Error as e:
            print(f"Error checking database existence: {e}")
            return False

    def add_user(self, last_name, first_name, email, password):
        """method used to register a new user"""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            with self.connect("budget_buddy") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                       INSERT INTO client (last_name, first_name, email, password)
                       VALUES (%s, %s, %s, %s)
                   """, (last_name, first_name, email, hashed_password))
                conn.commit()
                return True
        except Error as e:
            print(f"Error adding user: {e}")
            return False

    def verify_user(self, email, password):
        """method used for user login"""
        try:
            with self.connect("budget_buddy") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT password FROM client WHERE email = %s", (email,))
                result = cursor.fetchone()
                if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                    return True
        except Error as e:
            print(f"Error verifying user: {e}")
            return False
        
    def get_client_by_email(self, email_client):
        """
        Get the client information by email.
        :param email_client: The email of the client.
        :return: The client information.
        """
        try:
            with self.connect("budget_buddy") as conn:
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id_client, last_name, first_name, email FROM client WHERE email = %s", (email_client,))
                    client = cursor.fetchone()
                    return client
        except Error as e:
            print(f"Error getting client by email: {e}")
            return False

    
    def create_account(self, id_client):
        """
        Create a new account for a client with an initial amount of 0, 
        the current date as the creation date, and a unique IBAN.
        :param id_client: The ID of the client for whom the account is created.
        :return: ∅
        """
        iban = ''.join(random.choices(string.ascii_uppercase + string.digits, k=34))
        creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with self.connect("budget_buddy") as conn:
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO account (IBAN, amount, creation_date, id_client)
                        VALUES (%s, %s, %s, %s)
                    """, (iban, 0, creation_date, id_client))
                    conn.commit()
                    return True
        except Error as e:
            print(f"Error creating new account: {e}")
            return False
        
    def update_account_balance(self, iban_account, amount):
        """
        Update the amount of an account.
        :param id_account: The ID of the account.
        :param amount: The new amount of the account.
        :return: ∅
        """
        try:
            with self.connect("budget_buddy") as conn:
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE account SET amount = %s WHERE IBAN = %s", (amount, iban_account))
                    conn.commit()
                    return True
        except Error as e:
            print(f"Error updating account amount: {e}")
            return False

    def save_transaction(self, transaction_type, amount, id_origin_account, id_destination_account=None):
        """
        Save a transaction between two accounts.
        :param id_origin_account: The ID of the account from which the amount is withdrawn.
        :param id_destination_account: The ID of the account to which the amount is deposited.
        :param amount: The amount of the transaction.
        :return: ∅
        """
        try:
            with self.connect("budget_buddy") as conn:
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO transaction (id_origin_account, id_destination_account, transaction_type, amount, transaction_date)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (id_origin_account, id_destination_account, transaction_type, amount, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    conn.commit()
                    return True
        except Error as e:
            print(f"Error saving transaction: {e}")
            return False
        
    def get_transactions_by_account(self, id_account):
        """
        Get the transactions of an account.
        :param id_account: The ID of the account.
        :return: The transactions of the account.
        """
        try:
            with self.connect("budget_buddy") as conn:
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id_transaction, id_origin_account, id_destination_account, transaction_type, amount, transaction_date FROM transaction WHERE id_origin_account = %s OR id_destination_account = %s", (id_account, id_account))
                    transactions = cursor.fetchall()
                    return transactions
        except Error as e:
            print(f"Error getting transactions by account: {e}")
            return False
        
    def get_account_by_iban(self, iban):
        """
        Get the account information by IBAN.
        :param iban: The IBAN of the account.
        :return: The account information.
        """
        try:
            with self.connect("budget_buddy") as conn:
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id_account, IBAN, amount, creation_date, id_client FROM account WHERE IBAN = %s", (iban,))
                    account = cursor.fetchone()
                    return account
        except Error as e:
            print(f"Error getting account by IBAN: {e}")
            return False
        
    def get_client_ibans(self, id_client):
        """
        Get the accounts IBANs of a client.
        :param id_client: The ID of the client.
        :return: List of IBANs.
        """
        try:
            with self.connect("budget_buddy") as conn:
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT IBAN FROM account WHERE id_client = %s", (id_client,))
                    client_ibans = cursor.fetchall()
                    return client_ibans
        except Error as e:
            print(f"Error getting client accounts: {e}")
            return []
        
    def get_client_transactions(self, id_client):
        """
        Get the transactions of a client.
        :param id_client: The ID of the client.
        :return: The transactions of the client.
        """
        try:
            with self.connect("budget_buddy") as conn:
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT t.id_transaction, t.id_origin_account, t.id_destination_account, t.transaction_type, t.amount, t.transaction_date
                        FROM transaction t
                        JOIN account a ON t.id_origin_account = a.id_account
                        WHERE a.id_client = %s
                        JOIN account b ON t.id_destination_account = b.id_account
                        WHERE b.id_client = %s
                    """, (id_client))
                    transactions = cursor.fetchall()
                    return transactions
        except Error as e:
            print(f"Error getting client transactions: {e}")

if __name__ == '__main__':
    db = Database()
    # db.create_account(1)
    print(db.database_exists())
    print(db.get_client_ibans(1))
    print(db.get_account_by_iban('R6IW5M0E8B2AK7OOIQZ4I5NF4JN0ZSL79N'))
    # print(db.get_client_transactions(1))