from queue import Queue, Empty
from threading import Thread, active_count
from tkinter import filedialog, messagebox
from typing import List

from log import Log
from log_collector import LogCollector
from uploader import Uploader
from user_interface import UserInterface

ui: UserInterface

uploaded_logs = []
upload_thread = Thread()
upload_queue = Queue()
after_id = 0


def logic_ui(gui):
    global ui
    ui = gui


def click_upload():
    t = Thread(target=_click_upload)
    t.daemon = True
    global upload_thread
    upload_thread = t
    t.start()


def _click_upload():
    ui.uploadBtn.configure(text="Collecting", state="disabled")
    raid_days = [day for i, day in enumerate(ui.weekdays) if ui.weekdaysVar[i].get()]
    logs = LogCollector(ui.logPath.get(), raid_days, ui.week_delta.get(), 200000, ui.fracVar.get())
    logs = logs.collect()

    if not logs:
        # Finish, since nothing was uploaded
        ui.uploadPrg["maximum"] = 1
        ui.uploadPrg["value"] = 1
        ui.uploadBtn.configure(text="No logs found", state="normal")
    else:
        # Set up the progressbar
        ui.uploadPrg["value"] = 0
        ui.uploadPrg["maximum"] = len(logs)
        # Start the Log Upload
        _start_upload(logs)


def _start_upload(logs: List[Log]):
    ui.uploadBtn.configure(text="Uploading")
    global uploaded_logs, upload_queue
    uploaded_logs = []
    upload_queue = Queue(len(logs))
    up = Uploader(upload_queue)
    up.parallel_upload(logs)
    check_queue(up, len(logs))


def check_queue(up: Uploader, logs_len: int):
    print(active_count())
    try:
        uploaded_logs.append(str(upload_queue.get(block=False)))
    except Empty:
        pass
    else:
        ui.uploadPrg["value"] += 1

    if len(uploaded_logs) == logs_len:
        ui.uploadBtn.configure(text="Done")
    elif up.failed:
        on_upload_failure(up)
    else:
        global after_id
        after_id = ui.after(1000, check_queue, up, logs_len)


def on_upload_failure(up: Uploader):
    fail_string = ""
    for fail in up.failed_logs:
        fail_string += f"{fail.boss} "
    if messagebox.askretrycancel("UploadError", f"Failed on file(s): {fail_string}"):
        _start_upload(up.failed_logs)
    else:
        _reset()


def _reset():
    ui.uploadBtn.configure(text="Start Upload", state="normal")
    ui.copyButton.configure(text="Copy to Clipboard")
    ui.after_cancel(after_id)


def click_copy():
    ui.clipboard_clear()
    for log_line in uploaded_logs:
        ui.update()
        ui.clipboard_append(log_line + "\n")
    ui.copyButton.configure(text="Copied")


def click_browse():
    ui.logPath.set(filedialog.askdirectory())
