from multiprocessing import Process, Queue
from pathlib import Path
from queue import Empty
from tkinter import Tk, Frame, Label, Checkbutton, BooleanVar, filedialog, Button, StringVar, Entry, Spinbox, IntVar, \
    Text, INSERT
from tkinter.ttk import Progressbar

from uploader import get_log_metas, upload_file, get_glenna_line


def upload_file_wrapper(log_metas, q):
    for file in log_metas:
        upload_file(file, q)


class Uploader(Tk):
    def __init__(self):
        super().__init__()
        self.title("Glenna Upload Utility")
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
        self.raidDays = []
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
        self.to_clipboard = []

        # Output Frame
        self.outText = Text(self.bottomFrame, height=3, width=45)
        # self.outText.grid(column=0, row=0, sticky="W")
        self.outButton = Button(self.bottomFrame, text="Copy to clipboard", command=self.copy_to_clipboard)
        self.outButton.grid(column=0, row=0, sticky="W")

    def start(self):
        self.raidDays = [day for i, day in enumerate(self.weekdays) if self.weekdaysVar[i].get()]
        log_metas = get_log_metas(self.logPath.get(), self.raidDays, self.pastWeeks.get(), 400000)
        if len(log_metas) == 0:
            self.progress["maximum"] = 1
            self.progress["value"] = 1
        else:
            self.progress["value"] = 1
            self.progress["maximum"] = len(log_metas) + 1
            self.upload(log_metas)

    def upload(self, log_metas):
        q = Queue(50)
        p = Process(target=upload_file_wrapper, args=(log_metas, q))
        p.start()
        self.update()
        while p.is_alive() and len(self.to_clipboard) != len(log_metas):
            self.after(1000, self.check_queue(q, p))
            self.update()
        p.join(5)

    def check_queue(self, q, p):
        try:
            glenna_line = get_glenna_line(q.get(block=False))
        except Empty:
            if p.is_alive():
                self.after(1000, self.check_queue, q, p)
                self.update()
        else:
            self.to_clipboard.append(glenna_line)
            self.update_text(glenna_line)
            self.progress["value"] += 1
            if p.is_alive():
                self.after(1000, self.check_queue, q, p)
                self.update()

    def update_text(self, text):
        print(text)
        self.outText.insert(INSERT, text + "\n")

    def copy_to_clipboard(self):
        self.clipboard_clear()
        for log_line in self.to_clipboard:
            self.update()
            self.clipboard_append(log_line + "\n")
        self.outButton.configure(text="Copied")

    def browse_button(self):
        self.logPath.set(filedialog.askdirectory())


if __name__ == "__main__":
    app = Uploader()
    app.mainloop()
