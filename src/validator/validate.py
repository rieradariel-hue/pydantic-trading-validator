""" Kör alla rader i en CSV fil genom OHLCVBar och samlar giltiga/ogiltiga resultat """

from pathlib import Path
from typing import NamedTuple

from pydantic import ValidationError

from src.validator.loader import load_raw_rows
from src.validator.models import OHLCVBar


class ValidationSummary(NamedTuple):
    # Samlar resultatet i: giltiga rader och fel

    valid_bars: list[OHLCVBar]
    errors: list[dict]


def validate_csv(csv_path: Path) -> ValidationSummary:
    # Läser och validerar varje rad i CSV-filen, en rad i taget
    
    valid_bars: list[OHLCVBar] = []
    errors: list[dict] = []

    for row_number, raw_row in enumerate(load_raw_rows(csv_path), start=1):
        try:
            bar = OHLCVBar(**raw_row)
            valid_bars.append(bar)
        except ValidationError as exc:
            # Sparar radnummer, den råa data och felmeddelandet; inte bara att det "gick fel"
            
            errors.append({
                "row_number": row_number,
                "raw_row": raw_row,
                "error": str(exc),
            })

    return ValidationSummary(valid_bars=valid_bars, errors=errors)