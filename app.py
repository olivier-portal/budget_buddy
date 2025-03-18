from budget_buddy.database import Database
from budget_buddy.main_view import MainView

class App:
    def __init__(self):
        self.budget_db = Database()
        self.version = '1.0.0'

    def run(self):
        view = MainView(self.budget_db)
        view.mainloop()

if __name__ == '__main__':
    app = App()
    app.run()