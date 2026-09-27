""" Kör valideringen av OHLCV data och skriver ut en sammanfattning """

import logging

from src.validator.config import ReportSettings
from src.validator.validate import validate_csv

# Loggkonfiguration passar här bäst, inte i återanvändbara moduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    settings = ReportSettings()
    logger.info("Startar validering av %s", settings.input_csv)

    summary = validate_csv(settings.input_csv)

    print(f"Giltiga rader: {len(summary.valid_bars)}")
    print(f"Ogiltiga rader: {len(summary.errors)}")

    if summary.errors:
        print("\nExempel på fel (första 5):")
        for error in summary.errors[:5]:
            print(f"  Rad {error['row_number']}: {error['error']}")

    logger.info(
        "Validering klar. %d giltiga, %d ogiltiga",
        len(summary.valid_bars), len(summary.errors),
    )


if __name__ == "__main__":
    main()