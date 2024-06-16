from customtkinter import CTkFrame, CTkLabel, StringVar, CTkEntry, CTkButton
from tkinter import filedialog
from pathlib import Path
import ctypes.wintypes


class PathSelector(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # https://stackoverflow.com/a/30924555
        personal = 5  # My Documents
        type_current = 0  # Get current, not default value

        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, personal, None, type_current, buf)
        # -----

        # Create an inner frame
        inner_frame = CTkFrame(self, fg_color=("gray86", "gray17"))
        inner_frame.pack(anchor="center", pady=10)  # Center the inner frame

        arc_folder = (Path(buf.value) / "Guild Wars 2" / "addons" / "arcdps" / "arcdps.cbtlogs")
        self.logPath = StringVar(value=str(arc_folder))

        self.logPathLabel = CTkLabel(inner_frame, text="Path to log directory:")
        self.logPathLabel.grid(row=0, column=0, sticky="w")

        self.logPathText = CTkEntry(inner_frame, textvariable=self.logPath, width=325)
        self.logPathText.grid(row=1, column=0, sticky="w")
        self.pathButton = CTkButton(inner_frame, text="Change", command=self.select_path, width=100)
        self.pathButton.grid(row=1, column=1, sticky="w")

        self.controller = None

    def select_path(self):
        """
        Open up filedialog to get main log directory
        """
        self.logPath.set(filedialog.askdirectory())

    def get_path(self) -> str:
        return self.logPath.get()
