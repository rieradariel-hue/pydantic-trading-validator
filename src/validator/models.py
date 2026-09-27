""" Pydantic modeller för validering av OHLCV data (15-minutersstaplar) """

# Från Pydantic (models, field_validator, model_validator)
from datetime import date, time, datetime

from pydantic import BaseModel, field_validator, model_validator


class OHLCVBar(BaseModel):
    # En enskild 15-minutersstapel med pris och volymdata

    bar_date: date
    bar_time: time
    open: float
    high: float
    low: float
    close: float
    volume: int

    @field_validator("bar_date", mode="before")
    @classmethod
    def parse_date(cls, value: str | date) -> date:
        # Konverterar strängformatet "DD/MM/YYYY" (från CSV) till ett date-objekt
        
        if isinstance(value, str):
            return datetime.strptime(value, "%d/%m/%Y").date()
        return value


    @field_validator("bar_time", mode="before")
    @classmethod
    def parse_time(cls, value: str | time) -> time:
        # Konverterar strängformatet "HH:MM" (från CSV) till time-objekt
        
        if isinstance(value, str):
            return datetime.strptime(value, "%H:%M").time()
        return value

    @field_validator("volume")
    @classmethod
    def volume_must_be_non_negative(cls, value: int) -> int:
        # Volym kan aldrig vara negativ. Tecken på skadad data
        
        if value < 0:
            raise ValueError(f"volume kan inte vara negativ, fick {value}")
        return value

    @model_validator(mode="after")
    def check_price_consistency(self) -> "OHLCVBar":
        # High måste vara det högsta värdet och Low det lägsta. Annars är stapeln orimlig
        
        if self.high < self.low:
            raise ValueError(f"high ({self.high}) kan inte vara lägre än low ({self.low})")
        if self.high < max(self.open, self.close):
            raise ValueError(f"high ({self.high}) måste vara >= open och close")
        if self.low > min(self.open, self.close):
            raise ValueError(f"low ({self.low}) måste vara <= open och close")
        return self