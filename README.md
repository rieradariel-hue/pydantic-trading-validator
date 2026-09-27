### Pydantic Trading Data Validator
Ett litet Python-paket som validerar historisk "OHLCV"-prisdata ("Open", "High", "Low", "Close", "Volume") för futures-instrumentet "NQ", med hjälp av "Pydantic". Byggt för kursen "Fördjupning i Pythonprogrammering"

### Vad projektet gör
- Läser rader från en semikolon-separerad "CSV" fil med prisdata
- Validerar varje rad mot en "Pydantic" modell ("OHLCVBar")
- Kontrollerar både typer (datum, tid, tal) och affärsregler (t.ex. "high" kan inte vara lägre än "low", volym kan inte vara negativ)
- Samlar och rapporterar giltiga rader samt fel med radnummer och orsak

### Installation
Skapa och aktivera virtuell miljö samt installera beroenden via kommandona "python -m venv .venv", ".venv\Scripts\activate" och "pip install -r requirements.txt"

### Körning
Kör valideringen med kommandot "python -m src.validator"

Kör mot standardfilen "data/nq-15min_dataset.csv" (en liten demofil med både giltig och medvetet trasig data) och skriver ut antal giltiga och ogiltiga rader samt felmeddelanden

### Tester
Kör tests med kommandot "python -m pytest -v"

### Beroenden
Se "requirements.txt": "pydantic", "pandas", "pytest"

### Data
- "data/nq-15min_dataset.csv". En liten demofil (10 giltiga + 5 medvetet trasiga rader), genererad av "scripts/generate_dirty_sample.py"
- "data/nq-15m_bk.csv". En fullständig historisk källdata ("Databento", "NQ"-futures, 15-minutersstaplar). Används inte av standardkörningen men validerades separat mot samma modell (405 498 giltiga rader, 0 ogiltiga). Se "report.md" för resultat

### Bakgrund
Se "ml_background/nq_v1_model_summary.md" för kontext om varför denna typ av data behöver valideras