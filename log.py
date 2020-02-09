from datetime import datetime
from pathlib import Path


class Log:
    def __init__(self, path: Path, boss: str):
        self.path = path
        self.boss = boss
        file_info = path.stat()
        self.created = file_info.st_ctime
        self.modified = file_info.st_mtime
        self.size = file_info.st_size
        self.day = datetime.fromtimestamp(self.created).strftime("%A")
        self.try_ = 0
        self.link = ""

    def __str__(self):
        if self.link:
            return f"{self.link} {self.boss} {self.try_}"
        else:
            raise NoLogLinkError(self)


class NoLogLinkError(Exception):
    def __init__(self, log: Log):
        super().__init__(f"The Log of {log.boss} does not have a link. Filepath: {log.path}")
