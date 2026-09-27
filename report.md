### Datavalidering med Pydantic för historisk futures-prisdata



### Syfte
Syftet med detta arbete var att undersöka hur Pydantic kan användas för att säkerställa att historisk "OHLCV"-prisdata ("Open", "High", "Low", "Close", "Volume") för futures-instrumentet "NQ" har en korrekt struktur och rimliga värden innan den kan användas i ett analysflöde

### Området och relevans
Datavalidering med Python biblioteket "Pydantic", tillämpat på data från finansmarknaden. Det är relevant för Data Science rollen eftersom felaktig eller trasig indata leder till missvisande analys och modellresultat (oavsett hur bra en modell eller pipeline är byggd). Att bygga tydliga, återanvändbara validering steg är en central del av professionellt dataarbete

### Viktiga begrepp
- Pydantic BaseModel: klass som definierar datans förväntade struktur och typer, och som automatiskt validerar och konverterar indata vid instansiering
- field_validator: dekorator som låter en definiera anpassad logik för att validera eller konvertera ett enskilt fält (t.ex förvandla en textsträng till ett datumobjekt)
- model_validator: dekorator för validering som kräver flera fält samtidigt (t.ex att "high" inte är lägre än "low")
- ValidationError: undantaget Pydantic kastar när indata inte uppfyller modellens regler, med detaljerad information om vilket fält som orsakade felet och varför

### Genomförande
Lösningen är byggd som ett litet Python-paket ("src/validator/") med tydlig ansvarsuppdelning:

- "models.py" --- definierar "OHLCVBar", en Pydantic-modell som validerar både datatyper (datum, tid, pris, volym) och affärsregler (t.ex. "high >= low", volym kan inte vara negativ)
- "loader.py" --- läser rå CSV-data rad för rad utan att själv validera
- "validate.py" --- kopplar ihop läsning och validering, och samlar giltiga rader samt fel separat
- "config.py" --- dataclass med sökvägar, utan egen logik
- "__main__.py" --- programmets startpunkt, med loggningskonfiguration och användarvänd utskrift

Data hämtades från "Databento" (historiska "NQ"-futures, 15-minutersstaplar, 2008-2026). Under arbetet identifierades att verklig leverantörsdata nästan alltid är strukturellt korrekt, vilket gjorde att en separat, medvetet konstruerad demofil ("data/nq-15min_dataset.csv") skapades för att på ett tydligt sätt visa att valideringen faktisk fångar felaktig data när den förekommer

Ett problem som uppstod under arbetet var att skript som kördes med absolut sökväg (t.ex via IDE:ns kör-knapp) inte hittade projektets egna paket. Lösningen var att alltid köra filer som moduler från projektets rotmapp

### Resultat
- Validering av den fullständiga historiska filen (405498 rader) gav 405498 giltiga rader och 0 ogiltiga (vilket bekräftar att leverantörsdata är strukturellt tillförlitlig)
- Validering av demofilen (15 rader, varav 5 medvetet trasiga) gav 10 giltiga och 5 ogiltiga rader. Alla fem fel identifierades korrekt: tre fall av negativ volym och två fall där "high" var lägre än "low"
- Körtiden för den fullständiga filen var cirka 11 sekunder

### Begränsningar och möjliga förbättringar
- Lösningen validerar endast strukturell och grundläggande logisk korrekthet (typer, "high"/"low"-konsistens, icke-negativ volym) - den bedömer inte om priserna är rimliga i förhållande till marknadens historiska nivåer
- Onormala men giltiga händelser, t.ex kraftiga volymtoppar vid FOMC-beslut, flaggas inte separat i nuvarande version (detta vore en naturlig vidareutveckling) (att markera avvikande men inte ogiltig data, snarare än att bara godkänna/underkänna)
- Endast en del av datakvalitetsproblem testas i demofilen (fyra typer); fler typer (t.ex dubbletter, tidsluckor) skulle kunna läggas till

