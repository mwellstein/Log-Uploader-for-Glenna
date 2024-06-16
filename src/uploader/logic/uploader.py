import asyncio
import logging

import aiohttp
from aiohttp_retry import RetryClient, ExponentialRetry, RequestParams
from yaml import safe_load

from .log import Log


class Uploader:
    def __init__(self, controller, collected_logs):
        self.controller = controller
        self.collected_logs = collected_logs

        self.uploaded_logs: [Log] = []

        with open("const/config.yaml") as config_file:
            config = safe_load(config_file)

            self.url = config["upload"]["url"]
            self.backup_url = config["upload"]["backup"]
            self.endpoint = config["upload"]["endpoint"]
            self.params = config["upload"]["params"]
            self.rate_limit = config["upload"]["rate_limit"]
            self.rate_timeout_seconds = config["upload"]["rate_timeout_seconds"]
            retries = config["upload"]["retries"]
            self.retry_options = ExponentialRetry(attempts=retries, statuses={403, 500, 502, 503, 504, 429})
            parallel_connections = config["upload"]["parallel_connections"]
            self.semaphore = asyncio.Semaphore(parallel_connections)


    async def upload(self):
        """Uploads a list of Logs concurrently"""
        logging.info(f"Uploader tasked with uploading {len(self.collected_logs)} logs")
        tasks = [self._upload(log) for log in self.collected_logs]
        logging.info(f"Created {len(tasks)} tasks to be uploaded.")
        for future in asyncio.as_completed(tasks):
            log = await future
            if log:
                logging.info(f"Uploaded {log}, yielding it.")
                yield log

    async def _upload(self, log: Log):
        """
        Uploads files to specified url and gets the link to their uploaded log.
        :param retry_client: the retry client
        :param log: a Log object
        :return: json response from "dps.report"
        """
        # "dps.report" apparently closes the session after both a 403 try and a successful upload. So use multiple.
        async with aiohttp.ClientSession() as session:
            retry_client = RetryClient(session, retry_options=self.retry_options)
            async with self.semaphore:
                try:
                    re = None  # the response object, declared here to use it in except blocks
                    async with retry_client as retry_client:

                        with open(log.path, 'rb') as f:
                            file_data = f.read()
                        data = aiohttp.FormData()
                        data.add_field('file', file_data, filename=log.path.name)

                        logging.info(f"Starting upload of {log.boss}")
                        re = await retry_client.post(self.url, data=data)
                        re_json = await re.json()
                        if re.status == 200:
                            log.link = re_json["permalink"]
                            logging.info("Added a link to a log. Returning it now")
                            return log
                        else:
                            logging.debug(f"Error uploading {log.boss}")
                            logging.debug(f"Reason given dps.report: {re_json}")
                            logging.debug(f"{re.status}\n{re.reason}\n{re.text}")

                except aiohttp.client_exceptions.ClientOSError as e:
                    logging.error(f"ClientOSError while uploading {log.boss}: {str(e)}")
                    logging.debug(f"{re.status}\n{re.reason}\n{re.text}")
                except aiohttp.client_exceptions.ClientResponseError as e:
                    logging.error(f"ClientResponseError while uploading {log.boss}: {str(e)}")
                    logging.debug(f"{re.status}\n{re.reason}\n{re.text}")
                except RuntimeError as e:
                    if str(e) == 'Form data has been processed already':
                        logging.error(f"Runtime - FormData reuse while uploading {log.boss}: {str(e)}")
                        logging.debug(f"{re.status}\n{re.reason}\n{re.text}")
                    else:
                        print(str(e))
                        raise e
                except Exception as e:
                    logging.error(f"Unexpected Error while uploading {log.boss}: {str(e)}")
                    logging.debug(f"{re.status}\n{re.reason}\n{re.text}")
