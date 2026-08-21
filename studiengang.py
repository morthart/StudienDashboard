from __future__ import annotations
# Dieses Modul: Definiert Studiengangsdaten und berechnet ECTS-, Semester- und Notenkennzahlen.

from dataclasses import dataclass
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from enums import KursStatus, SemesterStatus
from konstanten import ECTS_PRO_SEMESTER
from semester import Semester
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
@dataclass
# Klasse Studiengang: Speichert den Studiengang und alle zugehörigen Semester.
class Studiengang:
    """Speichert den Studiengang und alle zugehörigen Semester."""

    name: str
    wunschnote: float
    gesamt_ects: int
    semester: list[Semester]

    def __post_init__(self) -> None:
        """Normalisiert grundlegende Studiengangsdaten nach dem Erzeugen."""

        self.wunschnote = round(float(self.wunschnote), 1)

    def berechne_max_semester(self) -> int:
        """Berechnet die maximale Semesteranzahl aus den Gesamt-ECTS."""

        return self.gesamt_ects // ECTS_PRO_SEMESTER

    def berechne_hoechste_semesternummer(self) -> int:
        """Ermittelt die höchste Nummer der bereits angelegten Semester."""

        hoechste_nummer = 0

        # Die vorhandenen Elemente werden nacheinander ausgewertet, damit aus ihrem aktuellen Zustand das Ergebnis ermittelt werden kann.
        for semester in self.semester:
            if semester.nummer > hoechste_nummer:
                hoechste_nummer = semester.nummer

        return hoechste_nummer

    def berechne_min_gesamt_ects(self) -> int:
        """Berechnet die kleinsten Gesamt-ECTS, die vorhandene Semester erlauben."""

        anzahl_semester = len(self.semester)
        hoechste_nummer = self.berechne_hoechste_semesternummer()
        notwendige_semester = anzahl_semester

        if hoechste_nummer > notwendige_semester:
            notwendige_semester = hoechste_nummer

        return notwendige_semester * ECTS_PRO_SEMESTER

    def berechne_erreichte_ects(self) -> int:
        """Berechnet die erreichten ECTS des gesamten Studiengangs."""

        gesamt = 0

        for semester in self.semester:
            gesamt = gesamt + semester.berechne_erreichte_ects()

        return gesamt

    def berechne_abgeschlossene_semester(self) -> int:
        """Zählt Semester, deren Status abgeschlossen ist."""

        anzahl = 0

        # Die vorhandenen Elemente werden nacheinander ausgewertet, damit aus ihrem aktuellen Zustand das Ergebnis ermittelt werden kann.
        for semester in self.semester:
            if semester.berechne_status() == SemesterStatus.ABGESCHLOSSEN:
                anzahl = anzahl + 1

        return anzahl

    def hat_nicht_bestandenen_kurs(self) -> bool:
        """Prüft, ob im Studiengang mindestens ein Kurs mit 5.0 bewertet wurde."""

        # Die vorhandenen Elemente werden nacheinander ausgewertet, damit aus ihrem aktuellen Zustand das Ergebnis ermittelt werden kann.
        for semester in self.semester:
            if semester.hat_nicht_bestandenen_kurs():
                return True

        return False

    def berechne_notendaten(self) -> tuple[float, int, int]:
        """Sammelt gewichtete Noten, benotete ECTS und anerkannte ECTS."""

        gewichtete_noten = 0.0
        benotete_ects = 0
        anerkannte_ects = 0

        # Die vorhandenen Elemente werden nacheinander ausgewertet, damit aus ihrem aktuellen Zustand das Ergebnis ermittelt werden kann.
        for semester in self.semester:
            # Die vorhandenen Elemente werden nacheinander ausgewertet, damit aus ihrem aktuellen Zustand das Ergebnis ermittelt werden kann.
            for kurs in semester.kurse:
                # Anerkannte Kurse zählen zu den erreichten ECTS, besitzen aber keine reguläre Kursnote.
                if kurs.status == KursStatus.ANERKANNT:
                    anerkannte_ects = anerkannte_ects + kurs.ects

                # Nur tatsächlich vorhandene Noten dürfen in den gewichteten Notenschnitt einfließen.
                if kurs.note is not None:
                    gewichtete_noten = gewichtete_noten + (kurs.note * kurs.ects)
                    benotete_ects = benotete_ects + kurs.ects

        return gewichtete_noten, benotete_ects, anerkannte_ects

    def berechne_notenschnitt(self) -> float | None:
        """Berechnet den nach ECTS gewichteten Schnitt aller benoteten Kurse."""

        gewichtete_noten, benotete_ects, _anerkannte_ects = self.berechne_notendaten()

        if benotete_ects == 0:
            return None

        return gewichtete_noten / benotete_ects

    def berechne_benoetigten_schnitt(self) -> float | None:
        """Berechnet den nötigen Schnitt der zukünftigen benoteten ECTS."""

        gewichtete_noten, benotete_ects, anerkannte_ects = self.berechne_notendaten()

        # Anerkannte ECTS werden abgezogen, weil für sie keine zukünftige Note mehr benötigt wird.
        maximal_benotete_ects = self.gesamt_ects - anerkannte_ects
        verbleibende_ects = maximal_benotete_ects - benotete_ects

        if verbleibende_ects <= 0:
            return None

        # Für die Zielnote wird zuerst die insgesamt benötigte gewichtete Notensumme bestimmt.
        ziel_notenpunkte = self.wunschnote * maximal_benotete_ects
        # Von der Zielsumme werden die bereits erreichten gewichteten Notenpunkte abgezogen.
        fehlende_notenpunkte = ziel_notenpunkte - gewichtete_noten

        return fehlende_notenpunkte / verbleibende_ects

    def semester_nummer_vorhanden(self, nummer: int, ausnahme: Semester | None = None) -> bool:
        """Prüft, ob die Nummer durch ein anderes Semester belegt ist."""

        # Die vorhandenen Elemente werden nacheinander ausgewertet, damit aus ihrem aktuellen Zustand das Ergebnis ermittelt werden kann.
        for semester in self.semester:
            if semester is ausnahme:
                continue

            if semester.nummer == nummer:
                return True

        return False

    def finde_semester(self, nummer: int) -> Semester | None:
        """Sucht ein Semester anhand seiner Nummer."""

        # Die vorhandenen Elemente werden nacheinander ausgewertet, damit aus ihrem aktuellen Zustand das Ergebnis ermittelt werden kann.
        for semester in self.semester:
            if semester.nummer == nummer:
                return semester

        return None

    def naechste_freie_semesternummer(self) -> int | None:
        """Gibt die erste noch freie Semesternummer zurück."""

        nummer = 1
        max_semester = self.berechne_max_semester()

        # Die Suche wird nur so lange fortgesetzt, bis die fachliche Grenze erreicht oder ein passender Wert gefunden wurde.
        while nummer <= max_semester:
            if not self.semester_nummer_vorhanden(nummer):
                return nummer

            nummer = nummer + 1

        return None

    def sortiere_semester(self) -> None:
        """Sortiert die Semester aufsteigend nach ihrer Nummer."""

        # Die Sortierung hält die Anzeige unabhängig von der Reihenfolge des Anlegens chronologisch.
        self.semester.sort(key = lambda semester: semester.nummer)

# ======================================================================================================================================================
