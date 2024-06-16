"""
Handle the inputs from the user interface.
All functions (mostly clicks and help functions) are down below.
The only ui changes will be labels and progress on the progressbar.
"""
import asyncio
import logging
from threading import Thread


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.async_loop = None
        self.async_thread: Thread | None = None
        self.async_tasks = None

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
        self.async_loop = asyncio.new_event_loop()
        self.async_thread = Thread(target=self.start_loop, args=(self.async_loop,))
        self.async_thread.start()

        self.async_tasks = asyncio.run_coroutine_threadsafe(self.model.upload_logs(self), self.async_loop)

    def handle_copy_button(self):
        logging.info("Copy was clicked")
        if not self.model.uploaded_logs:
            logging.info("No logs to copy")
            self.view.copy.change_copy_button_text("No Logs yet")
            return
        self.view.clipboard_clear()
        for log in self.model.uploaded_logs:
            self.view.update()
            self.view.clipboard_append(str(log) + "\n")
        logging.info(f"Logs added to clipboard: ~{len(self.model.uploaded_logs)}")
        self.view.copy.change_copy_button_text(f"Copied {len(self.model.uploaded_logs)} Logs")

    def handle_reset_button(self):

        # TODO: A list that saves all already successfully uploaded logs
        # Pressing Upload again will only upload the missing ones, unless reupload is check!
        # => Less need to error handle stuff to make a missing list
        # Reset should then reset this list and stop the current tasks.
        # Stop the async loop
        logging.info("Cancel button was pressed. Stopping tasks.")

        # Finishes current upload, then stops remaining tasks
        self.async_tasks.cancel()
        self.async_loop.call_soon_threadsafe(self.async_loop.stop)

    def update_ui_depending_on_upload_count(self, up_count):
        self.view.copy.update_copy_tooltip_count(up_count)
        self.view.upload.update_progress(up_count)

    @staticmethod
    def start_loop(async_loop):
        asyncio.set_event_loop(async_loop)
        async_loop.run_forever()
