#!/usr/bin/env python3
"""
PoE2 Currency Tracker - Fetch Script
=====================================
Ruft die poe.ninja Exchange-Overview-API fuer Path of Exile 2 ab (fuer alle
aktuell verfuegbaren Ligen, z.B. mehrere parallele Challenge-Ligen plus
Standard/Hardcore), rechnet alle Preise in Chaos / Exalted / Divine Orbs um
und speichert das Ergebnis als data/latest.json.

Wird per GitHub Actions (siehe .github/workflows/update-prices.yml)
oder per Cron-Job stuendlich ausgefuehrt.

Datenquelle: https://poe.ninja/docs/api
Hinweis der Doku: PoE2-Daten aktualisieren sich serverseitig nur
ca. stuendlich - haeufigeres Abrufen bringt keine frischeren Daten
und belastet unnoetig die kostenlose Community-Ressource.
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import quote

BASE_URL = "https://poe.ninja/poe2/api/economy"

# Bitte anpassen: eine echte Kontakt-Info, wie von poe.ninja erbeten
# (siehe "Usage guidelines" in https://poe.ninja/docs/api)
USER_AGENT = "poe2-currency-tracker/1.0 (contact: christopher.schmitt1993@gmail.com)"

# Kategorien, die getrackt werden. Vollstaendige Liste der gueltigen
# "type"-Werte steht in der poe.ninja-Doku (Exchange overview, PoE2).
CATEGORIES = [
    "Currency",
    "Fragments",
    "Essences",
    "SoulCores",
    "Runes",
    "Idols",
    "Ritual",
    "Expedition",
    "Delirium",
    "Breach",
    "Abyss",
    "UncutGems",
    "LineageSupportGems",
    "Verisium",
]

# Anzeigenamen fuer die Kategorien im Dashboard. Bei manchen Kategorien
# weicht der interne poe.ninja-"type"-Wert vom Namen ab, den Spieler
# kennen (z.B. liefert "Breach" die Catalysts-Preise, "Ritual" die Omen-
# Preise, "Delirium" die Liquid-Emotions-Preise).
CATEGORY_LABELS = {
    "Currency": "Currency",
    "Fragments": "Fragments",
    "Essences": "Essences",
    "SoulCores": "Soul Cores",
    "Runes": "Runes",
    "Idols": "Idols",
    "Ritual": "Omens",
    "Expedition": "Expedition",
    "Delirium": "Liquid Emotions",
    "Breach": "Catalysts",
    "Abyss": "Abyssal Bones",
    "UncutGems": "Uncut Gems",
    "LineageSupportGems": "Lineage Gems",
    "Verisium": "Verisium",
}

# Referenzwaehrungen, die im Dashboard angezeigt werden sollen
TARGET_CURRENCIES = ["chaos", "exalted", "divine"]

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "latest.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

# Trend-Zeitfenster (in Stunden) fuer die Anzeige im Dashboard
TREND_WINDOWS = {"1h": 1, "3h": 3, "3d": 72, "7d": 168}

# Maximal erlaubte Abweichung (in Stunden) zwischen dem gewuenschten Zeitpunkt
# und dem tatsaechlich gefundenen History-Eintrag. Wird diese Toleranz
# ueberschritten (z.B. weil das Skript laengere Zeit nicht lief), wird der
# Trend lieber als "nicht verfuegbar" (None) ausgegeben, statt einen
# irrefuehrenden Wert auf Basis eines viel zu alten Snapshots zu zeigen.
TREND_TOLERANCE_HOURS = {"1h": 1, "3h": 2, "3d": 12, "7d": 24}

# Etwas Puffer ueber 7 Tage hinaus behalten, falls einzelne Laeufe ausfallen
HISTORY_RETENTION_HOURS = 24 * 8


def load_history() -> dict:
    if not os.path.exists(HISTORY_FILE):
        return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("WARNUNG: history.json konnte nicht gelesen werden, starte neu.", file=sys.stderr)
        return {}


def prune_history(entries: list, now: datetime) -> list:
    cutoff = now - timedelta(hours=HISTORY_RETENTION_HOURS)
    cutoff_iso = cutoff.isoformat(timespec="seconds")
    return [e for e in entries if e["t"] >= cutoff_iso]


def value_at_or_before(entries: list, target_iso: str):
    """Sucht den juengsten History-Eintrag, dessen Zeitstempel <= target_iso ist.
    ISO-8601-Zeitstempel (mit Zeitzone, fester Breite) sind lexikografisch
    sortierbar, ein String-Vergleich reicht daher aus.
    Gibt (wert, zeitstempel) zurueck, oder (None, None) wenn nichts gefunden."""
    candidates = [e for e in entries if e["t"] <= target_iso]
    if not candidates:
        return None, None
    best = max(candidates, key=lambda e: e["t"])
    return best["v"], best["t"]


def compute_trends(entries: list, current_value: float, now: datetime) -> dict:
    trends = {}
    for label, hours_ago in TREND_WINDOWS.items():
        target_time = now - timedelta(hours=hours_ago)
        target_iso = target_time.isoformat(timespec="seconds")
        old_value, found_iso = value_at_or_before(entries, target_iso)

        if old_value is None or old_value == 0 or current_value is None:
            trends[label] = None
            continue

        # Toleranzpruefung: liegt der gefundene Snapshot zu weit vom
        # gewuenschten Zeitpunkt entfernt (z.B. weil das Skript zwischenzeitlich
        # nicht lief), lieber None statt eines irrefuehrenden Wertes liefern.
        found_time = datetime.fromisoformat(found_iso)
        deviation_hours = abs((target_time - found_time).total_seconds()) / 3600
        tolerance = TREND_TOLERANCE_HOURS.get(label, hours_ago)

        if deviation_hours > tolerance:
            trends[label] = None
        else:
            trends[label] = round((current_value - old_value) / old_value * 100, 2)
    return trends



def http_get_json(url: str) -> dict:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_all_leagues() -> list:
    """Holt die vollstaendige Liga-Liste von poe.ninja.
    Laut Doku ist der erste Eintrag immer die aktuelle Challenge-Liga."""
    leagues = http_get_json(f"{BASE_URL}/leagues")
    if not leagues:
        raise RuntimeError("Keine Ligen von poe.ninja erhalten")
    return leagues


def get_target_leagues(all_leagues: list) -> list:
    """Bestimmt, welche Ligen getrackt werden sollen.

    Standardmaessig: ALLE von poe.ninja gelieferten Ligen. Das ist bewusst
    so gewaehlt, weil PoE2 zeitweise mehrere parallele Challenge-Ligen haben
    kann (z.B. "Runes of Aldur" und zusaetzlich die Event-Liga
    "Forbidden Rites" liefen im September 2026 gleichzeitig) - eine feste
    Auswahl wie "nur die erste Liga + Standard + Hardcore" wuerde solche
    zusaetzlichen Ligen stillschweigend auslassen.

    Ueber die Umgebungsvariable POE2_LEAGUES (kommagetrennte Liga-IDs) kann
    das eingeschraenkt werden, z.B.:
        POE2_LEAGUES="Standard,Hardcore"
    """
    override = os.environ.get("POE2_LEAGUES")
    if override:
        by_id = {l["id"]: l for l in all_leagues}
        ids = [x.strip() for x in override.split(",") if x.strip()]
        return [{"id": i, "name": by_id.get(i, {}).get("name", i)} for i in ids]

    return all_leagues


def value_in_currency(primary_value: float, primary_id: str, rates: dict, target: str) -> float | None:
    """Rechnet einen in der Primaerwaehrung angegebenen Wert in eine
    Zielwaehrung (chaos/exalted/divine) um."""
    if target == primary_id:
        return round(primary_value, 6)
    rate = rates.get(target)
    if rate is None:
        return None
    return round(primary_value * rate, 6)


def fetch_category(league: str, category: str, league_history: dict, now: datetime) -> tuple:
    # Liga-IDs koennen Leerzeichen enthalten (z.B. "Forbidden Rites") - muessen
    # deshalb URL-kodiert werden, sonst lehnt Python/der Server die Anfrage ab.
    url = f"{BASE_URL}/exchange/current/overview?league={quote(league)}&type={quote(category)}"
    payload = http_get_json(url)

    core = payload.get("core", {})
    primary_id = core.get("primary")
    rates = core.get("rates", {})
    # WICHTIG: core["items"] enthaelt nur die 2-3 Referenzwaehrungen fuer die
    # Kursberechnung (z.B. Divine/Chaos/Exalted). Die vollstaendigen Namen und
    # Icon-Pfade fuer ALLE Items der Kategorie stehen auf oberster Ebene der
    # Antwort unter payload["items"] - nicht unter core["items"].
    items_meta = {item["id"]: item for item in payload.get("items", [])}

    category_history = league_history.setdefault(category, {})
    now_iso = now.isoformat(timespec="seconds")

    results = []
    for line in payload.get("lines", []):
        item_id = line["id"]
        meta = items_meta.get(item_id, {})
        primary_value = line.get("primaryValue", 0)

        values = {}
        for target in TARGET_CURRENCIES:
            values[target] = value_in_currency(primary_value, primary_id, rates, target)

        # History fuer dieses Item fortschreiben: aktuellen Snapshot anhaengen,
        # alte Eintraege jenseits der Aufbewahrungsfrist verwerfen.
        entries = category_history.setdefault(item_id, [])
        trend = compute_trends(entries, primary_value, now)
        entries.append({"t": now_iso, "v": primary_value})
        category_history[item_id] = prune_history(entries, now)

        results.append({
            "id": item_id,
            "name": meta.get("name", item_id),
            "icon": meta.get("image"),
            "values": values,
            "listingVolumePrimary": line.get("volumePrimaryValue"),
            "trend": trend,
        })

    # Teuerste Items zuerst (in Chaos, da das immer vorhanden sein sollte)
    results.sort(key=lambda x: x["values"].get("chaos") or 0, reverse=True)
    return results, core


def extract_exchange_rates(core: dict) -> dict:
    """Baut eine vollstaendige Kursmatrix zwischen Divine, Chaos und Exalted
    aus dem core-Block einer beliebigen Kategorie-Antwort. Diese Kurse sind
    liga-weit und unabhaengig von der jeweils abgefragten Kategorie.

    Rueckgabeformat:
        { "divine": {"chaos": .., "exalted": ..},
          "chaos":  {"divine": .., "exalted": ..},
          "exalted": {"divine": .., "chaos": ..} }
    """
    rates = core.get("rates", {})
    divine_to_chaos = rates.get("chaos")
    divine_to_exalted = rates.get("exalted")

    if not divine_to_chaos or not divine_to_exalted:
        return {}

    chaos_to_divine = round(1 / divine_to_chaos, 6)
    exalted_to_divine = round(1 / divine_to_exalted, 6)
    exalted_to_chaos = round(divine_to_chaos / divine_to_exalted, 6)
    chaos_to_exalted = round(divine_to_exalted / divine_to_chaos, 6)

    return {
        "divine": {"chaos": round(divine_to_chaos, 6), "exalted": round(divine_to_exalted, 6)},
        "chaos": {"divine": chaos_to_divine, "exalted": chaos_to_exalted},
        "exalted": {"divine": exalted_to_divine, "chaos": exalted_to_chaos},
    }


def dedupe_currency_category(categories_data: dict) -> dict:
    """poe.ninja liefert im 'Currency'-Endpunkt teils auch Items zurueck, die
    zusaetzlich in spezifischeren Kategorien (Fragments, Breach/Catalysts,
    Ritual/Omens, ...) auftauchen. Damit die 'Currency'-Ansicht im Dashboard
    nur echte Currency-Orbs zeigt, werden alle Item-IDs entfernt, die bereits
    in einer anderen Kategorie vorkommen."""
    if "Currency" not in categories_data:
        return categories_data

    other_ids = set()
    for cat, items in categories_data.items():
        if cat == "Currency":
            continue
        for item in items:
            other_ids.add(item["id"])

    before = len(categories_data["Currency"])
    categories_data["Currency"] = [
        item for item in categories_data["Currency"] if item["id"] not in other_ids
    ]
    removed = before - len(categories_data["Currency"])
    if removed:
        print(f"  (Currency bereinigt: {removed} Ueberschneidung(en) mit anderen Kategorien entfernt)")

    return categories_data


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        all_leagues = get_all_leagues()
        target_leagues = get_target_leagues(all_leagues)
    except (HTTPError, URLError, RuntimeError) as exc:
        print(f"FEHLER beim Abrufen der Liga-Liste: {exc}", file=sys.stderr)
        sys.exit(1)

    if not target_leagues:
        print("FEHLER: Keine passenden Ligen gefunden.", file=sys.stderr)
        sys.exit(1)

    print("Verwende Ligen: " + ", ".join(f"{l['id']}" for l in target_leagues))

    now = datetime.now(timezone.utc)
    history = load_history()  # Struktur: { league_id: { category: { item_id: [...] } } }

    leagues_output = {}
    for league in target_leagues:
        league_id = league["id"]
        print(f"--- Liga: {league_id} ---")
        league_history = history.setdefault(league_id, {})

        categories_data = {}
        exchange_rates = None
        for category in CATEGORIES:
            try:
                print(f"  Abrufen: {category} ...")
                results, core = fetch_category(league_id, category, league_history, now)
                categories_data[category] = results
                # Wechselkurse muessen nur einmal pro Liga extrahiert werden -
                # sie sind nicht kategorie-spezifisch, sondern liga-weit gueltig.
                if exchange_rates is None:
                    exchange_rates = extract_exchange_rates(core)
            except (HTTPError, URLError) as exc:
                print(f"  WARNUNG: {category} ({league_id}) konnte nicht geladen werden: {exc}", file=sys.stderr)
            # kleine Pause zwischen Requests - freundlich zur API
            time.sleep(1.5)

        if categories_data:
            categories_data = dedupe_currency_category(categories_data)
            leagues_output[league_id] = {
                "name": league.get("name", league_id),
                "exchangeRates": exchange_rates,
                "categories": categories_data,
            }
        else:
            print(f"  WARNUNG: Liga {league_id} lieferte keine Daten, wird ausgelassen.", file=sys.stderr)

    if not leagues_output:
        print("FEHLER: Keine einzige Liga konnte geladen werden.", file=sys.stderr)
        sys.exit(1)

    output = {
        "generated_at": now.isoformat(timespec="seconds"),
        "currencies": TARGET_CURRENCIES,
        "trendWindows": list(TREND_WINDOWS.keys()),
        "categoryLabels": CATEGORY_LABELS,
        "defaultLeague": target_leagues[0]["id"],
        "leagues": leagues_output,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False)

    print(f"Fertig. {len(leagues_output)} Liga(en) gespeichert in {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
