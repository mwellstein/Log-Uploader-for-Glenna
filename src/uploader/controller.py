"""
Handle the inputs from the user interface.
All functions (mostly clicks and help functions) are down below.
The only ui changes will be labels and progress on the progressbar.
"""
import asyncio
import logging
import threading
from queue import Queue
from threading import Thread

from logic.collector import LogCollector
from logic.uploader import Uploader


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_error(self, title, msg, tb):
        """Open an error box with error information"""
        self.view.show_error(title, msg, tb)

    def handle_upload_button(self):
        logging.info("Upload was clicked - Collecting config information")
        path: str = self.view.path.get_path()

        days: [str] = self.view.days.get_selected_days()
        week_delta = self.view.week.get_week_delta()
        raids, strikes, fracs = self.view.upload.get_checked_categories()

        logging.info("Telling model to collect Logs")
        self.model.collect_logs(self, path, days, week_delta, raids, strikes, fracs)
        logging.info("Telling model to upload Logs")

        # Tkinter doesn't support async, so lets workaround it
        async_loop = asyncio.new_event_loop()
        t = threading.Thread(target=self.start_loop, args=(async_loop,))
        t.start()

        asyncio.run_coroutine_threadsafe(self.model.upload_logs(self), async_loop)
        # self.model.upload_logs(self)

    def handle_copy_button(self):
        logging.info("Copy was clicked")
        if not self.model.uploaded_logs:
            logging.info("No logs to copy")
            return
        self.view.clipboard_clear()
        for log in self.model.uploaded_logs:
            # self.view.update()
            self.view.clipboard_append(str(log) + "\n")
        logging.info(f"Logs added to clipboard: ~{len(self.model.uploaded_logs)}")
        self.view.copy.copyButton.configure(text="Copied")

    @staticmethod
    def start_loop(async_loop):
        asyncio.set_event_loop(async_loop)
        async_loop.run_forever()
