from queue import Queue


class Model:
    def __init__(self):
        self.collect_queue = Queue()
        self.collect_size_queue = Queue()
        self.uploaded_queue = Queue()
        self.failed_up_queue = Queue()
        self.log_count = 0

    def upload_log(self, controller):
        # Threaded Function - used by self.upload_threads
        uploader = Uploader(controller)
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

    def collect_logs(self, controller, path, days, week_delta, raids, strikes, fracs):
        collector = LogCollector(controller, path, days, week_delta, raids, strikes, fracs)
        collector.collect()

    # ... other methods ...
