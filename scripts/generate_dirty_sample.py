"""Skapar en liten CSV-fil med både giltiga och medvetet trasiga rader, för demo. Stort tack till Ai hjälp här"""

import random
from itertools import islice
from pathlib import Path

from src.validator.loader import load_raw_rows

# Fast seed - samma "slumpmässiga" trasiga rader varje gång scriptet körs
random.seed(42)

SOURCE_CSV = Path("data/nq-15m_bk.csv")
OUTPUT_CSV = Path("data/nq-15min_dataset.csv")

CLEAN_ROW_COUNT = 15
DIRTY_ROW_COUNT = 5



def corrupt_high_below_low(row: dict) -> dict:
    # Byter plats på high och low
    
    row = row.copy()
    row["high"], row["low"] = row["low"], row["high"]
    return row


def corrupt_negative_volume(row: dict) -> dict:
    # Gör volymen negativ
    
    row = row.copy()
    row["volume"] = f"-{row['volume']}"
    return row


def corrupt_non_numeric_price(row: dict) -> dict:
    # Ersätter open-pris med text istället för tal

    row = row.copy()
    row["open"] = "N/A"
    return row


def corrupt_missing_field(row: dict) -> dict:
    # Tar bort close helt 
    
    row = row.copy()
    del row["close"]
    return row


CORRUPTIONS = [
    corrupt_high_below_low,
    corrupt_negative_volume,
    corrupt_non_numeric_price,
    corrupt_missing_field,
]


def row_to_csv_line(row: dict) -> str:
    # OBS: rader med saknat fält blir kortare
    
    return ";".join(row.values())


def main() -> None:
    rows = list(islice(load_raw_rows(SOURCE_CSV), CLEAN_ROW_COUNT))

    dirty_indices = random.sample(range(len(rows)), DIRTY_ROW_COUNT)
    for index in dirty_indices:
        corruption = random.choice(CORRUPTIONS)
        rows[index] = corruption(rows[index])

    with open(OUTPUT_CSV, "w", encoding="utf-8") as file:
        for row in rows:
            file.write(row_to_csv_line(row) + "\n")

    print(f"Skrev {len(rows)} rader till {OUTPUT_CSV} ({DIRTY_ROW_COUNT} trasiga)")


if __name__ == "__main__":
    main()