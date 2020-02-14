from pathlib import Path
from tkinter import Tk, BooleanVar, StringVar, IntVar
from tkinter.ttk import Progressbar, Frame, Label, Checkbutton, Button, Entry, Spinbox
from interface_logic import *


class UserInterface(Tk):
    def __init__(self):
        super().__init__()
        self.title("Log Uploader for Glenna")
        self.geometry("500x350")

        # Top Frame
        self.topFrame = Frame()
        self.topFrame.grid(column=0, row=0, sticky="NW", padx=20, pady=20)
        self.leftFrame = Frame(self.topFrame)
        self.leftFrame.grid(column=0, row=0, sticky="NW", padx=20)
        self.rightFrame = Frame(self.topFrame)
        self.rightFrame.grid(column=1, row=0, sticky="NW", padx=30)

        # Bottom Frame
        self.bottomFrame = Frame()
        self.bottomFrame.grid(row=1)

        # Left Frame
        self.weekLabel = Label(self.leftFrame, text="When did you raid?")
        self.weekLabel.grid(row=0)
        self.raid_days = []
        self.weekdaysVar = []
        self.weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(self.weekdays):
            day_in = BooleanVar()
            day_button = Checkbutton(self.leftFrame, text=day, var=day_in)
            day_button.grid(row=i + 1, sticky="W")
            self.weekdaysVar.append(day_in)

        # Right Frames
        self.pathFrame = Frame(self.rightFrame)
        self.pathFrame.grid(column=0, row=0, sticky="W")
        self.pastFrame = Frame(self.rightFrame)
        self.pastFrame.grid(column=0, row=1, sticky="W")
        self.startFrame = Frame(self.rightFrame)
        self.startFrame.grid(column=0, row=2, sticky="W", pady=30)

        # Path Frame
        self.logPath = StringVar(
            value=Path().home() / "Documents" / "Guild Wars 2" / "addons" / "arcdps" / "arcdps.cbtlogs")
        self.logPathLabel = Label(self.pathFrame, text="Path to the logs main folder:")
        self.logPathLabel.grid(column=0, row=0, sticky="W")
        self.logPathText = Entry(self.pathFrame, text=self.logPath, width=30)
        self.logPathText.grid(column=0, row=1, sticky="W")
        self.pathButton = Button(self.pathFrame, text="Select Folder", command=click_browse)
        self.pathButton.grid(column=1, row=1, sticky="W")

        # Past Frame
        self.pastLabel = Label(self.pastFrame, text="Look into the past. (0 = this week)").grid(row=0, sticky="W")
        self.week_delta = IntVar()
        self.pastSpin = Spinbox(self.pastFrame, textvariable=self.week_delta, from_=0, to=99, width=5)
        self.pastSpin.grid(row=1, sticky="W")

        # Start Frame
        self.startButton = Button(self.startFrame, text="Start Upload", command=click_upload)
        self.startButton.grid(column=0, row=0, sticky="W")
        self.fracVar = BooleanVar()
        self.fracCheck = Checkbutton(self.startFrame, text="Upload Fractals", var=self.fracVar)
        self.fracCheck.grid(column=0, row=0, sticky="E")
        self.progress = Progressbar(self.startFrame, length=200, mode="determinate")
        self.progress.grid(column=0, row=1, sticky="W", pady=10)
        self.uploaded_logs = []

        # Copy Frame
        self.copyButton = Button(self.bottomFrame, text="Copy to Clipboard", command=click_copy)
        self.copyButton.grid(column=0, row=0, sticky="W")


if __name__ == "__main__":
    window = UserInterface()
    logic_ui(window)
    window.protocol("WM_DELETE_WINDOW", lambda: print("Hello"))
    window.mainloop()
