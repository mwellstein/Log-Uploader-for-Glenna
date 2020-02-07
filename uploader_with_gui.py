from uploader import *
from tkinter import Tk, Frame, Label, Checkbutton, BooleanVar, filedialog, Button, StringVar, Entry, Spinbox, IntVar
from tkinter.ttk import Progressbar


class Uploader(Tk):
    def __init__(self):
        super().__init__()
        self.title("dps.report Upload Utility")
        self.geometry("500x300")
        self.leftFrame = Frame()
        self.leftFrame.grid(column=0, row=0, sticky="N", padx=20, pady=20)
        self.rightFrame = Frame()
        self.rightFrame.grid(column=1, row=0, sticky="NW", padx=20, pady=20)

        # Left Frame
        self.weekLabel = Label(self.leftFrame, text="When did you raid?")
        self.weekLabel.grid(row=0)
        self.raidDays = []
        self.weekdaysVar = []
        self.weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(self.weekdays):
            print(i, day)
            day_in = BooleanVar()
            day_button = Checkbutton(self.leftFrame, text=day, var=day_in)
            day_button.grid(row=i + 1, sticky="W")
            self.weekdaysVar.append(day_in)

        # Right Frame
        self.pathFrame = Frame(self.rightFrame)
        self.pathFrame.grid(column=0, row=0, sticky="W")
        self.pastFrame = Frame(self.rightFrame)
        self.pastFrame.grid(column=0, row=1, sticky="W")
        self.startFrame = Frame(self.rightFrame)
        self.startFrame.grid(column=0, row=2, sticky="W", pady=30)

        # Path Frame
        self.logPath = StringVar()
        self.logPathLabel = Label(self.pathFrame, text="Select the main log folder")
        self.logPathLabel.grid(column=0, row=0, sticky="W")
        self.logPathText = Entry(self.pathFrame, text=self.logPath, width=30)
        self.logPathText.grid(column=0, row=1, sticky="W")
        self.pathButton = Button(self.pathFrame, text="Change", command=self.browse_button)
        self.pathButton.grid(column=1, row=1, sticky="W")

        # Past Frame
        self.pastLabel = Label(self.pastFrame, text="Go back to past weeks").grid(row=0, sticky="W")
        self.pastWeeks = IntVar()
        self.pastSpin = Spinbox(self.pastFrame, textvariable=self.pastWeeks, from_=0, to=3, width=5)
        self.pastSpin.grid(row=1, sticky="W")

        # Start Frame
        self.startButton = Button(self.startFrame, text="Start upload", command=self.start)
        self.startButton.grid(column=0, row=0, sticky="W")
        self.progress = Progressbar(self.startFrame, length=200, mode="determinate")
        self.progress.grid(column=0, row=1, sticky="W", pady=10)

    def start(self):
        self.progress["value"] = 0
        self.progress["maximum"] = 12  # Anzahl der Logs die hochgeladen werden
        self.raidDays = [day for i, day in enumerate(self.weekdays) if self.weekdaysVar[i].get()]
        print(self.weekdays)

    def upload_progress(self):
        pass

    def browse_button(self):
        self.logPath.set(filedialog.askdirectory())


app = Uploader()
app.mainloop()
