import mysql.connector
from mysql.connector import Error
from dotenv import find_dotenv, load_dotenv
from os import getenv


class Database:
    """ Class to manage the database. """
    def __init__(self):
        # Load the environment variables from .env
        self.dotenv_path = find_dotenv(".env")
        load_dotenv(self.dotenv_path)

        # Access to the environment variables
        self.db_host = getenv("HOST")
        self.db_port = getenv("PORT")
        self.db_user = getenv("USER")
        self.db_password = getenv("PASSWORD")

    def connect(self, chosen_database=None):
        """
        Establish the database connection.
        :return: Database connection.
        """
        try:
            conn = mysql.connector.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
            )
            if chosen_database is not None:
                conn.database = chosen_database
            return conn
        except Error as e:
            raise Exception(f"Database connection error: {e}")
    
    def create_database(self):
        """
        Create a new database.
        :return: ∅
        """
        with self.connect() as conn:  # with statement to automatically close the connection
            if conn:
                cursor = conn.cursor()
                cursor.execute(f"CREATE DATABASE budget_buddy")
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
                        password VARCHAR(50) NOT NULL,
                        PRIMARY KEY(id_client),
                        UNIQUE(email)
                    )
                    """)
                conn.commit()
                
    def create_account_table(self):
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
                        IBAN VARCHAR(34) NOT NULL,
                        amount DECIMAL(15,2) NOT NULL,
                        creation_date DATE NOT NULL,
                        id_client INT NOT NULL,
                        PRIMARY KEY(id_account),
                        UNIQUE(IBAN),
                        FOREIGN KEY(id_client) REFERENCES client(id_client)
                        )
                        """)
                conn.commit()
                
    def create_transaction_table(self):
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

   