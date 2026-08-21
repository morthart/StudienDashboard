from enum import Enum
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
class SemesterStatus(Enum):
    """Beschreibt den automatisch berechneten Status eines Semesters."""

    NICHT_BEGONNEN = "nicht_begonnen"
    BEGONNEN = "begonnen"
    ABGESCHLOSSEN = "abgeschlossen"
# ======================================================================================================================================================


# ======================================================================================================================================================
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
