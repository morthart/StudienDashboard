from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from kurs import Kurs
from semester import Semester
from studiengang import Studiengang
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
@dataclass
class Configuration:
    """Speichert technische Einstellungen des Programms."""

    eyecatcher: str
    schema_version: int
    speicherort: Path
    letzter_studiengang: Path | None
# ======================================================================================================================================================


# ======================================================================================================================================================
@dataclass
class Anwendungszustand:
    """Enthält den veränderlichen Zustand der laufenden Anwendung.

    Der Zustand ist bewusst von der Tkinter-Oberfläche getrennt. Verwaltungs- und
    Steuerungsklassen können dadurch mit den Daten arbeiten, ohne das Hauptfenster
    oder andere GUI-Objekte kennen zu müssen.
    """

    config_pfad: Path
    configuration: Configuration | None = None
    studiengang: Studiengang | None = None
    aktuelles_semester: Semester | None = None
    aktueller_kurs: Kurs | None = None
# ======================================================================================================================================================
