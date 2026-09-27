# PoE2 Currency Tracker

Zeigt aktuelle Path-of-Exile-2-Preise (Chaos / Exalted / Divine Orbs) an und
aktualisiert sich automatisch jede Stunde über GitHub Actions.

Datenquelle: die öffentliche, dokumentierte [poe.ninja Economy-API](https://poe.ninja/docs/api)
(inoffiziell, ohne Garantie/SLA seitens poe.ninja).

## Wie es funktioniert

```
fetch_prices.py  →  data/latest.json  →  index.html (Dashboard)
      ↑
GitHub Actions (stündlich, siehe .github/workflows/update-prices.yml)
```

1. `fetch_prices.py` ruft für alle aktuell verfügbaren Ligen (z. B. Standard,
   Hardcore, sowie eine oder mehrere parallele Challenge-/Event-Ligen) und
   mehrere Kategorien (Currency, Fragments, Essences, …) die
   PoE2-Exchange-Overview von poe.ninja ab und rechnet alle Preise in
   Chaos-, Exalted- und Divine-Orb-Äquivalente um.
2. Das Ergebnis wird in `data/latest.json` gespeichert. Zusätzlich schreibt
   das Skript jeden Preis-Snapshot in `data/history.json` fort (rollierend,
   ca. 8 Tage Aufbewahrung) und berechnet daraus für jedes Item die
   Preis-Trends über 1h / 3h / 3 Tage / 7 Tage.
3. `index.html` lädt die Daten und zeigt sie in einer durchsuchbaren, nach
   Liga und Kategorie filterbaren Tabelle an – inklusive der vier
   Trend-Spalten.
4. Ein GitHub-Actions-Workflow führt Schritt 1+2 automatisch jede Stunde aus
   und committet `data/latest.json` sowie `data/history.json` zurück ins Repo.

**Wichtig zu den Trends:** poe.ninja liefert selbst keine Preis-Historie mit
frei wählbaren Zeiträumen (nur eine kurze, nicht dokumentierte Sparkline pro
Abfrage). Die 1h/3h/3d/7d-Trends in diesem Projekt werden deshalb selbst
berechnet, indem jeder stündliche Lauf einen Preis-Snapshot in
`data/history.json` ablegt. Das bedeutet: **die 3-Tage- und 7-Tage-Trends
sind erst zuverlässig, sobald der Workflow tatsächlich 3 bzw. 7 Tage lang
gelaufen ist.** Bis dahin zeigt die Tabelle für diese Spalten „–" an.

## Setup (empfohlen: GitHub Pages + Actions, kein eigener Server nötig)

1. **Neues GitHub-Repo erstellen** und diesen Ordner hochladen (oder
   `git init`, `git add .`, `git commit`, `git push` in ein leeres Repo).

2. **Schreibrechte für Actions aktivieren**, damit der Workflow die
   aktualisierten Daten zurück committen darf:
   `Settings → Actions → General → Workflow permissions →
   "Read and write permissions"` auswählen und speichern.

3. **GitHub Pages aktivieren**:
   `Settings → Pages → Source: "Deploy from a branch" → Branch: main / (root)`.
   Nach ein paar Minuten ist das Dashboard unter
   `https://DEIN-USERNAME.github.io/DEIN-REPO/` erreichbar.

4. **Kontakt-User-Agent eintragen** (von poe.ninja erbeten, siehe deren
   Nutzungsrichtlinien): in `fetch_prices.py` die Zeile mit `USER_AGENT`
   anpassen und eine echte Kontakt-Info (z. B. E-Mail) eintragen.

5. **Ersten Lauf manuell anstoßen** (optional, sonst läuft er automatisch
   zur nächsten vollen Stunde): im Tab **Actions** den Workflow
   "Update PoE2 currency prices" auswählen → "Run workflow".

Das war's – ab jetzt aktualisieren sich die Preise automatisch stündlich,
passend zum Update-Rhythmus von poe.ninja selbst (häufiger pollen bringt
laut deren Doku ohnehin keine frischeren Daten).

## Lokal testen

```bash
python3 fetch_prices.py          # holt aktuelle Preise, schreibt data/latest.json
python3 -m http.server 8000      # startet lokalen Webserver
# dann im Browser: http://localhost:8000
```

(`index.html` per Doppelklick öffnen funktioniert nicht zuverlässig, weil
Browser `fetch()` auf lokale Dateien oft aus Sicherheitsgründen blockieren –
deshalb den kleinen lokalen Webserver verwenden.)

## Kategorien erweitern/ändern

Die getrackten Kategorien stehen in `fetch_prices.py` in der Liste
`CATEGORIES`. Gültige Werte für PoE2 (Stand poe.ninja-Doku):

`Currency`, `Fragments`, `Abyss`, `UncutGems`, `LineageSupportGems`,
`Essences`, `SoulCores`, `Idols`, `Runes`, `Ritual`, `Expedition`,
`Delirium`, `Breach`, `Verisium`

## Liga ändern

Standardmäßig werden **alle** Ligen abgerufen, die poe.ninja gerade liefert,
und im Dashboard per Dropdown auswählbar gemacht. Das ist bewusst so
gewählt, weil PoE2 zeitweise mehrere parallele Challenge-Ligen gleichzeitig
haben kann – aktuell z. B. **Runes of Aldur** und zusätzlich die
Event-Liga **Forbidden Rites**, die im September 2026 gestartet ist und
parallel zu Runes of Aldur läuft (keine Ablösung). Eine feste Auswahl wie
„nur eine Challenge-Liga + Standard + Hardcore" würde eine solche
zusätzliche Liga stillschweigend auslassen – deshalb holt das Skript
lieber alles und lässt dich im Dashboard wählen.

Um das einzuschränken (z. B. nur bestimmte Ligen abzurufen und damit
Laufzeit/Requests zu reduzieren), die Umgebungsvariable `POE2_LEAGUES` mit
einer kommagetrennten Liste von Liga-IDs setzen – lokal per
`POE2_LEAGUES="Standard,Hardcore" python3 fetch_prices.py`, im Workflow per
`env:`-Eintrag in `.github/workflows/update-prices.yml`. Die erste Liga in
der Liste (bzw. der Reihenfolge von poe.ninja) wird beim Laden des
Dashboards vorausgewählt.

## Grenzen / Fair Use

poe.ninja bittet ausdrücklich darum, die Economy-Endpoints nicht öfter als
nötig abzufragen und einen aussagekräftigen User-Agent zu senden (siehe
[poe.ninja/docs/api](https://poe.ninja/docs/api)). Der stündliche Rhythmus
in diesem Projekt ist bewusst so gewählt, dass er nicht öfter pollt, als
sich die Daten dort selbst aktualisieren. Durch den Abruf aller verfügbaren
Ligen (Standard, Hardcore, sowie ggf. mehrere parallele Challenge-/Event-
Ligen) macht ein Lauf entsprechend mehr Requests (Ligen × Kategorien) – bei
Bedarf über `POE2_LEAGUES` auf weniger Ligen einschränken, um die Laufzeit
und Anzahl der Anfragen zu reduzieren.
