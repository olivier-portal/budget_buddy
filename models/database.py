from .database_connect import ConnectDatabase
import mysql.connector
from mysql.connector import Error
import bcrypt


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