### Koppling till yrkesrollen
En Data Scientist eller dataanalytiker arbetar sällan med data som är garanterat korrekt (även data från betrodda leverantörer kan innehålla fel). Att bygga in strukturerad validering tidigt i en pipeline, med tydliga och testbara regler, minskar risken för att felaktig data i tysthet förvanskar senare analyser eller modeller

### Källor
- Pydantic, officiell dokumentation ("BaseModel", "field_validator", "model_validator")
- pytest, officiell dokumentation ("tmp_path", "pytest.raises")
- Kursmaterial: moduler, paket, felhantering, projektstruktur, testning
- Databento (datakälla för historisk NQ-futuresdata)





### Självreflektion

# 1. Vad lärde du dig som du inte kunde innan?
Jag lärde mig att använda "Pydantic" för att bygga tydligare och mer strukturerad datavalidering än vad manuell kontrolllogik hade gett. Genom "field_validator" och "model_validator" kunde jag separera typkonvertering (datum, tid, tal) från affärsregler (t.ex att "high" inte kan vara lägre än "low"), och "ValidationError" gav mig detaljerad information om exakt vilket fält och villkor som brutits och inte bara att något var fel

# 2. Vad var svårast att förstå eller genomföra?
Det svåraste var att inse att verklig leverantörsdata (från "Databento") i praktiken alltid är strukturellt korrekt. Detta gjorde att en enkel valideringskörning mot riktig data aldrig visade några fel, trots att koden fungerade korrekt. Jag ville visa att valideringen faktiskt kan upptäcka fel, utan att lämna det riktiga datasetet helt, eftersom perfekt rensad data sällan är verkligheten i en arbetsmiljö. Lösningen blev att blanda en liten mängd riktiga rader med några medvetet trasiga rader i en och samma fil, istället för att ha separata "ren" och "smutsig" data i olika körvägar

# 3. Vilket tekniskt val är du mest nöjd med och varför?
Jag är mest nöjd med beslutet att blanda ren och trasig data i en enda fil istället för att ha flera separata filer eller körvägar för olika syften. Det var en lösning jag kom fram till efter att ha insett att mitt ursprungliga upplägg (en stor ren fil och en liten trasig fil) inte gav en tydlig demonstration. Att istället bygga en enda representativ fil gjorde lösningen enklare att köra, förstå och förklara och tvingade mig att tänka igenom vad en "realistisk" datamängd faktiskt innebär

# 4. Vad hade du gjort annorlunda om du började om?
I efterhand hade jag valt ett annat fördjupningsexempel än just "NQ"-futuresdata från "Databento", eftersom den datan visade sig vara ovanligt ren. Ett område där riktig, naturligt förekommande smutsig data är vanligare hade gjort det möjligt att demonstrera valideringen direkt mot verklig data, istället för att jag behövde lägga tid på att skriva ett separat skript för att generera en blandad demofil. Något jag insåg först relativt sent i arbetet, när alla valideringar konsekvent gick igenom

# 5. Vad skulle vara ett naturligt nästa steg om du fortsatte arbetet?
Ett naturligt nästa steg vore att lägga till fler valideringslager, till exempel flaggning av extrema men giltiga händelser ("FOMC" beslut, nyhetsdagar, eller enskilda staplar med ovanligt stora prisrörelser). Dessa dagar är tekniskt giltiga men statistiskt avvikande, och skulle kunna flaggas snarare än avvisas. Vilket sedan gör det möjligt att medvetet exkludera dem vid träning och test av en ML-modell, eftersom de inte representerar en normal handelsdag

# 6. Vilket betyg tycker du själv att arbetet motsvarar - G eller VG?
G

# 7. Motivera din bedömning genom att koppla till kraven för G och VG
Jag bedömer arbetet som G eftersom jag självständigt valt och avgränsat ett relevant Pythonområde, satt mig in i "Pydantic" via dess dokumentation, byggt en fungerande valideringslösning som jag förstår och kan förklara, samt dokumenterat och testat koden. Jag når inte ut VG-kraven eftersom jag inte hunnit implementera fler lager av validering (t.ex flaggning av extremvärden) eller resonera lika djupt kring alternativa lösningar som tiden hade tillåtit