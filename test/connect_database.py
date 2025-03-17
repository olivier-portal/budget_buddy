import mysql.connector
from dotenv import find_dotenv, load_dotenv
from os import getenv

from .create_database import CreateDatabase


class ConnectDatabase:
    """ Class to connect to the database. """

    def __init__(self):
        """ Initialization of the class. """
        self.my_base = self.connect()

    def connect(self):
        """
        Connect to the database store.
        :return: Connexion to the database.
        """
        # Load the environment variables from .env
        dotenv_path = find_dotenv(".env")
        load_dotenv(dotenv_path)

        # Access to the environment variables
        my_host = getenv("HOST")
        my_port = getenv("PORT")
        my_user = getenv("USER")
        my_password = getenv("PASSWORD")

        # Connect to MySQL
        my_base = mysql.connector.connect(
            host=my_host,
            port=my_port,
            user=my_user,
            password=my_password
        )

        # Check if my database exists, if not create it
        if my_base.is_connected():
            cursor = my_base.cursor()

            cursor.execute("SHOW DATABASES LIKE 'store';")
            my_database = cursor.fetchone()

            if my_database:
                my_base.database = "store"  # Connect to my database
            else:
                CreateDatabase(my_base).create()  # Create my database
                my_base.database = "store"

            cursor.close()

        return my_base
