""" Läser in rå OHLCV data rad efter rad från CSV-filen """

from pathlib import Path
from typing import Iterator

# Kolumnordningen i CSV-filen (ingen header finns därinne)

COLUMN_NAMES = ["bar_date", "bar_time", "open", "high", "low", "close", "volume"]


def load_raw_rows(csv_path: Path) -> Iterator[dict[str, str]]:
    # Läser filen och returnerar varje rad som en dict med råa strängvärden
    
    with open(csv_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # Hoppar över tomma rader
            values = line.split(";")
            yield dict(zip(COLUMN_NAMES, values))