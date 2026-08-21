# Dieses Modul: Definiert die festen Statuswerte für Semester, Kurse und Teilaufgaben.
from enum import Enum
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
# Klasse SemesterStatus: Beschreibt den automatisch berechneten Status eines Semesters.
class SemesterStatus(Enum):
    """Beschreibt den automatisch berechneten Status eines Semesters."""

    NICHT_BEGONNEN = "nicht_begonnen"
    BEGONNEN = "begonnen"
    ABGESCHLOSSEN = "abgeschlossen"
# ======================================================================================================================================================


# ======================================================================================================================================================
# Klasse KursStatus: Beschreibt den Bearbeitungsstatus eines Kurses.
class KursStatus(Enum):
    """Beschreibt den Bearbeitungsstatus eines Kurses."""

    NICHT_BEGONNEN = "nicht_begonnen"
    BEGONNEN = "begonnen"
    ABGESCHLOSSEN = "abgeschlossen"
    ANERKANNT = "anerkannt"

    def ects_werden_angerechnet(self) -> bool:
        """Gibt zurück, ob die ECTS des Kurses als erreicht gelten."""

        if self == KursStatus.ABGESCHLOSSEN:
            return True

        if self == KursStatus.ANERKANNT:
            return True

        return False
# ======================================================================================================================================================
