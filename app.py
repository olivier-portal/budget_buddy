from Models.database import Database
from Models.main_view import MainView
from Models.controller import Controller

class App:
    def __init__(self):
        self.budget_db = Database()
        self.controller = Controller(self.budget_db)
        self.version = '1.0.0'

    def run(self):
        view = MainView(self.controller)
        view.mainloop()

if __name__ == '__main__':
    app = App()
    app.run()