import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        ''' Establish the database connection '''
        try:
            conn = mysql.connector.connect(
                host=os.getenv("HOST"),
                user=os.getenv("USER"),
                password=os.getenv("PASSWORD"),
                database=self.db_name
            )
            return conn
        except Error as e:
            raise Exception(f"Database connection error: {e}")