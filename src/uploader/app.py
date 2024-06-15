from ui.view import View
from uploader.controller import Controller
from logic.model import Model
import logging


class App:
    def __init__(self):
        self.view = View()
        self.model = Model()

        controller = Controller(self.model, self.view)
        self.view.set_controller(controller)
        self.logging()

    @staticmethod
    def logging():
        logger = logging.getLogger()
        # TODO: Set back to error only
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Create a file handler
        # file_handler = logging.FileHandler("glenna_log_uploader.log")
        # file_handler.setLevel(logging.ERROR)
        # file_handler.setFormatter(formatter)
        # logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)


if __name__ == "__main__":
    app = App()
    window = app.view
    window.protocol("WM_DELETE_WINDOW", lambda: window.destroy())
    window.mainloop()
