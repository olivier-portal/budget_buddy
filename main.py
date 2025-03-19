from models import *
from frames import *
from app import App

if __name__ == '__main__':
    app = App()
    app.mainloop()

    if app.budget_db.database_exists():
        app.run()
    else:
        app.budget_db = CreateDatabase()
        app.budget_db.create_database()
        app.budget_db.create_table_client()
        app.budget_db.create_table_account()
        app.budget_db.create_table_transaction()
        app.budget_db = Database()  # Reconnect to the newly created database

        app.run()