from multiprocessing import Process, freeze_support, Queue
from pathlib import Path
from queue import Empty
from tkinter import Tk, BooleanVar, filedialog, StringVar, IntVar
from tkinter.ttk import Progressbar, Frame, Label, Checkbutton, Button, Entry, Spinbox

from log_collector import LogCollector
from uploader import upload


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
        self.pathButton = Button(self.pathFrame, text="Select Folder", command=self.browse_button)
        self.pathButton.grid(column=1, row=1, sticky="W")

        # Past Frame
        self.pastLabel = Label(self.pastFrame, text="Look into the past. (0 = this week)").grid(row=0, sticky="W")
        self.week_delta = IntVar()
        self.pastSpin = Spinbox(self.pastFrame, textvariable=self.week_delta, from_=0, to=99, width=5)
        self.pastSpin.grid(row=1, sticky="W")

        # Start Frame
        self.startButton = Button(self.startFrame, text="Start Upload", command=self.click_start)
        self.startButton.grid(column=0, row=0, sticky="W")
        self.fracVar = BooleanVar()
        self.fracCheck = Checkbutton(self.startFrame, text="Upload Fractals", var=self.fracVar)
        self.fracCheck.grid(column=0, row=0, sticky="E")
        self.progress = Progressbar(self.startFrame, length=200, mode="determinate")
        self.progress.grid(column=0, row=1, sticky="W", pady=10)
        self.uploaded_logs = []

        # Copy Frame
        self.copyButton = Button(self.bottomFrame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copyButton.grid(column=0, row=0, sticky="W")

    def click_start(self):
        # Reset progress, kill processes, restart everything
        self._reset()
        self.startButton.configure(text="Uploading")
        self.uploaded_logs = []
        # [i for i, _ in enumerate(self.weekdays) if self.weekdaysVar[i].get()]
        # => No Need to compute weekday in Log(), still need day number
        self.raid_days = [day for i, day in enumerate(self.weekdays) if self.weekdaysVar[i].get()]

        logs = LogCollector(self.logPath.get(), self.raid_days, self.week_delta.get(), 200000, self.fracVar.get())
        logs = logs.collect()

        if not logs:
            # Finish, since nothing was uploaded
            self.progress["maximum"] = 1
            self.progress["value"] = 1
            self.startButton["text"] = "No logs found."
        else:
            # Set up the progressbar
            self.progress["value"] = 0
            self.progress["maximum"] = len(logs)
            # Start the Log Upload
            self.upload(logs)

    def _reset(self):
        self.copyButton.configure(text="Copy to Clipboard")
        # self.p.terminate()

    def click_reset(self):
        # Add button
        self.copyButton.configure(text="Copy to Clipboard")

    def upload(self, logs):
        q = Queue(len(logs))
        poi = Process(target=upload, args=(logs, q))
        poi.start()
        self.update()
        self.check_queue(q, poi, len(logs))

    def check_queue(self, q, p, meta_len):
        try:
            self.uploaded_logs.append(str(q.get(block=False)))
        except Empty:
            self.queue_stopper(q, p, meta_len)
        else:
            self.progress["value"] += 1
            self.queue_stopper(q, p, meta_len)

    def queue_stopper(self, q, p, meta_len):
        if p.is_alive() and len(self.uploaded_logs) != meta_len:
            self.after(3000, self.check_queue, q, p, meta_len)
            self.update()
        elif p.is_alive() and len(self.uploaded_logs) == meta_len:
            p.join(5)
            self.check_queue(q, p, meta_len)
        elif not p.is_alive():
            self.startButton.configure(text="Done")

    def copy_to_clipboard(self):
        self.clipboard_clear()
        for log_line in self.uploaded_logs:
            self.update()
            self.clipboard_append(log_line + "\n")
        self.copyButton.configure(text="Copied")

    def browse_button(self):
        self.logPath.set(filedialog.askdirectory())


if __name__ == "__main__":
    freeze_support()
    app = UserInterface()
    app.mainloop()
