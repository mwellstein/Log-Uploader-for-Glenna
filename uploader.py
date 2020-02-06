import requests
from typing import List, Tuple
from pathlib import Path
import os
from datetime import datetime, timedelta


def get_encounter_meta(logs_base_dir) -> List:
    """
    Given the logs base directory, extract all subdirectories and their respective files. Filter those with filter_logs().
    :param logs_base_dir: The Path to your main logs folder
    :return: A list of Tuples with the last encounter log path, boss name and number of tries
    """
    # The last logs of all bosses, be aware that e.g. eyes has two folders, thus two entries here
    relevant_logs = []
    # Collect all boss folders
    bosses_path = [logs_base_dir / folder for folder in os.scandir(logs_base_dir) if folder.is_dir()]
    # Collect the latest log-file for each boss
    for boss_path in bosses_path:
        boss_fights = [boss_path / log for log in os.scandir(boss_path) if log.is_file()]
        boss_fights = filter_logs(boss_fights)
        try_count = len(boss_fights)
        if boss_fights:
            relevant_logs.append((max(boss_fights, key=os.path.getctime), boss_path.name, try_count))
    return relevant_logs


def filter_logs(logs_path: List) -> List[Path]:
    """
    Filter those by: this week, raid days and a minimum file size.
    :param logs_path: List of Paths to the log files of one boss
    :return: A list with the Paths of all files that satisfy the filtering conditions
    """
    filtered_logs = []
    week_delta = 0
    if last_week:
        week_delta = 1
    current = datetime.now() - timedelta(weeks=week_delta)
    weeks_monday = current - timedelta(days=current.weekday())
    week_start = datetime.combine(weeks_monday, datetime.min.time())
    print(week_start)
    for log in logs_path:
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


def get_glenna_lines(boss_meta: Tuple) -> None:
    link, boss, try_ = boss_meta
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


if __name__ == '__main__':
    # Change x of Path(x) to your log main folder. You may need to escape \ to \\
    base_log_dir = Path("C:\\Users\\Matthias\\Documents\\Guild Wars 2\\addons\\arcdps\\arcdps.cbtlogs")
    # Where do you want the output file with the uploaded fights?
    output_to = Path("C:\\Users\\Matthias\\Desktop")
    # What are your raiding days? English. Separate multiple with comma
    raid_weekdays = "Wednesday", "Sunday"
    # Do you consider files smaller than y to be a try? 1000 is roughly 1 KB
    min_file_size = 4000
    # You forgot the files from last week? Set this to True
    last_week = False

    # Currently only german names guaranteed (also, only w5-7)
    # No more need to configure, just code from here on
    boss_logs = get_encounter_meta(base_log_dir)
    glenna_meta = upload_files(boss_logs)
    for fight in glenna_meta:
        get_glenna_lines(fight)
