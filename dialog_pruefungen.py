# Dieses Modul: Enthält zentral verwendete Prüfungen und Umwandlungen für Benutzereingaben.
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from konstanten import (
    ECTS_PRO_SEMESTER,
    MAX_GESAMT_ECTS,
    MIN_ECTS_PRO_KURS,
    MIN_GESAMT_ECTS,
    ZULAESSIGE_KURSNOTEN
)
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
def pruefe_name(eingabe: str, fehlermeldung: str) -> str:
    """Prüft einen Namen und gibt den bereinigten Text zurück."""

    name = eingabe.strip()

    if not name:
        raise ValueError(fehlermeldung)

    return name
# ======================================================================================================================================================


# ======================================================================================================================================================
def pruefe_wunschnote(eingabe: str) -> float:
    """Prüft die frei eingebbare Wunschnote und rundet sie auf eine Nachkommastelle."""

    note_text = eingabe.strip()

    if not note_text:
        raise ValueError("Bitte Wunschnote eingeben.")

    # Fehler bei Datei-, Konfigurations- oder Benutzervorgängen werden hier kontrolliert behandelt, statt die Anwendung abzubrechen.
    try:
        note = float(note_text.replace(",", "."))
    except ValueError as fehler:
        raise ValueError("Bitte eine gültige Wunschnote eingeben.") from fehler

    note = round(note, 1)

    if note < 1.0 or note > 4.0:
        raise ValueError("Die Wunschnote muss zwischen 1.0 und 4.0 liegen.")

    return note
# ======================================================================================================================================================


# ======================================================================================================================================================
def pruefe_kursnote(eingabe: str) -> float:
    """Akzeptiert ausschließlich die festgelegten Kursnoten."""

    note_text = eingabe.strip()

    if not note_text:
        raise ValueError("Bitte Note eingeben.")

    # Fehler bei Datei-, Konfigurations- oder Benutzervorgängen werden hier kontrolliert behandelt, statt die Anwendung abzubrechen.
    try:
        note = float(note_text.replace(",", "."))
    except ValueError as fehler:
        raise ValueError("Bitte eine gültige Note eingeben.") from fehler

    if note not in ZULAESSIGE_KURSNOTEN:
        erlaubte_noten = "; ".join(f"{wert:.1f}" for wert in ZULAESSIGE_KURSNOTEN)
        raise ValueError(f"Erlaubte Noten sind: {erlaubte_noten}")

    return note
# ======================================================================================================================================================


# ======================================================================================================================================================
def pruefe_gesamt_ects_wert(eingabe: str, min_gesamt_ects: int) -> int:
    """Prüft Gesamt-ECTS auf Ganzzahl, Bereich, Teilbarkeit und vorhandene Semester."""

    ects_text = eingabe.strip()

    if not ects_text:
        raise ValueError("Bitte Gesamt-ECTS eingeben.")

    # Fehler bei Datei-, Konfigurations- oder Benutzervorgängen werden hier kontrolliert behandelt, statt die Anwendung abzubrechen.
    try:
        gesamt_ects = int(ects_text)
    except ValueError as fehler:
        raise ValueError("Gesamt-ECTS müssen als ganze Zahl eingegeben werden.") from fehler

    if gesamt_ects < 0:
        raise ValueError("Positiv bitte du Witzbold (:")

    if gesamt_ects % ECTS_PRO_SEMESTER != 0:
        raise ValueError(f"Bitte ein Vielfaches von {ECTS_PRO_SEMESTER} eingeben")

    if gesamt_ects < MIN_GESAMT_ECTS:
        raise ValueError(f"Gesamt-ECTS müssen mindestens {MIN_GESAMT_ECTS} betragen.")

    if gesamt_ects > MAX_GESAMT_ECTS:
        raise ValueError(f"Gesamt-ECTS dürfen höchstens {MAX_GESAMT_ECTS} betragen.")

    if gesamt_ects < min_gesamt_ects:
        anzahl_semester = min_gesamt_ects // ECTS_PRO_SEMESTER
        raise ValueError(
            f"Kann nicht unter {min_gesamt_ects} reduziert werden, da "
            f"{anzahl_semester} Semester in diesem Studiengang angelegt wurden."
        )

    return gesamt_ects
# ======================================================================================================================================================


# ======================================================================================================================================================
def pruefe_kurs_ects_wert(eingabe: str, max_ects: int) -> int:
    """Prüft Kurs-ECTS auf Ganzzahl, positive Werte, Teilbarkeit und Semesterlimit."""

    ects_text = eingabe.strip()

    if not ects_text:
        raise ValueError("Bitte ECTS eingeben")

    # Fehler bei Datei-, Konfigurations- oder Benutzervorgängen werden hier kontrolliert behandelt, statt die Anwendung abzubrechen.
    try:
        ects = int(ects_text)
    except ValueError as fehler:
        raise ValueError("Bitte ECTS als ganze Zahl eingeben.") from fehler

    if ects < 0:
        raise ValueError("Positiv bitte du Witzbold (:")

    if ects == 0 or ects % MIN_ECTS_PRO_KURS != 0:
        raise ValueError(f"Bitte ein Vielfaches von {MIN_ECTS_PRO_KURS} eingeben")

    if ects > max_ects:
        raise ValueError(f"Für diesen Kurs können höchstens {max_ects} ECTS eingetragen werden.")

    return ects
# ======================================================================================================================================================
