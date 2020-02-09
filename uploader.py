from http import HTTPStatus
from multiprocessing import Queue
from typing import List

import requests
import requests.cookies
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from log import Log


def upload(logs: List[Log], q: Queue):
    for log in logs:
        _upload(log, q)


"""def parallel_upload(logs: List[Log], q: Queue):
    with Pool(processes=cpu_count()) as pool:
        pool.map_async(work, logs)


def work(log: Log):
    _upload(log)"""


def _upload(log: Log, q: Queue = False):
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
                if q:
                    q.put(log)
                else:
                    return log
