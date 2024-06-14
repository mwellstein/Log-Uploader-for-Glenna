from http import HTTPStatus
import requests
from requests.adapters import HTTPAdapter
from requests_ratelimiter import LimiterSession
from urllib3 import Retry
from yaml import safe_load
import traceback
from aiohttp import ClientSession
from aiohttp_retry import ExponentialRetry, RetryClient

from .log import Log


class Uploader:
    def __init__(self, controller):
        retry = Retry(total=8, backoff_factor=0.2)
        self.adapter = HTTPAdapter(max_retries=retry)
        self.controller = controller

        with open("const/config.yaml") as config_file:
            config = safe_load(config_file)

            self.url = config["dps_report"]["url"]
            self.backup_url = config["dps_report"]["backup"]
            self.rate_limit = config["dps_report"]["rate_limit"]
            self.rate_timeout_seconds = config["dps_report"]["rate_timeout_seconds"]

    async def upload(self, log: Log):
        """
        Uploads files to specified url and gets the link to their uploaded log
        :param log: A log object
        :return: the return json from "dps.report"
        """

        retry_options = ExponentialRetry(attempts=5)
        async with ClientSession() as session:
            retry_client = RetryClient(session, retry_options=retry_options)
            async with retry_client.get("http://example.com") as response:
                text = await response.text()

        dps_report_error = ""
        with open(log.path, "rb") as log_file:
            try:
                with requests.session() as session:
                    session.mount("https://", self.adapter)

                    print("start upload")

                    re = session.post(f"{self.url}uploadContent?json=1", files={'file': log_file})
                    if re.status_code == 200:
                        print("Done uploading")
                        return re.json()

                    re = session.post(f"{self.backup_url}uploadContent?json=1", files={'file': log_file})
                    if re.status_code == 200:
                        return re.json()

                    dps_report_error = re.json()['error']  # TODO: this errored out
                    print(dps_report_error)
                    raise requests.exceptions.ConnectionError(f"{re.url}, {re.status_code}, error: {dps_report_error}")
            except requests.exceptions.ConnectionError:
                tb = traceback.format_exc()
                self.controller.show_error("Uploader: ConnectionError",
                                           f"{log.boss}, code: {re.status_code}, dps.report: {dps_report_error}",
                                           tb)
            except Exception as err:
                tb = traceback.format_exc()
                self.controller.show_error("Uploader: Exception - Uncaught and Unknown",
                                           f"{log.boss}, code: {re.status_code}, dps.report: {dps_report_error}",
                                           tb)
