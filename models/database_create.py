import mysql.connector
from mysql.connector import Error
from dotenv import find_dotenv, load_dotenv
from os import getenv
from .database_connect import ConnectDatabase


class CreateDatabase(ConnectDatabase):
    """ Class to manage the database. """
    def __init__(self):
       super().__init__()
    
    def create_database(self):
        """
        Create a new database.
        :return: ∅
        """
        with self.connect() as conn:  # with statement to automatically close the connection
            if conn:
                cursor = conn.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS budget_buddy")
                conn.commit()

    def create_table_client(self):
        """
        Create the client table of the budget_buddy database.
        :return: ∅
        """
        with self.connect("budget_buddy") as conn:
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS client(
                        id_client INT AUTO_INCREMENT,
                        last_name VARCHAR(100) NOT NULL,
                        first_name VARCHAR(50) NOT NULL,
                        email VARCHAR(100) NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        PRIMARY KEY(id_client),
                        UNIQUE(email)
                    )
                    """)
                conn.commit()

    def create_table_account(self):
        """
        Create the account table of the budget_buddy database.
        :return: ∅
        """
        with self.connect("budget_buddy") as conn:
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS account(
                        id_account INT AUTO_INCREMENT,
                        IBAN CHAR(34) NOT NULL,
                        amount DECIMAL(12,2) NOT NULL,
                        creation_date DATE NOT NULL,
                        id_client INT NOT NULL,
                        PRIMARY KEY(id_account),
                        UNIQUE(IBAN),
                        FOREIGN KEY(id_client) REFERENCES client(id_client)
                        )
                        """)
                conn.commit()

    def create_table_transaction(self):
        """
        Create the client transaction of the budget_buddy database.
        :return: ∅
        """
        with self.connect("budget_buddy") as conn:
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS transaction(
                        id_transaction INT AUTO_INCREMENT,
                        id_origin_account INT NOT NULL,
                        id_target_account INT NULL,
                        amount DECIMAL(10, 2) NOT NULL,
                        transaction_type VARCHAR(20) NOT NULL,
                        transaction_date TIMESTAMP,
                        PRIMARY KEY(id_transaction),
                        FOREIGN KEY (id_origin_account) REFERENCES account(id_account),
                        FOREIGN KEY (id_target_account) REFERENCES account(id_account)
                    )
                    """)
                conn.commit()