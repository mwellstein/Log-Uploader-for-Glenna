from tkinter.messagebox import showerror

from customtkinter import CTk, CTkFrame

from .day_selector import DaySelector
from .path_selector import PathSelector
from .week_selector import WeekSelector
from .upload_frame import UploadFrame
from .copy_frame import CopyFrame


class View(CTk):
    def __init__(self):
        super().__init__()

        self.title("Log Uploader for Glenna")
        self.geometry("600x400")

        # Top Frame Level 1 (deep)
        self.top_frame = CTkFrame(self)
        self.top_frame.grid(row=0, column=0, sticky="nwse")

        # Inside Top Frame L2
        self.days = DaySelector(self.top_frame)
        self.days.grid(row=0, column=0, rowspan=3, sticky="nwse")
        self.right_frame = CTkFrame(self.top_frame)
        self.right_frame.grid(row=0, column=1, sticky="w")

        # Inside Right Frame L3
        self.path = PathSelector(self.right_frame)
        self.path.grid(row=0, column=0, padx=10, pady=10, sticky="nwse")
        self.week = WeekSelector(self.right_frame)
        self.week.grid(row=1, column=0, padx=10, pady=10, sticky="nwse")
        self.upload = UploadFrame(self.right_frame)
        self.upload.grid(row=2, column=0, padx=10, pady=10, sticky="nwse")

        # Bottom Frame L1
        self.copy = CopyFrame(self)
        self.copy.grid(row=1, column=0, columnspan=2, sticky="n")

        self.controller = None

    def reset(self):
        self.upload.reset_texts()
        self.copy.reset_texts()

    @staticmethod
    def show_error(title, msg, tb):
        err_msg = f"{msg}\n\n{tb}"
        showerror(title, err_msg)

    def set_controller(self, controller):
        self.controller = controller
        self.days.controller = controller
        self.path.controller = controller
        self.week.controller = controller
        self.upload.controller = controller
        self.copy.controller = controller
