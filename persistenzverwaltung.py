# Dieses Modul: Kapselt die Dateioperationen und delegiert die JSON-Umwandlung an JsonDatenhaltung.
import re
from pathlib import Path
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from anwendungsdaten import Configuration
from json_verwaltung import JsonDatenhaltung
from studiengang import Studiengang
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
# Klasse PersistenzVerwaltung: Kapselt Dateisystem, Dateinamen und JSON-Datenhaltung an einer zentralen Stelle.
class PersistenzVerwaltung:
    """Kapselt Dateisystem, Dateinamen und JSON-Datenhaltung an einer zentralen Stelle."""
# ======================================================================================================================================================


# ======================================================================================================================================================
    def __init__(self) -> None:
        """Verwendet JsonDatenhaltung für die eigentliche Umwandlung der Daten."""

        self.datenhaltung = JsonDatenhaltung()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def dateiname_erzeugen(self, name: str) -> str:
        """Erzeugt aus einem Studiengangsnamen einen sicheren JSON-Dateinamen."""

        dateiname = name.strip().lower()
        dateiname = re.sub(r"[^a-z0-9äöüß_-]+", "_", dateiname)
        dateiname = dateiname.strip("_")

        if not dateiname:
            dateiname = "studiengang"

        return f"{dateiname}.json"
# ======================================================================================================================================================


# ======================================================================================================================================================
    def studiengang_dateipfad(self, speicherort: Path, name: str) -> Path:
        """Erzeugt den vollständigen Dateipfad eines Studiengangs."""

        return speicherort / self.dateiname_erzeugen(name)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def datei_existiert(self, dateipfad: Path | None) -> bool:
        """Prüft, ob ein Pfad auf eine vorhandene Datei zeigt."""

        if dateipfad is None:
            return False

        return dateipfad.is_file()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def ordner_existiert(self, ordner: Path) -> bool:
        """Prüft, ob der angegebene Ordner vorhanden ist."""

        return ordner.is_dir()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def erstelle_ordner(self, ordner: Path) -> None:
        """Legt einen Ordner einschließlich fehlender übergeordneter Ordner an."""

        ordner.mkdir(parents = True, exist_ok = True)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def finde_json_dateien(self, ordner: Path) -> list[Path]:
        """Liefert alle JSON-Dateien eines Ordners sortiert zurück."""

        if not ordner.is_dir():
            return []

        return sorted(ordner.glob("*.json"))
# ======================================================================================================================================================


# ======================================================================================================================================================
    def loesche_datei(self, dateipfad: Path | None) -> None:
        """Löscht eine Datei, sofern sie vorhanden ist."""

        if dateipfad is None or not dateipfad.is_file():
            return

        dateipfad.unlink()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def speichere_studiengang(self, studiengang: Studiengang, dateipfad: Path) -> None:
        """Speichert einen Studiengang über die JSON-Datenhaltung."""

        self.datenhaltung.speichere_studiengang(studiengang, dateipfad)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def lade_studiengang(self, dateipfad: Path) -> Studiengang:
        """Lädt einen Studiengang über die JSON-Datenhaltung."""

        return self.datenhaltung.lade_studiengang(dateipfad)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def lade_studiengang_sicher(self, dateipfad: Path) -> Studiengang | None:
        """Lädt einen Studiengang für Listen oder Programmstart; fehlerhafte Dateien werden ausgelassen."""

        # Fehler bei Datei-, Konfigurations- oder Benutzervorgängen werden hier kontrolliert behandelt, statt die Anwendung abzubrechen.
        try:
            return self.lade_studiengang(dateipfad)
        except (OSError, KeyError, TypeError, ValueError):
            return None
# ======================================================================================================================================================


# ======================================================================================================================================================
    def speichere_configuration(self, configuration: Configuration, dateipfad: Path) -> None:
        """Speichert die Programmeinstellungen über die JSON-Datenhaltung."""

        self.datenhaltung.speichere_configuration(configuration, dateipfad)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def lade_configuration_sicher(self, dateipfad: Path) -> Configuration | None:
        """Lädt die Configuration; eine fehlende oder ungültige Datei liefert None."""

        if not self.datei_existiert(dateipfad):
            return None

        # Fehler bei Datei-, Konfigurations- oder Benutzervorgängen werden hier kontrolliert behandelt, statt die Anwendung abzubrechen.
        try:
            return self.datenhaltung.lade_configuration(dateipfad)
        except (OSError, KeyError, TypeError, ValueError):
            return None
# ======================================================================================================================================================
