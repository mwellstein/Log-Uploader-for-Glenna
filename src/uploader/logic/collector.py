import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from yaml import safe_load

from .log import Log


class LogCollector:
    """
    The log collector takes all logs, filters through and holds on to the resulting logs
    """

    def __init__(self, controller, base: str, raid_days: List[str], week_delta: int,
                 raids: bool, strikes: bool, fractals: bool):
        self.base = Path(base)
        self.raid_days = raid_days
        self.from_ = datetime.combine(datetime.now() - timedelta(weeks=week_delta, days=datetime.now().weekday()),
                                      datetime.min.time())
        self.until = self.from_ + timedelta(weeks=1)
        self.raids = raids
        self.strikes = strikes
        self.fractals = fractals
        self.raid_bosses = []
        self.strike_bosses = []
        self.fractal_bosses = []
        self.controller = controller

        if getattr(sys, "frozen", False) and hasattr(sys, '_MEIPASS'):
            config_path = Path(getattr(sys, "_MEIPASS")) / "config.yaml"
        else:
            config_path = Path("const/config.yaml")  # If run from source

        logging.info(f"Loading config file at: {config_path}")

        with open(config_path) as config_file:
            config = safe_load(config_file)

        self.min_size = config["logs"]["min_size"]

        de_raid_bosses = config["raids"]["de"]
        en_raid_bosses = config["raids"]["en"]
        self.raid_bosses.extend(de_raid_bosses)
        self.raid_bosses.extend(en_raid_bosses)
        self.raid_bosses = list(set(self.raid_bosses))
        de_strike_bosses = config["strikes"]["de"]
        en_strike_bosses = config["strikes"]["en"]
        self.strike_bosses.extend(de_strike_bosses)
        self.strike_bosses.extend(en_strike_bosses)
        self.strike_bosses = list(set(self.strike_bosses))
        de_fractals_bosses = config["fractals"]["de"]
        en_fractals_bosses = config["fractals"]["en"]
        self.fractal_bosses.extend(de_fractals_bosses)
        self.fractal_bosses.extend(en_fractals_bosses)
        self.fractal_bosses = list(set(self.fractal_bosses))

        logging.info("Collector initialized successfully")

    def collect(self):
        logging.info("Start collection")
        # Collect all boss directories
        boss_dirs = []
        if self.raids:
            boss_dirs.extend([boss_dir for boss_dir in self.base.iterdir() if
                              boss_dir.is_dir() and boss_dir.name in self.raid_bosses])
        if self.strikes:
            boss_dirs.extend([boss_dir for boss_dir in self.base.iterdir() if
                              boss_dir.is_dir() and boss_dir.name in self.strike_bosses])
        if self.fractals:
            boss_dirs.extend([boss_dir for boss_dir in self.base.iterdir() if
                              boss_dir.is_dir() and boss_dir.name in self.fractal_bosses])

        if not boss_dirs:
            return

        logs_to_upload = []  # The return list with all logs to upload
        # Iterate over each boss_dir and create Logs for every file
        # Then filter - twice - to only get the latest created one for every boss_dir
        for boss_dir in boss_dirs:
            logs = [Log(self.controller, path, boss_dir.name) for path in self._collect(boss_dir)]

            # Remove all logs that aren't in the desired time frame
            logs = self.filter(logs)

            # If there are any logs that day for this boss, get the latest one to upload it
            if logs:
                latest_log = max(logs, key=lambda k: k.created)
                latest_log.kill_try_nr = len(logs)
                logs_to_upload.append(latest_log)

        logging.info("Collecting done, returning latest logs per folder.")
        return logs_to_upload

    def filter(self, logs: List[Log]) -> List[Log]:
        """Return only logs that meet the conditions set, i.e. date and size"""
        logging.info("Start filtering logs")
        filtered_logs = []
        for log in logs:
            # If the log is not from the desired week
            if not self.from_.timestamp() < log.created < self.until.timestamp():
                continue
            # If the los is not from a raid day
            if log.day not in self.raid_days:
                continue
            # If the log is not bigger than the minimum
            if not log.size > self.min_size:
                continue
            filtered_logs.append(log)
        logging.info("Finish filtering logs")
        return filtered_logs

    @staticmethod
    def _collect(boss_dir) -> [Path]:
        """Collects the actual files by Path"""
        logging.info("Starting actual file collections")
        # Collect all file paths, i.e. boss_dir/log_name
        files = [boss_dir / log_name for log_name in boss_dir.iterdir() if log_name.is_file()]

        # Collect all subfolders of this boss_dir in case they exist and extend the list of files
        sub_dirs = [boss_dir / sub for sub in boss_dir.iterdir() if sub.is_dir()]
        for sub_dir in sub_dirs:
            files.extend([sub_dir / log for log in sub_dir.iterdir() if log.is_file()])
        logging.info("Finished actual file collection")
        return files
