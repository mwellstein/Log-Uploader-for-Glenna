import logging

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
        """Instantiate a LogCollector with the given parameters and collect latest logs."""
        # If we are "mid-run" and just missing some uploads, no need to collect logs again => less ui freezing
        logging.info("Starting collection handling")
        if self.missing_uploads:
            return

        logging.info("Starting collection process")
        try:
            collector = LogCollector(controller, path, days, week_delta, raids, strikes, fracs)
        except Exception as e:
            logging.error(e)
            raise e
        self.collected_logs = collector.collect()
        self.collected_count = len(self.collected_logs)
        logging.info(f"Collected {self.collected_count} logs")
        self.missing_uploads = self.collected_logs

    async def upload_logs(self, controller):
        uploader = Uploader(controller, self.missing_uploads)

        # Reset missing_count to 0, else it will possibly increment above collect_counts and it + uploaded != collected
        self.missing_count = 0

        async for log in uploader.upload():
            try:
                if not log:
                    self.missing_count += 1
                    logging.debug("+1 Missing Log counted")
                    self.controller.update_ui_depending_on_upload_count(self.uploaded_count)
                    continue
                self.uploaded_logs.append(log)
                self.uploaded_count += 1
                self.missing_uploads = [missing_log for missing_log in self.missing_uploads if missing_log.boss != log.boss]
                logging.debug(f"Removed {log.boss} from missing. Collected {self.collected_count}, "
                              f"Uploaded: {self.uploaded_count}, "
                              f"Missing: {len(self.missing_uploads)}")

                if self.controller:
                    self.controller.update_ui_depending_on_upload_count(self.uploaded_count)
            except Exception as e:
                logging.error(f"Unexpected Error collecting uploads {log.boss}: {str(e)}")
                raise e

    def reset(self):
        logging.debug("Resetting model properties")
        self.collected_logs = []
        self.collected_count = 0
        self.uploaded_logs = []
        self.uploaded_count = 0
        self.missing_uploads = []

    def set_controller(self, controller):
        self.controller = controller
