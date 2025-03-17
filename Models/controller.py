class Controller:
    def __init__(self, database):
        self.database = database

    def add_user(self, last_name, first_name, email, password):
        return self.database.add_user(last_name, first_name, email, password)

    def verify_user(self, email, password):
        return self.database.verify_user(email, password)
