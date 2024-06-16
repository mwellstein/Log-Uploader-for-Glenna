import logging
from queue import Queue
from .collector import LogCollector
from .uploader import Uploader


class Model:
    def __init__(self):
        self.collect_queue = Queue()
        self.collect_size_queue = Queue()
        self.uploaded_queue = Queue()
        self.failed_up_queue = Queue()
        self.collected_logs = []
        self.collected_count = 0
        self.uploaded_logs = []
        self.uploaded_count = 0

        self.controller = None

    def collect_logs(self, controller, path, days, week_delta, raids, strikes, fracs):
        """Instantiate a LogCollector with the given parameters and """
        collector = LogCollector(controller, path, days, week_delta, raids, strikes, fracs)
        self.collected_logs = collector.collect()
        self.collected_count = len(self.collected_logs)
        logging.info(f"Collected {self.collected_count} logs")

    async def upload_logs(self, controller):
        uploader = Uploader(controller, self.collected_logs)

        async for log in uploader.upload():
            self.uploaded_logs.append(log)
            self.uploaded_count += 1
            if self.controller:
                self.controller.update_ui_depending_on_upload_count(self.uploaded_count)

    def set_controller(self, controller):
        self.controller = controller
