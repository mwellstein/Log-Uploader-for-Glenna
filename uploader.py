import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple
from multiprocessing import Queue

import requests


def filter_logs(logs: List, raid_weekdays: List[str], week_delta: int, min_file_size: int) -> List[Path]:
    """
    Filter those by: this week, raid days and a minimum file size.
    :param logs: List of Paths to the log files of one boss
    :param raid_weekdays: which days of the week are the desired raid days
    :param week_delta: optional for x weeks in the past
    :param min_file_size: optional minimum file size
    :return: A list with the Paths of all files that satisfy the filtering conditions
    """
    filtered_logs = []
    current = datetime.now() - timedelta(weeks=week_delta)
    weeks_monday = current - timedelta(days=current.weekday())
    week_start = datetime.combine(weeks_monday, datetime.min.time())
    for log in logs:
        file_size = os.path.getsize(log)
        log_timestamp = os.path.getctime(log)
        log_weekday = datetime.fromtimestamp(log_timestamp).strftime("%A")
        # If the log is from this week
        if log_timestamp > week_start.timestamp():
            # and from a raid day
            if log_weekday in raid_weekdays:
                # and more than a instant gg
                if file_size > min_file_size:
                    filtered_logs.append(log)
    return filtered_logs


def upload_file(logs_meta: Tuple, q: Queue = False) -> Tuple:
    """
    Uploads files to specified url and gets the link to their uploaded log
    :param logs_meta: The log Path
    :param q: the queue, if its a child process
    :return: The permalink to the log, the boss name and the number of tries needed
    """
    log_file, log_boss, log_try_ = logs_meta
    with open(log_file, "rb") as log:
        re = requests.post("https://dps.report/uploadContent?json=1", files={'file': log})
        if re.status_code == 200:
            meta = re.json()["permalink"], log_boss, log_try_
            if q:
                q.put(meta)
            return meta
        else:
            print("Error, downloading", re.status_code)


def get_glenna_line(log_meta: Tuple) -> str:
    """
    Returns lines to copy/paste for glenna.
    
    Currently only german names guaranteed (also, only w5-7)
    :param log_meta: 
    :return: 
    """
    link, boss, try_ = log_meta
    # Those bosses bought a name change for 1000 gems
    if "Auge des" in boss:
        boss = "Augen"
    if "Desmina" in boss:
        boss = "Fluss der Seelen"
    if "Nikare" in boss:
        boss = "Largos-Zwillinge"

    # And some are not compatible with glenna
    # Namely strikes
    if "Knochenhäuter" in boss:
        return ""
    if "Eisbrut-Konstrukt" in boss:
        return ""
    if "Stimme der Gefallenen" in boss:
        return ""
    if "Fraenir Jormags" in boss:
        return ""
    # And some raid events
    if "Spukende Statue" in boss:
        return ""
    return f"{link} {boss} {try_}"


def get_log_metas(base: str, raid_weekdays: List[str], week_delta: int, min_file_size: int):
    """
    Get the latest log_path for each boss killed on the specified days in the specified week, that are larger then
    the minimum file size. And the bosses Name (dir name), as well as how many tries where needed.
    :param base: Path to the main log folder
    :param raid_weekdays: From which days you want to have the uploads
    :param week_delta: Go back in time
    :param min_file_size: Filter instant gg`s
    :return:
    """
    base = Path(base)
    # Collect all boss folders
    bosses = [base / boss for boss in os.scandir(base) if boss.is_dir()]
    # The last logs of all bosses, be aware that e.g. eyes has two folders, thus two entries here
    log_metas = []
    # Collect the latest log-file for each boss
    for boss in bosses:
        logs = [boss / log for log in os.scandir(boss) if log.is_file()]
        logs = filter_logs(logs, raid_weekdays, week_delta, min_file_size)
        try_count = len(logs)
        if logs:
            log_metas.append((max(logs, key=os.path.getctime), boss.name, try_count))
    return log_metas


if __name__ == '__main__':
    logs_info = get_log_metas("C:\\Users\\Matthias\\Documents\\Guild Wars 2\\addons\\arcdps\\arcdps.cbtlogs",
                              ["Wednesday", "Sunday"], 0, 400000)
    glenna_meta = []
    for file in logs_info:
        fight = upload_file(file)
        print(get_glenna_line(fight))
