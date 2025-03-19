import mysql.connector
from mysql.connector import Error
from dotenv import find_dotenv, load_dotenv
from os import getenv


class ConnectDatabase:
    """Base class to manage database connections."""

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
