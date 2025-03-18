from models import *

class App:
    def __init__(self):
        self.budget_db = Database()
        self.version = '1.0.0'

    def run(self):
        view = MainView(self.budget_db)
        view.mainloop()

if __name__ == '__main__':
    app = App()
    app.budget_db.create_database()
    app.budget_db.create_table_client()
    app.budget_db.create_table_account()
    app.budget_db.create_table_transaction()
    app.run()