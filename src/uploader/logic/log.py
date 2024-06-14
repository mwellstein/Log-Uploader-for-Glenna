from datetime import datetime
from pathlib import Path


class Log:
    def __init__(self, controller, path: Path, boss: str):
        self.path = path
        self.boss = boss
        file_info = self.path.stat()
        self.created = file_info.st_ctime
        self.modified = file_info.st_mtime
        self.size = file_info.st_size
        self.day = datetime.fromtimestamp(self.created).strftime("%A")
        self.kill_try_nr = 0
        self.link = ""
        self.controller = controller

    def __str__(self):
        if self.link:
            return f"{self.link} {self.kill_try_nr}"
        else:
            raise NoLogLinkError(self)

    def __repr__(self):
        return f"{self.boss}"


class NoLogLinkError(Exception):
    def __init__(self, log: Log):
        super().__init__(f"The Log of {log.boss} does not have a link. Filepath: {log.path}")
