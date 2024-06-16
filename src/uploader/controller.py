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

        # If nothing was collected
        if self.model.collected_count == 0:
            self.view.upload.change_upload_text("No Logs found")
            self.view.update()
            delay = 1500
            self.view.after(delay, self.view.reset)
            self.view.after(delay, self.view.upload.toggle_button_state)
            return

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
            self.view.after(1500, self.view.copy.reset_texts)
            return
        self.view.clipboard_clear()
        for log in self.model.uploaded_logs:
            self.view.update()
            self.view.clipboard_append(str(log) + "\n")
        logging.info(f"Logs added to clipboard: ~{len(self.model.uploaded_logs)}")
        self.view.copy.change_copy_button_text(f"Copied {len(self.model.uploaded_logs)} Logs")

    def handle_reset_button(self):
        logging.info("Reset button was pressed. Stopping tasks.")

        self.view.copy.change_reset_button_text("Resetting - One Minute")
        self.view.upload.toggle_button_state(disable=True)

        self.model.reset()
        self.view.reset()
        self.view.update()

        # Finishes current upload, then stops remaining tasks
        if self.async_loop:
            # Only if there already is a loop
            self.async_tasks.cancel()
            self.async_loop.call_soon_threadsafe(self.async_loop.stop)

        self.check_reset_status()

    def check_reset_status(self):
        if self.async_loop and self.async_loop.is_running():
            self.view.after(250, self.check_reset_status)
        else:
            self.view.copy.change_reset_button_text("Reset done")
            self.view.update()

            delay = 1500
            self.view.after(delay, self.view.copy.reset_reset_button)
            self.view.after(delay, self.view.upload.toggle_button_state)

    def update_ui_depending_on_upload_count(self, up_count):
        self.view.copy.update_copy_tooltip_count(up_count)
        self.view.upload.update_progress(up_count)

        if self.model.missing_count and self.model.missing_count + self.model.uploaded_count == self.model.collected_count:
            self.view.upload.change_upload_text("Missing some!")
            self.view.upload.update_upload_tooltip(f"Missing {self.model.missing_count} Logs. Click to try again.")
            self.view.upload.toggle_button_state()  # Activate again if done, but some Logs are missing

        if len(self.model.missing_uploads) == 0:
            self.view.upload.change_upload_text("Upload done!")
            self.view.upload.update_upload_tooltip("All found logs should be uploaded! Reset to upload again.")
            self.view.upload.toggle_button_state()  # Activate again once done

        self.view.update()

    @staticmethod
    def start_loop(async_loop):
        asyncio.set_event_loop(async_loop)
        async_loop.run_forever()
