import logging
from queue import Queue
from .collector import LogCollector
from .uploader import Uploader


class Model:
    def __init__(self):
        self.collected_logs = []
        self.collected_count = 0
        self.uploaded_logs = []
        self.uploaded_count = 0
        self.missing_uploads = []  # Collected - Uploaded
        self.missing_count = 0  # Missing + uploaded counts == collected count => done

        self.controller = None

    def collect_logs(self, controller, path, days, week_delta, raids, strikes, fracs):
        """Instantiate a LogCollector with the given parameters and """
        collector = LogCollector(controller, path, days, week_delta, raids, strikes, fracs)
        self.collected_logs = collector.collect()
        self.collected_count = len(self.collected_logs)
        logging.info(f"Collected {self.collected_count} logs")

        self.missing_uploads = self.collected_logs

    async def upload_logs(self, controller):
        uploader = Uploader(controller, self.missing_uploads)

        async for log in uploader.upload():
            if not log:
                self.missing_count += 1
            self.uploaded_logs.append(log)
            self.uploaded_count += 1
            self.missing_uploads = [missing_log for missing_log in self.missing_uploads if missing_log.boss != log.boss]
            logging.debug(f"Removed {log.boss} from missing. Collected {self.collected_count}, "
                          f"Missing: {len(self.missing_uploads)}")

            if self.controller:
                self.controller.update_ui_depending_on_upload_count(self.uploaded_count)

    def reset(self):
        logging.debug("Resetting model properties")
        self.collected_logs = []
        self.collected_count = 0
        self.uploaded_logs = []
        self.uploaded_count = 0
        self.missing_uploads = []

    def set_controller(self, controller):
        self.controller = controller
