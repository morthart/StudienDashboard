from __future__ import annotations
# Dieses Modul: Definiert Semesterdaten und leitet Status sowie ECTS aus den enthaltenen Kursen ab.

from dataclasses import dataclass
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from enums import KursStatus, SemesterStatus
from konstanten import ECTS_PRO_SEMESTER, MAX_KURSE_PRO_SEMESTER, MIN_ECTS_PRO_KURS
from kurs import Kurs
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
@dataclass
# Klasse Semester: Speichert die Nummer und alle Kurse eines Semesters.
class Semester:
    """Speichert die Nummer und alle Kurse eines Semesters."""

    nummer: int
    kurse: list[Kurs]

    def berechne_zugewiesene_ects(self) -> int:
        """Berechnet die Summe aller ECTS, die durch Kurse belegt sind."""

        gesamt = 0

        for kurs in self.kurse:
            gesamt = gesamt + kurs.ects

        return gesamt

    def berechne_erreichte_ects(self) -> int:
        """Berechnet die Summe der abgeschlossenen oder anerkannten ECTS."""

        gesamt = 0

        for kurs in self.kurse:
            gesamt = gesamt + kurs.berechne_erreichte_ects()

        return gesamt

    def berechne_freie_ects(self) -> int:
        """Berechnet die noch freien ECTS bis zum festen Semesterlimit."""

        return ECTS_PRO_SEMESTER - self.berechne_zugewiesene_ects()

    def sind_alle_kurse_fertig(self) -> bool:
        """Prüft, ob die ECTS aller vorhandenen Kurse angerechnet werden."""

        # Die vorhandenen Elemente werden nacheinander ausgewertet, damit aus ihrem aktuellen Zustand das Ergebnis ermittelt werden kann.
        for kurs in self.kurse:
            if kurs.berechne_erreichte_ects() != kurs.ects:
                return False

        return True

    def hat_nicht_bestandenen_kurs(self) -> bool:
        """Prüft, ob mindestens ein Kurs des Semesters mit 5.0 bewertet wurde."""

        # Die vorhandenen Elemente werden nacheinander ausgewertet, damit aus ihrem aktuellen Zustand das Ergebnis ermittelt werden kann.
        for kurs in self.kurse:
            if kurs.ist_nicht_bestanden():
                return True

        return False

    def wurde_mindestens_ein_kurs_begonnen(self) -> bool:
        """Prüft, ob mindestens ein Kurs begonnen, abgeschlossen oder anerkannt ist."""

        # Die vorhandenen Elemente werden nacheinander ausgewertet, damit aus ihrem aktuellen Zustand das Ergebnis ermittelt werden kann.
        for kurs in self.kurse:
            if kurs.status != KursStatus.NICHT_BEGONNEN:
                return True

        return False

    def berechne_status(self) -> SemesterStatus:
        """Leitet den Semesterstatus automatisch aus den Kursstatus ab."""

        if not self.kurse:
            return SemesterStatus.NICHT_BEGONNEN

        alle_kurse_fertig = self.sind_alle_kurse_fertig()
        mindestens_ein_kurs_begonnen = self.wurde_mindestens_ein_kurs_begonnen()

        if self.berechne_zugewiesene_ects() == ECTS_PRO_SEMESTER and alle_kurse_fertig:
            return SemesterStatus.ABGESCHLOSSEN

        if mindestens_ein_kurs_begonnen:
            return SemesterStatus.BEGONNEN

        return SemesterStatus.NICHT_BEGONNEN

    def kann_kurs_aufnehmen(self, ects: int, bisherige_ects: int = 0) -> bool:
        """Prüft, ob ein neuer oder geänderter Kurs in das Semester passt."""

        neue_summe = self.berechne_zugewiesene_ects()
        neue_summe = neue_summe - bisherige_ects
        neue_summe = neue_summe + ects

        if neue_summe > ECTS_PRO_SEMESTER:
            return False

        return True

    def kann_weiteren_kurs_aufnehmen(self) -> bool:
        """Prüft ECTS-Limit und maximale Anzahl der Kurskarten."""

        if len(self.kurse) >= MAX_KURSE_PRO_SEMESTER:
            return False

        if self.berechne_freie_ects() < MIN_ECTS_PRO_KURS:
            return False

        return True

    def finde_kurs(self, name: str) -> Kurs | None:
        """Sucht einen Kurs anhand seines Namens ohne Beachtung der Großschreibung."""

        # Die vorhandenen Elemente werden nacheinander ausgewertet, damit aus ihrem aktuellen Zustand das Ergebnis ermittelt werden kann.
        for kurs in self.kurse:
            if kurs.name.casefold() == name.casefold():
                return kurs

        return None

    def sortiere_kurse(self) -> None:
        """Sortiert alle Kurse alphabetisch."""

        self.kurse.sort(key = lambda kurs: kurs.name.casefold())

# ======================================================================================================================================================
