from threading import Thread
from queue import Queue, Empty
from log_collector import LogCollector
from uploader import Uploader
from user_interface import UserInterface
from tkinter import filedialog

ui: UserInterface

uploaded_logs = []
upload_thread = Thread()
upload_queue = Queue()


def logic_ui(gui):
    global ui
    ui = gui


def click_upload():
    t = Thread(target=_click_upload)
    t.daemon = True
    global upload_thread
    upload_thread = t
    t.start()


def click_reset():
    t = Thread(target=_click_upload)
    t.daemon = True
    t.start()


def _click_upload():
    global uploaded_logs, upload_queue
    if uploaded_logs and upload_thread and upload_queue:
        _reset()
    ui.startButton.configure(text="Collecting")
    raid_days = [day for i, day in enumerate(ui.weekdays) if ui.weekdaysVar[i].get()]
    logs = LogCollector(ui.logPath.get(), raid_days, ui.week_delta.get(), 200000, ui.fracVar.get())
    logs = logs.collect()

    if not logs:
        # Finish, since nothing was uploaded
        ui.progress["maximum"] = 1
        ui.progress["value"] = 1
        ui.startButton["text"] = "No logs found."
    else:
        # Set up the progressbar
        ui.progress["value"] = 0
        ui.progress["maximum"] = len(logs)
        # Start the Log Upload
        ui.startButton.configure(text="Uploading")
        uploaded_logs = []
        upload_queue = Queue(len(logs))
        up = Uploader(upload_queue)
        up.parallel_upload(logs)
        check_queue()


def check_queue():
    try:
        uploaded_logs.append(str(upload_queue.get(block=False)))
    except Empty:
        pass
    else:
        ui.progress["value"] += 1
    if not upload_thread.is_alive():
        ui.startButton.configure(text="Done")
    ui.after(1000, check_queue)


def _reset():
    ui.startButton.configure(text="Start Upload")
    ui.copyButton.configure(text="Copy to Clipboard")
    global uploaded_logs, upload_thread, upload_queue
    uploaded_logs.clear()
    upload_thread = Thread()
    upload_queue = Queue()


def click_copy():
    ui.clipboard_clear()
    for log_line in uploaded_logs:
        ui.update()
        ui.clipboard_append(log_line + "\n")
    ui.copyButton.configure(text="Copied")


def click_browse():
    ui.logPath.set(filedialog.askdirectory())
