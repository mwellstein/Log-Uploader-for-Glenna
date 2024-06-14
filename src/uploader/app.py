from ui.view import View
from uploader.controller import Controller
from logic.model import Model

class App:
    def __init__(self):
        self.view = View()

        self.model = 2

        controller = Controller(self.model, self.view)

        self.view.set_controller(controller)


if __name__ == "__main__":
    app = App()
    window = app.view
    window.protocol("WM_DELETE_WINDOW", lambda: window.destroy())
    window.mainloop()
