import logging
import sys
import traceback
from logging.handlers import RotatingFileHandler
from pathlib import Path

from controller import Controller
from logic.model import Model
from ui.view import View


class App:
    def __init__(self):
        self.view = View()
        self.model = Model()

        self.controller = Controller(self.model, self.view)
        self.view.set_controller(self.controller)
        self.model.set_controller(self.controller)
        self.setup_logging()

    @staticmethod
    def setup_logging():
        logger = logging.getLogger()

        logger.setLevel(logging.DEBUG)  # Global level

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # TODO Add Option to disable in GUI? Or to delete on close by default but being able to disable?

        # TODO: AS EXE its stuck at the collecting stage?

        if getattr(sys, "frozen", False) and hasattr(sys, '_MEIPASS'):
            log_path = Path(getattr(sys, "_MEIPASS")) / "glenna_log_uploader.log"
        else:
            log_path = Path("glenna_log_uploader.log")  # If run from source

        # Create a file handler
        file_handler = RotatingFileHandler(log_path, maxBytes=5*1024*1024, backupCount=3)
        file_handler.setLevel(logging.DEBUG)  # File level can be different
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    def close(self):
        logging.info("Closing window - ending async thread")
        if self.controller:
            self.controller.handle_reset_button()  # Stops the async loop and thread after current uploads

        window.destroy()


if __name__ == "__main__":
    try:
        app = App()
        window = app.view
        window.protocol("WM_DELETE_WINDOW", app.close)
        window.mainloop()
    except Exception as e:
        logging.error(f"Unexpected Error in the App: {str(e)}")
        with open("glenna_log_uploader.crashlog", "a") as file:
            traceback.print_exc(file=file)
            raise e
