

class User():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def create_user(self):
        self.database.create_user(self.username, self.password)

    def login_user(self):
        self.database.login_user(self.username, self.password)

    def logout_user(self):
        self.database.logout_user(self.username)

    def delete_user(self):
        self.database.delete_user(self.username)