from __future__ import annotations
# Dieses Modul: Definiert die Daten und fachlichen Zustandsabfragen eines einzelnen Kurses.

from dataclasses import dataclass
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from enums import KursStatus
from konstanten import MIN_ECTS_PRO_KURS, ZULAESSIGE_KURSNOTEN
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
@dataclass
# Klasse Kurs: Speichert die Daten eines Kurses innerhalb eines Semesters.
class Kurs:
    """Speichert die Daten eines Kurses innerhalb eines Semesters."""

    name: str
    status: KursStatus
    ects: int
    note: float | None = None


    def __post_init__(self) -> None:
        """Normalisiert und prüft die Kursdaten direkt nach dem Erzeugen."""

        if self.note is not None:
            self.note = float(self.note)

        self.validiere_daten()

    def validiere_daten(self) -> None:
        """Verhindert unvollständige oder widersprüchliche Kursdaten."""

        if not self.name.strip():
            raise ValueError("Der Kursname darf nicht leer sein.")

        if self.ects <= 0:
            raise ValueError("Die ECTS eines Kurses müssen größer als 0 sein.")

        if self.ects % MIN_ECTS_PRO_KURS != 0:
            raise ValueError(f"Die ECTS eines Kurses müssen durch {MIN_ECTS_PRO_KURS} teilbar sein.")

        if self.note is not None:
            if self.note not in ZULAESSIGE_KURSNOTEN:
                raise ValueError("Die gespeicherte Kursnote ist nicht zulässig.")

        if self.status == KursStatus.ABGESCHLOSSEN and self.note is None:
            raise ValueError("Ein abgeschlossener Kurs benötigt eine Note.")

        if self.status != KursStatus.ABGESCHLOSSEN and self.note is not None:
            raise ValueError("Nur ein abgeschlossener Kurs darf eine Note besitzen.")

    def berechne_erreichte_ects(self) -> int:
        """Gibt die ECTS nur für bestandene oder anerkannte Kurse zurück."""

        if self.ist_nicht_bestanden():
            return 0

        if self.status.ects_werden_angerechnet():
            return self.ects

        return 0

    def ist_nicht_bestanden(self) -> bool:
        """Prüft, ob der Kurs mit der Note 5.0 abgeschlossen wurde."""

        return self.status == KursStatus.ABGESCHLOSSEN and self.note == 5.0

    def hat_note(self) -> bool:
        """Prüft, ob für den Kurs eine Note gespeichert wurde."""

        return self.note is not None

# ======================================================================================================================================================
