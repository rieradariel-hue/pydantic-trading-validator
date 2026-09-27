""" Konfiguration för valideringsprojektet - sökvägar till indata och loggfil (loggfil har jag inte behövt lägga till) """

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ReportSettings:
    """ Enkla inställningar för var indata finns. Ingen logik, bara data """

    input_csv: Path = Path("data/nq-15min_dataset.csv")