import mysql.connector
from mysql.connector import Error
from dotenv import find_dotenv, load_dotenv
from os import getenv
import bcrypt

class Database:
    def __init__(self):
        # Load the environment variables from .env
        self.dotenv_path = find_dotenv("../.env")
        load_dotenv(self.dotenv_path)

        # Access to the environment variables
        self.db_host = getenv("HOST")
        self.db_port = getenv("PORT")
        self.db_user = getenv("USER")
        self.db_password = getenv("PASSWORD")
        self.db_name = "budget_buddy"

    def connect(self, chosen_database=None):
        ''' Establish the database connection '''
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
    
    def create_database(self, database):
        '''create a database'''
        with self.connect() as conn:  # with statement to automatically close the connection
            if conn:
                cursor = conn.cursor()
                cursor.execute(f"CREATE DATABASE {database}")
                conn.commit()

    def create_table_client(self):
        '''create a table'''
        with self.connect("budget_buddy") as conn:
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS client(
                    Id_client INT AUTO_INCREMENT,
                    last_name VARCHAR(100) NOT NULL,
                    first_name VARCHAR(50) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    password VARCHAR(50) NOT NULL,
                    PRIMARY KEY(Id_client),
                    UNIQUE(email)
                    )""")
                conn.commit()

    def add_user(self, last_name, first_name, email, password):
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

