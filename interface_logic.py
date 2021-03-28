"""
Handle the inputs from the user interface.
All functions (mostly clicks and help functions) are down below.
Only design changes will be label text and progressbar.
"""
from datetime import datetime
from queue import Queue, Empty
from threading import Thread
from tkinter import filedialog, messagebox
from typing import List

from log import Log
from log_collector import LogCollector
from uploader import Uploader
from user_interface import UserInterface

# To handle changes and variables of the ui, without circle import, assign the ui from user_interface
ui: UserInterface

# The current used container to collect the logs, the active thread that manages uploading
# and the queue to retrieve upload information
uploaded_logs = []
upload_thread = Thread()
upload_queue = Queue()
# After id is used to cancel ui.after(), which otherwise continues to call the given function
# Kinda unclear, since it shouldn't just be recursive calling, but calling it once only didn't work out
after_id = 0


def logic_ui(gui) -> None:
    """
    Set the UI to apply the logic to. Just a setter.
    :param gui: The gui-root after calling it in user_interfaces __main__ part
    """
    global ui
    ui = gui


def click_upload() -> None:
    """
    Handles the click to start upload. Opens a new thread to handle everything related to the upload.
    This new thread becomes the global upload_thread
    """
    # If no day was specified, default to today
    days_selected = [day for day in ui.weekdaysVar if day.get()]
    if not days_selected:
        today = datetime.now().weekday()
        ui.weekdaysVar[today].set(True)
    # Start thread for further work
    t = Thread(target=_click_upload)
    t.daemon = True
    global upload_thread
    upload_thread = t
    t.start()


def _click_upload() -> None:
    """
    Called in upload_thread, disables button, than collects all relevant setting in the ui and collects relevant logs.
    """
    ui.uploadBtn.configure(text="Collecting", state="disabled")
    raid_days = [day for i, day in enumerate(ui.weekdays) if ui.weekdaysVar[i].get()]
    to_up_logs = LogCollector(ui.logPath.get(), raid_days, ui.week_delta.get(), 200000, ui.fracVar.get())
    to_up_logs = to_up_logs.collect()

    # If Reupload is not True, go ahead and delete all upload log tasks, that were already uploaded
    if not ui.reupVar.get():
        for up_log in uploaded_logs:
            for i, to_up_log in enumerate(to_up_logs):
                if up_log.path == to_up_log.path:
                    to_up_logs.pop(i)
    else:
        # If reupload is True, reset uploaded logs
        uploaded_logs.clear()

    if not to_up_logs:
        # Finish, since nothing was uploaded
        ui.progressBar.adjustSize(0)
        # ui.uploadPrg["maximum"] = 1
        # ui.uploadPrg["value"] = 1
        ui.uploadButton.setText("No logs found.")
        # ui.uploadBtn.configure(text="No logs found", state="normal")
    else:
        # Set up the progressbar
        ui.uploadPrg["value"] = 0
        ui.uploadPrg["maximum"] = len(to_up_logs)
        # Start the Log Upload
        _start_upload(to_up_logs)


def _start_upload(logs: List[Log]) -> None:
    """
    Setting up the queue and Uploader instance. Than starts uploading and initialize checking of the queue.
    Not part of _click_upload to enable call from on_upload_failure with the remaining logs.
    :param logs: The logs that shall get uploaded by the uploader instance
    """
    # For multiple uploads, offset is needed, to ensure that check_queue finishes correctly len(uploaded) == len(to_up)
    reup_offset = len(uploaded_logs)

    ui.uploadBtn.configure(text="Uploading")
    global upload_queue
    upload_queue = Queue(len(logs))
    up = Uploader(upload_queue)
    up.parallel_upload(logs)
    check_queue(up, len(logs) + reup_offset)


def check_queue(up: Uploader, logs_len: int) -> None:
    """
    To have a working progressbar and kinda error handling from the upload subthreads the queue will be checked
    every second if it's filled. If not ignore, else update progressbar.
    Check if all logs got uploaded or if an error happened during the upload. Lastly call again after 1 second
    :param up: The Uploader instance to give it as kinda error handle for on_failure
    :param logs_len: The amount of logs that shall be uploaded to check for completing of the job
    """
    try:
        uploaded_log = upload_queue.get(block=False)
    except Empty:
        pass
    else:
        uploaded_logs.append(uploaded_log)
        ui.uploadPrg["value"] += 1

    if len(uploaded_logs) == logs_len:
        ui.uploadBtn.configure(text="Done", state="normal")
    elif up.failed:
        on_upload_failure(up)
    else:
        global after_id
        after_id = ui.after(1000, check_queue, up, logs_len)


def on_upload_failure(up: Uploader) -> None:
    """
    If a fail was detected, collect all fails, ask for retry. If not, reset program
    :param up: The Uploader instance, contains which logs failed
    """
    fail_string = ""
    for fail in up.failed_logs:
        fail_string += f"{fail.boss} "
    if messagebox.askretrycancel("UploadError", f"Failed on file(s): {fail_string}"):
        _start_upload(up.failed_logs)
    else:
        _reset()


def _reset() -> None:
    """
    As much reset as possible. Can't terminate threads easily, thus tried to cancel them by themself
    """
    ui.uploadBtn.configure(text="Start Upload", state="normal")
    ui.copyButton.configure(text="Copy to Clipboard")
    ui.after_cancel(after_id)


def click_copy() -> None:
    """
    Clears the Clipboard, then adds all links and try_count as new lines.
    """
    ui.clipboard_clear()
    for log_line in uploaded_logs:
        ui.update()
        ui.clipboard_append(str(log_line) + "\n")
    ui.copyButton.configure(text="Copied")


def click_browse() -> None:
    """
    Open up filedialog to get main log directory
    """
    ui.logPath.set(filedialog.askdirectory())


def click_clear_cache() -> None:
    """
    Clear all already uploaded logs. So that Copy to Clipboard will not copy those anymore.
    """
    uploaded_logs.clear()
