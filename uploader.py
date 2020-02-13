from http import HTTPStatus
from multiprocessing import Queue
from threading import Thread
from typing import List

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from log import Log


class Uploader:

    def __init__(self, queue):
        self.queue = queue

    def upload(self, logs: List[Log]):
        for log in logs:
            self._upload(log)

    def parallel_upload(self, logs: List[Log]):
        # Let's test how many connection we can manage.
        # One for each log proved already fatal => [WinError 10054]

        # Create a list of lists like [[log_1, log_5, log_9], [log_2, log_6], [log_3, log_7] ...]
        split_by = 4
        split_logs = [[log for i, log in enumerate(logs) if i % split_by == j] for j in range(split_by)]
        for logs in split_logs:
            Thread(target=self.upload, args=(logs,)).start()
        # t.daemon = True
        # t.start()

    def _upload(self, log: Log):
        """
        Uploads files to specified url and gets the link to their uploaded log
        :param log: A log object
        :return: The permalink to the log, the boss name and the number of tries needed
        """
        with open(log.path, "rb") as log_file:
            with requests.session() as session:
                session.mount("https://", HTTPAdapter(
                    max_retries=Retry(total=3, connect=3, redirect=10, backoff_factor=0.2,
                                      status_forcelist=[HTTPStatus.REQUEST_TIMEOUT,  # HTTP 408
                                                        HTTPStatus.CONFLICT,  # HTTP 409
                                                        HTTPStatus.INTERNAL_SERVER_ERROR,  # HTTP 500
                                                        HTTPStatus.BAD_GATEWAY,  # HTTP 502
                                                        HTTPStatus.SERVICE_UNAVAILABLE,  # HTTP 503
                                                        HTTPStatus.GATEWAY_TIMEOUT])))  # HTTP 504
                re = session.post("https://dps.report/uploadContent?json=1", files={'file': log_file})
                if re.status_code != 200:
                    raise HTTPStatus(re.url, re.status_code)
                elif re.status_code == 200:
                    log.link = re.json()["permalink"]
                    self.queue.put(log)
                    return log
