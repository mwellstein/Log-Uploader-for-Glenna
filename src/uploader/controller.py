"""
Handle the inputs from the user interface.
All functions (mostly clicks and help functions) are down below.
The only ui changes will be labels and progress on the progressbar.
"""
from queue import Queue
from threading import Thread

from logic.collector import LogCollector
from logic.uploader import Uploader



class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.collect_thread = Thread(target=self.model.collect_logs, args=(self, path, days, week_delta, raids, strikes, fracs))
        self.collect_thread.daemon = True
        self.collect_thread.start()
        self.upload_threads = [Thread(target=self.model.upload_log, args=(self,)) for _ in range(6)]
        for thread in self.upload_threads:
            thread.start()


class Controller2:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.collect_thread = None
        self.collect_queue = Queue()
        self.collect_size_queue = Queue()
        self.upload_threads = [Thread(target=self._upload_log) for _ in range(6)]
        for thread in self.upload_threads:
            thread.start()
        self.uploaded_queue = Queue()
        self.failed_up_queue = Queue()
        self.log_count = 0

    def show_error(self, title, msg, tb):
        self.view.show_error(title, msg, tb)

    def _upload_log(self):
        # Threaded Function - used by self.upload_threads
        uploader = Uploader(self)
        # TODO: Exception in Uploader can't access dps_report_error
        # leading to a exception error lmao
        # make sure it is accessible AND find out what is causing
        # uploads to fail
        # Maybe a system in place to retry or show status codes and dps_report log
        block_temp = False
        while True:
            log = self.collect_queue.get()

            if log is None:
                self.collect_queue.put(None)
                return

            if block_temp:
                return
            else:
                block_temp = True
            response = uploader.upload(log)
            log.link = response["permalink"]

            self.uploaded_queue.put(log)

    def check_status(self):
        """Check if the collection thread is still alive, else start upload."""
        if self.collect_thread is None:
            raise TypeError("Expected a thread, not None.")

        self.log_count = self.collect_size_queue.qsize()
        self.view.update_upload_label(f"Collected: {self.log_count} logs")

        if not self.collect_thread.is_alive():  # done collecting
            if self.log_count == 0:
                return
            step_size = 1 / self.log_count
            amount_uploaded = self.uploaded_queue.qsize()
            self.view.update_progress(step_size * amount_uploaded)

        # if all upload threads are finished stop checking status
        uploads_running = any([thread.is_alive() for thread in self.upload_threads])
        if uploads_running:
            self.view.after(100, self.check_status)

    def handle_upload_button(self):
        print("Getting UI config state")
        path = self.view.path.get_path()

        days = self.view.days.get_selected_days()
        week_delta = self.view.week.get_week_delta()
        raids, strikes, fracs = self.view.upload.get_checked_categories()

        print("Collecting Logs")
        collector = LogCollector(self, path, days, week_delta, raids, strikes, fracs)
        self.collect_thread = Thread(target=collector.collect)
        self.collect_thread.daemon = True
        self.collect_thread.start()

        self.view.after(0, self.check_status)

    def clear(self):
        pass

