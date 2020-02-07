import requests
from typing import List, Tuple
from pathlib import Path
import os
from datetime import datetime, timedelta


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


def upload_files(logs_meta: List) -> Tuple:
    """
    Uploads files to specified url and gets the link to their uploaded log
    :param logs_meta: The log Path
    :return: The permalink to the log, the boss name and the number of tries needed
    """
    for log_file, log_boss, log_try_ in logs_meta:
        with open(log_file, "rb") as log:
            re = requests.post("https://dps.report/uploadContent?json=1", files={'file': log})
            yield re.json()["permalink"], log_boss, log_try_


def get_glenna_lines(log_meta: Tuple) -> None:
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
        return
    if "Eisbrut-Konstrukt" in boss:
        return
    if "Stimme der Gefallenen" in boss:
        return
    if "Fraenir Jormags" in boss:
        return
    # And some raid events
    if "Spukende Statue" in boss:
        return
    print(f"{link} {boss} {try_}")


def main(base: str, raid_weekdays: List[str], week_delta: int, min_file_size: int):
    base = Path(base)
    # Collect all boss folders
    bosses = [base / boss for boss in os.scandir(base) if boss.is_dir()]
    # The last logs of all bosses, be aware that e.g. eyes has two folders, thus two entries here
    log_upload_meta = []
    # Collect the latest log-file for each boss
    for boss in bosses:
        logs = [boss / log for log in os.scandir(boss) if log.is_file()]
        logs = filter_logs(logs, raid_weekdays, week_delta, min_file_size)
        try_count = len(logs)
        if logs:
            log_upload_meta.append((max(logs, key=os.path.getctime), boss.name, try_count))

    # No more need to configure, just code from here on
    glenna_meta = upload_files(log_upload_meta)
    for fight in glenna_meta:
        get_glenna_lines(fight)


if __name__ == '__main__':
    main("C:\\Users\\Matthias\\Documents\\Guild Wars 2\\addons\\arcdps\\arcdps.cbtlogs", ["Wednesday", "Sunday"], 0, 4000)
