from multiprocessing import Process, Queue, freeze_support
from pathlib import Path
from queue import Empty
from tkinter import Tk, Frame, Label, Checkbutton, BooleanVar, filedialog, Button, StringVar, Entry, Spinbox, IntVar
from tkinter.ttk import Progressbar

from uploader import get_log_metas, upload_file, get_glenna_line


def upload_file_wrapper(log_metas, q):
    for file in log_metas:
        upload_file(file, q)


class LogUploaderUI(Tk):
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
        self.logPathLabel = Label(self.pathFrame, text="Path to the logs main folder:")
        self.logPathLabel.grid(column=0, row=0, sticky="W")
        self.logPathText = Entry(self.pathFrame, text=self.logPath, width=30)
        self.logPathText.grid(column=0, row=1, sticky="W")
        self.pathButton = Button(self.pathFrame, text="Select Folder", command=self.browse_button)
        self.pathButton.grid(column=1, row=1, sticky="W")

        # Past Frame
        self.pastLabel = Label(self.pastFrame, text="Look into the past. (0 = this week)").grid(row=0, sticky="W")
        self.pastWeeks = IntVar()
        self.pastSpin = Spinbox(self.pastFrame, textvariable=self.pastWeeks, from_=0, to=3, width=5)
        self.pastSpin.grid(row=1, sticky="W")

        # Start Frame
        self.startButton = Button(self.startFrame, text="Start Upload", command=self.start)
        self.startButton.grid(column=0, row=0, sticky="W")
        self.progress = Progressbar(self.startFrame, length=200, mode="determinate")
        self.progress.grid(column=0, row=1, sticky="W", pady=10)
        self.to_clipboard = []

        # Output Frame
        self.outButton = Button(self.bottomFrame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.outButton.grid(column=0, row=0, sticky="W")

    def start(self):
        self.startButton.configure(text="Uploading")
        self.outButton.configure(text="Copy to Clipboard")
        self.to_clipboard = []
        self.raidDays = [day for i, day in enumerate(self.weekdays) if self.weekdaysVar[i].get()]
        log_metas = get_log_metas(self.logPath.get(), self.raidDays, self.pastWeeks.get(), 300000)
        if len(log_metas) == 0:
            self.progress["maximum"] = 1
            self.progress["value"] = 1
        else:
            self.progress["value"] = 0
            self.progress["maximum"] = len(log_metas)
            self.upload(log_metas)

    def upload(self, log_metas):
        q = Queue(50)
        p = Process(target=upload_file_wrapper, args=(log_metas, q))
        p.start()
        self.update()
        self.check_queue(q, p, len(log_metas))
        # while p.is_alive() and len(self.to_clipboard) != len(log_metas):
        #     self.after(3000, self.check_queue(q, p))
        #     self.update()

    def check_queue(self, q, p, meta_len):
        try:
            glenna_line = get_glenna_line(q.get(block=False))
        except Empty:
            self.queue_stopper(q, p, meta_len)
        else:
            if glenna_line:
                self.to_clipboard.append(glenna_line)
            self.progress["value"] += 1
            self.queue_stopper(q, p, meta_len)

    def queue_stopper(self, q, p, meta_len):
        if p.is_alive() and len(self.to_clipboard) != meta_len:
            self.after(3000, self.check_queue, q, p, meta_len)
            self.update()
        elif p.is_alive() and len(self.to_clipboard) == meta_len:
            p.join(5)
            self.check_queue(q, p, meta_len)
        elif not p.is_alive():
            self.startButton.configure(text="Done")

    def copy_to_clipboard(self):
        self.clipboard_clear()
        for log_line in self.to_clipboard:
            self.update()
            self.clipboard_append(log_line + "\n")
        self.outButton.configure(text="Copied")

    def browse_button(self):
        self.logPath.set(filedialog.askdirectory())


if __name__ == "__main__":
    freeze_support()
    app = LogUploaderUI()
    app.mainloop()
