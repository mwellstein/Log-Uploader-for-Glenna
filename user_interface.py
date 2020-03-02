from pathlib import Path
from tkinter import Tk, BooleanVar, StringVar, IntVar
from tkinter.ttk import Progressbar, Frame, Label, Checkbutton, Button, Entry, Style, Radiobutton

from interface_logic import *


class UserInterface(Tk):
    def __init__(self):
        super().__init__()
        self.title("Log Uploader for Glenna")
        self.geometry("500x350")

        self.style = Style()
        print(self.style.theme_names())
        self.style.theme_use("xpnative")
        self.style.configure("HeadLabel.TLabel", font=("Helvetica", 12))
        # Top Frame
        self.topFrame = Frame()
        self.topFrame.place(relheight=0.7, relwidth=1.0)
        self.leftFrame = Frame(self.topFrame)
        self.leftFrame.place(relheight=1.0, relwidth=0.3)
        self.rightFrame = Frame(self.topFrame)
        self.rightFrame.place(relheight=1.0, relwidth=0.7, relx=0.3, rely=0.07)

        # Bottom Frame
        self.bottomFrame = Frame()
        self.bottomFrame.place(relheight=0.3, relwidth=1.0, rely=0.7)

        # Left Frame
        self.weekLabel = Label(self.leftFrame, text="When did you raid?", style="HeadLabel.TLabel")
        self.weekLabel.place(relx=0.1, rely=0.09)
        self.weekdaysVar = []
        self.weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(self.weekdays):
            day_in = BooleanVar()
            day_button = Checkbutton(self.leftFrame, text=day, var=day_in)
            day_button.place(relx=0.1, rely=0.2 + 0.1 * i)
            self.weekdaysVar.append(day_in)

        # Right Frames
        self.pathFrame = Frame(self.rightFrame)
        self.pathFrame.place(relheight=0.25, relwidth=1.0, rely=0.0)
        self.pastFrame = Frame(self.rightFrame)
        self.pastFrame.place(relheight=0.25, relwidth=1.0, rely=0.25)
        self.startFrame = Frame(self.rightFrame)
        self.startFrame.place(relheight=0.5, relwidth=1.0, rely=0.5)

        # Path Frame
        self.logPath = StringVar(
            value=Path().home() / "Documents" / "Guild Wars 2" / "addons" / "arcdps" / "arcdps.cbtlogs")
        self.logPathLabel = Label(self.pathFrame, text="Path to log directory:", style="HeadLabel.TLabel")
        self.logPathLabel.place(relx=0.1, rely=0.1)
        self.logPathText = Entry(self.pathFrame, text=self.logPath, width=30)
        self.logPathText.place(relwidth=0.5, relx=0.1, rely=0.5)
        self.pathButton = Button(self.pathFrame, text="Select Folder", command=click_browse)
        self.pathButton.place(relx=0.61, rely=0.45)

        # Past Frame
        self.pastLabel = Label(self.pastFrame, text="Select week to upload:", style="HeadLabel.TLabel")
        self.pastLabel.place(relx=0.1, rely=0.1)
        self.week_delta = IntVar()
        self.weekRadio1 = Radiobutton(self.pastFrame, text="Current", variable=self.week_delta, value=0)
        self.weekRadio1.place(relx=0.1, rely=0.5)
        self.weekRadio2 = Radiobutton(self.pastFrame, text="Last", variable=self.week_delta, value=1)
        self.weekRadio2.place(relx=0.33, rely=0.5)
        self.weekRadio3 = Radiobutton(self.pastFrame, text="Second-last", variable=self.week_delta, value=2)
        self.weekRadio3.place(relx=0.5, rely=0.5)

        # Start Frame
        self.uploadBtn = Button(self.startFrame, text="Start Upload", command=click_upload)
        self.uploadBtn.place(relx=0.1, rely=0.1)
        self.fracVar = BooleanVar()
        self.fracCheck = Checkbutton(self.startFrame, text="Upload Fractals", var=self.fracVar)
        self.fracCheck.place(relx=0.38, rely=0.05)
        self.reupVar = BooleanVar()
        self.reuploadCheck = Checkbutton(self.startFrame, text="Reupload", var=self.reupVar)
        self.reuploadCheck.place(relx=0.38, rely=0.2)
        self.uploadPrg = Progressbar(self.startFrame, length=200, mode="determinate")
        self.uploadPrg.place(relx=0.1, rely=0.4)

        # Copy Frame
        self.copyButton = Button(self.bottomFrame, text="Copy to Clipboard", command=click_copy)
        self.copyButton.place(relx=0.5, rely=0.2, anchor="n")
        self.clearCacheButton = Button(self.bottomFrame, text="Clear Uploaded", command=click_clear_cache)
        self.clearCacheButton.place(relx=0.5, rely=0.6, anchor="n")


if __name__ == "__main__":
    window = UserInterface()
    logic_ui(window)
    window.protocol("WM_DELETE_WINDOW", lambda: window.destroy())
    window.mainloop()
