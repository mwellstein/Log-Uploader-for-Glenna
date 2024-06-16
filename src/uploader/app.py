import logging
import traceback

from controller import Controller
from logic.model import Model
from ui.view import View


class App:
    def __init__(self):
        self.view = View()
        self.model = Model()

        controller = Controller(self.model, self.view)
        self.view.set_controller(controller)
        self.model.set_controller(controller)
        self.logging()

    @staticmethod
    def logging():
        logger = logging.getLogger()

        logger.setLevel(logging.DEBUG)  # Global level

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Create a file handler
        file_handler = logging.FileHandler("glenna_log_uploader.log")
        file_handler.setLevel(logging.DEBUG)  # File level can be different
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)


if __name__ == "__main__":
    try:
        app = App()
        window = app.view
        window.protocol("WM_DELETE_WINDOW", lambda: window.destroy())
        window.mainloop()
    except Exception as e:
        logging.error(f"Unexpected Error in the App: {str(e)}")
        with open("glenna_log_uploader.crashlog", "a") as file:
            traceback.print_exc(file=file)
            raise e
