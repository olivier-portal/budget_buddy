import mysql.connector
from mysql.connector import Error
from dotenv import find_dotenv, load_dotenv
from os import getenv
import bcrypt


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

    def add_user(self, last_name, first_name, email, password):
        """"""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            with self.connect(self.db_name) as conn:
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
        """"""
        try:
            with self.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT password FROM client WHERE email = %s", (email,))
                result = cursor.fetchone()
                if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                    return True
        except Error as e:
            print(f"Error verifying user: {e}")
        return False
