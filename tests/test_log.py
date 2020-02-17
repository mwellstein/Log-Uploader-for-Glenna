import unittest
from log import Log, NoLogLinkError
from pathlib import Path
from datetime import datetime


class TestLog(unittest.TestCase):
    def setUp(self) -> None:
        with open("20200209-210916.zevtc", "w") as log_file:
            log_file.write("something")
        self.log = Log(Path("20200209-210916.zevtc"), "Xera")

    def tearDown(self) -> None:
        self.log.path.unlink()

    def test_creation(self):
        # Set up a log
        self.assertEqual(self.log.path, Path("20200209-210916.zevtc"))
        self.assertEqual(self.log.boss, "Xera")
        file_info = Path("20200209-210916.zevtc").stat()
        self.assertEqual(self.log.created, file_info.st_ctime)
        self.assertEqual(self.log.modified, file_info.st_mtime)
        self.assertEqual(self.log.size, file_info.st_size)
        self.assertEqual(self.log.day, datetime.fromtimestamp(self.log.created).strftime("%A"))

    def test_str(self):
        # str() and repr()
        with self.assertRaises(NoLogLinkError):
            str(self.log)
        self.assertEqual(repr(self.log), "Xera")
