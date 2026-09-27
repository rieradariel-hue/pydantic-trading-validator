""" Tester för OHLCVBar-modell, load_raw_rows och validate_csv-funktionerna """

# Från pytest (tmp_path, pytest.raises)
import pytest
from pydantic import ValidationError

from src.validator.models import OHLCVBar
from src.validator.loader import load_raw_rows
from src.validator.validate import validate_csv


def test_ohlcv_bar_parses_date_and_time_strings():
    # Fångar om datum / tidsparsning går sönder
    
    bar = OHLCVBar(
        bar_date="17/03/2026", bar_time="21:45",
        open="25120.75", high="25128.0", low="25112.5",
        close="25118.5", volume="697",
    )
    assert bar.bar_date.isoformat() == "2026-03-17"
    assert bar.bar_time.isoformat() == "21:45:00"
    assert bar.volume == 697


def test_ohlcv_bar_rejects_invalid_price():
    # Fångar om ogiltiga prisvärden (icke-numeriska) accepteras
    
    with pytest.raises(ValidationError):
        OHLCVBar(
            bar_date="17/03/2026", bar_time="21:45",
            open="not_a_number", high="25128.0", low="25112.5",
            close="25118.5", volume="697",
        )


def test_load_raw_rows_yields_expected_columns(tmp_path):
    # Fångar om kolumnmappningen går sönder vid ändringar i loader.py
    
    csv_file = tmp_path / "mini.csv"
    csv_file.write_text(
        "17/03/2026;21:45;25120.75;25128.0;25112.5;25118.5;697\n",
        encoding="utf-8",
    )

    rows = list(load_raw_rows(csv_file))

    assert len(rows) == 1
    assert rows[0]["bar_date"] == "17/03/2026"
    assert rows[0]["volume"] == "697"


def test_ohlcv_bar_rejects_high_below_low():
    # Fångar om orimliga high/low kombinationer accepteras
    
    with pytest.raises(ValidationError):
        OHLCVBar(
            bar_date="17/03/2026", bar_time="21:45",
            open="100", high="90", low="95",
            close="98", volume="697",
        )


def test_ohlcv_bar_rejects_negative_volume():
    # Fångar om negativ volym accepteras
    
    with pytest.raises(ValidationError):
        OHLCVBar(
            bar_date="17/03/2026", bar_time="21:45",
            open="100", high="105", low="95",
            close="102", volume="-50",
        )


def test_validate_csv_separates_valid_and_invalid_rows(tmp_path):
    # Fångar om validate_csv slutar skilja på giltiga/ogiltiga rader eller tappar felinfo
    
    csv_file = tmp_path / "mixed.csv"
    csv_file.write_text(
        "17/03/2026;21:45;25120.75;25128.0;25112.5;25118.5;697\n"
        "17/03/2026;22:00;100;90;95;98;500\n",  # high < low - ogiltig
        encoding="utf-8",
    )

    summary = validate_csv(csv_file)

    assert len(summary.valid_bars) == 1
    assert len(summary.errors) == 1
    assert summary.errors[0]["row_number"] == 2