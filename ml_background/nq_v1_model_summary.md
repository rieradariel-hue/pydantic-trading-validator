### Bakgrund: ML-modellen som ligger som grund för valideringsdatan

Detta dokument är enbart bakgrund kontext. Uppgiften handlar om datavalidering med Pydantic, inte om att optimera eller bedöma denna ML-modell

### Vad modellen försökte göra

En XGBoost-klassificerare och regressor tränades för att gissa riktning ("bullish"/"bearish") och storlek (i ticks) på NQ-futuresmarknadens RTH-session (US-öppning), baserat på tidigare Asia/London/RTH-sessions beteende och volatilitet ("ATR" average true range)

### Data

- Källa: Databento, 15-minutersstaplar ("OHLCV") för NQ-futures, 2008-2026
- Aprox 4166 dagar efter rensning av korta-dagar (tidig stängning) och FOMC-dagar med onormala volym

### Resultat

Modellresultat

Klassificerare
Valideringsresultat (2021-2023): F1 macro 0.37
Out-of-sample (2024-2026): -

Regressor
Valideringsresultat (2021-2023): R² 0.41, MAE 69 poäng
Out-of-sample (2024-2026): -

Backtest (Sharpe-kvot)
Valideringsresultat (2021-2023): 1.34
Out-of-sample (2024-2026): -0.21

### Slutsats

Modellen presterade lovande på valideringsdata men misslyckades på ett låst out-of-sample-test. Ett tydligt exempel på överanpassning till en specifik marknadsregim (2021-2023). Detta är precis anledningen till att denna typ av historisk pris- och signaldata behöver strukturerad validering innan den används i analysflöden (vilket är den faktiska fördjupningen i detta arbete)