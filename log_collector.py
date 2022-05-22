from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from log import Log


class LogCollector:
    """
    The log collector takes all logs, filters through and holds on to the resulting logs
    """

    def __init__(self, base: str, raid_days: List[str], week_delta: int, min_size: int, fractals: bool):
        self.base = Path(base)
        self.raid_days = raid_days
        self.from_ = datetime.combine(datetime.now() - timedelta(weeks=week_delta, days=datetime.now().weekday()),
                                      datetime.min.time())
        self.until = self.from_ + timedelta(weeks=1)
        self.min_size = min_size
        self.fractals = fractals
        self.raid_bosses = [
            "Tal-Wächter", "Gorseval der Facettenreiche", "Sabetha die Saboteurin",  # W1 GER
            "Vale Guardian", "Gorseval the Multifarious", "Sabetha the Saboteur",  # W1 ENG
            "Faultierion", "Berg", "Matthias Gabrel",  # W1 GER
            "Slothasor",  # W2 ENG
            "Festenkonstrukt", "Spukende Statue", "Xera",  # W3 GER
            "Keep Construct", "Haunting Statue",  # W3 EMG
            "Cairn der Unbeugsame", "Mursaat-Aufseher", "Samarog", "Deimos",  # W4 GER
            "Cairn the Indomitable", "Mursaat Overseer",  # W4 ENG
            "Seelenloser Schrecken", "Desmina", "Bezwungener König", "Seelenverzehrer", "Auge des Urteils",
            "Auge des Schicksals", "Dhuum",  # W5 GER
            "Soulless Horror", "Broken King", "Eater of Souls", "Eye of Judgment", "Eye of Fate",  # W5 ENG
            "Beschworene Verschmelzung", "Nikare", "Qadim",  # W6 GER
            "Conjured Amalgamate",  # W6 ENG
            "Kardinal Adina", "Kardinal Sabir", "Qadim der Unvergleichliche",  # W7 GER
            "Cardinal Adina", "Cardinal Sabir", "Qadim the Peerless",  # W7 GER
            "Eisbrut-Konstrukt", "Stimme der Gefallenen", "Fraenir Jormags", "Knochenhäuter", "Stimme der Gefallenen",
            # Strikes GER
            "Icebrood Construct", "Voice of the Fallen", "Fraenir of Jormag", "Boneskinner", "Whisper of Jormag",
            "Freezie",  # Strikes ENG
            "Kapitän Mai Trin", "Ankka", "Minister Lee", "Die Drachenleere"  # EoD Strikes GER
            "Captain Mai Trin", "Ankka", "Minister Lee", "The Dragonvoid"  # EoD Strikes ENG
        ]
        self.fractal_bosses = [
            "MAMA", "Albtraum-Oratuss", "Ensolyss der endlosen Pein", "Skorvald der Zerschmetterte",
            "Siax the Corrupted", "Ensolyss of the Endless Torment", "Skorvald the Shattered", "Artsariiv", "Arkk"
        ]

    def collect(self):
        # Collect all boss directories
        if self.fractals:
            boss_dirs = [boss for boss in self.base.iterdir() if boss.is_dir() and boss.name in self.fractal_bosses]
        else:
            boss_dirs = [boss for boss in self.base.iterdir() if boss.is_dir() and boss.name in self.raid_bosses]
        latest_logs = []
        for boss_dir in boss_dirs:
            logs = [Log(path, boss_dir.name) for path in _collect(boss_dir)]
            logs = self.filter(logs)
            # If there are any logs
            if logs:
                latest_log = max(logs, key=lambda k: k.created)
                latest_log.try_ = len(logs)
                latest_logs.append(latest_log)
        return latest_logs

    def filter(self, logs: List[Log]) -> List[Log]:
        filtered_logs = []
        for log in logs:
            # If the log is from the desired week
            if self.from_.timestamp() < log.created < self.until.timestamp():
                # If the los is from a raid day
                if log.day in self.raid_days:
                    # If the log is bigger than the minimum
                    if log.size > self.min_size:
                        filtered_logs.append(log)
        return filtered_logs


def _collect(boss_dir):
    """Collects the actual file Paths"""
    files = [boss_dir / log for log in boss_dir.iterdir() if log.is_file()]
    sub_dirs = [boss_dir / sub for sub in boss_dir.iterdir() if sub.is_dir()]
    for sub_dir in sub_dirs:
        files.extend([sub_dir / log for log in sub_dir.iterdir() if log.is_file()])
    return files
