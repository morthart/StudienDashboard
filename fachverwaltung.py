# Dieses Modul: Ändert die fachlichen Objekte Studiengang, Semester und Kurs ohne Abhängigkeit von der GUI.
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# Fachliche Verwaltung
#
# Die drei Verwaltungsklassen gehören zur gleichen Schicht und stehen deshalb gemeinsam
# in diesem Modul. Die Klassen bleiben weiterhin klar getrennt und besitzen jeweils nur
# die Verantwortung für Studiengang, Semester oder Kurs.
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------------------------------------------------
from anwendungsdaten import Anwendungszustand
from enums import KursStatus
from konstanten import ECTS_PRO_SEMESTER, ZULAESSIGE_KURSNOTEN
from kurs import Kurs
from semester import Semester
from studiengang import Studiengang
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
# Klasse StudiengangVerwaltung: Erstellt und verändert Studiengangsobjekte ohne GUI- oder Persistenzabhängigkeit.
class StudiengangVerwaltung:
    """Erstellt und verändert Studiengangsobjekte ohne GUI- oder Persistenzabhängigkeit."""
# ======================================================================================================================================================


# ======================================================================================================================================================
    def __init__(self, zustand: Anwendungszustand) -> None:
        """Verknüpft die Verwaltung ausschließlich mit dem gemeinsamen Anwendungszustand."""

        self.zustand = zustand
# ======================================================================================================================================================


# ======================================================================================================================================================
    def erstelle_studiengang(
            self,
            name: str,
            wunschnote: float,
            gesamt_ects: int
    ) -> Studiengang:
        """Erzeugt einen neuen Studiengang, ohne ihn bereits zu speichern oder auszuwählen."""

        return Studiengang(
            name = name,
            wunschnote = wunschnote,
            gesamt_ects = gesamt_ects,
            semester = []
        )
# ======================================================================================================================================================


# ======================================================================================================================================================
    def erstelle_bearbeiteten_studiengang(
            self,
            name: str,
            wunschnote: float,
            gesamt_ects: int
    ) -> Studiengang:
        """Erzeugt aus dem aktuellen Studiengang eine bearbeitete Fassung mit denselben Semestern."""

        if self.zustand.studiengang is None:
            raise ValueError("Bitte zuerst einen Studiengang anlegen oder wechseln.")

        return Studiengang(
            name = name,
            wunschnote = wunschnote,
            gesamt_ects = gesamt_ects,
            semester = self.zustand.studiengang.semester
        )
# ======================================================================================================================================================


# ======================================================================================================================================================
    def uebernehme_aktuellen_studiengang(
            self,
            studiengang: Studiengang,
            auswahl_zuruecksetzen: bool = True
    ) -> None:
        """Übernimmt einen Studiengang und setzt bei Bedarf Semester- und Kursauswahl zurück."""

        self.zustand.studiengang = studiengang

        if not auswahl_zuruecksetzen:
            return

        self.zustand.aktuelles_semester = None
        self.zustand.aktueller_kurs = None
# ======================================================================================================================================================


# ======================================================================================================================================================
    def studiengang_loeschen(self) -> None:
        """Entfernt den aktuellen Studiengang und dessen Auswahl aus dem Anwendungszustand."""

        if self.zustand.studiengang is None:
            raise ValueError("Bitte zuerst einen Studiengang anlegen oder wechseln.")

        self.zustand.studiengang = None
        self.zustand.aktuelles_semester = None
        self.zustand.aktueller_kurs = None
# ======================================================================================================================================================


# ======================================================================================================================================================
# Klasse SemesterVerwaltung: Ändert ausschließlich Semesterdaten und kennt keine grafische Oberfläche.
class SemesterVerwaltung:
    """Ändert ausschließlich Semesterdaten und kennt keine grafische Oberfläche."""
# ======================================================================================================================================================


# ======================================================================================================================================================
    def __init__(self, zustand: Anwendungszustand) -> None:
        """Erhält nur den von der Oberfläche unabhängigen Anwendungszustand."""

        self.zustand = zustand
# ======================================================================================================================================================


# ======================================================================================================================================================
    def semester_kurs_auswaehlen(self, semester: Semester, kurs: Kurs) -> None:
        """Wählt ein Semester und genau den angegebenen Kurs aus."""

        self.zustand.aktuelles_semester = semester
        self.zustand.aktueller_kurs = kurs
# ======================================================================================================================================================


# ======================================================================================================================================================
    def semester_anlegen(self) -> Semester:
        """Legt automatisch das nächste freie Semester an und gibt es zurück."""

        if self.zustand.studiengang is None:
            raise ValueError("Bitte zuerst einen Studiengang anlegen oder wechseln.")

        nummer = self.zustand.studiengang.naechste_freie_semesternummer()

        if nummer is None:
            raise ValueError(
                "Für diesen Studiengang können keine weiteren Semester angelegt werden."
            )

        semester = Semester(
            nummer = nummer,
            kurse = []
        )

        self.zustand.studiengang.semester.append(semester)
        self.zustand.studiengang.sortiere_semester()
        self.zustand.aktuelles_semester = semester
        self.zustand.aktueller_kurs = None

        return semester
# ======================================================================================================================================================


# ======================================================================================================================================================
    def semester_auswaehlen(self, semester: Semester) -> None:
        """Setzt das Semester als aktuellen Arbeitskontext."""

        self.zustand.aktuelles_semester = semester
        self.zustand.aktueller_kurs = None

        if semester.kurse:
            semester.sortiere_kurse()
            self.zustand.aktueller_kurs = semester.kurse[0]
# ======================================================================================================================================================


# ======================================================================================================================================================
    def semester_loeschen(self, semester: Semester) -> None:
        """Löscht das übergebene Semester und setzt den Arbeitskontext sinnvoll neu."""

        if self.zustand.studiengang is None:
            return

        self.zustand.studiengang.semester.remove(semester)

        if self.zustand.aktuelles_semester is not semester:
            return

        self.zustand.aktuelles_semester = None
        self.zustand.aktueller_kurs = None

        if not self.zustand.studiengang.semester:
            return

        self.zustand.studiengang.sortiere_semester()
        self.zustand.aktuelles_semester = self.zustand.studiengang.semester[0]

        if self.zustand.aktuelles_semester.kurse:
            self.zustand.aktuelles_semester.sortiere_kurse()
            self.zustand.aktueller_kurs = self.zustand.aktuelles_semester.kurse[0]
# ======================================================================================================================================================


# ======================================================================================================================================================
# Klasse KursVerwaltung: Ändert ausschließlich Kursdaten und kennt keine grafische Oberfläche.
class KursVerwaltung:
    """Ändert ausschließlich Kursdaten und kennt keine grafische Oberfläche."""
# ======================================================================================================================================================


# ======================================================================================================================================================
    def __init__(self, zustand: Anwendungszustand) -> None:
        """Erhält nur den von der Oberfläche unabhängigen Anwendungszustand."""

        self.zustand = zustand
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_anlegen(self, name: str, ects: int, anerkannt: bool) -> Kurs:
        """Erstellt einen Kurs aus bereits geprüften Benutzerdaten und fügt ihn hinzu."""

        semester = self.zustand.aktuelles_semester

        if semester is None:
            raise ValueError("Bitte zuerst ein Semester auswählen oder anlegen.")

        if not semester.kann_weiteren_kurs_aufnehmen():
            raise ValueError(
                f"Das Semester hat die maximale Kursanzahl oder {ECTS_PRO_SEMESTER} ECTS erreicht."
            )

        if semester.finde_kurs(name) is not None:
            raise ValueError("In diesem Semester existiert bereits ein Kurs mit diesem Namen.")

        if anerkannt:
            status = KursStatus.ANERKANNT
        else:
            status = KursStatus.NICHT_BEGONNEN

        kurs = Kurs(
            name = name,
            status = status,
            ects = ects,
            note = None
        )

        semester.kurse.append(kurs)
        semester.sortiere_kurse()
        self.zustand.aktueller_kurs = kurs

        return kurs
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_auswaehlen(self, kurs: Kurs) -> None:
        """Setzt den angegebenen Kurs als aktuellen Kurs."""

        self.zustand.aktueller_kurs = kurs
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_bearbeiten(
            self,
            kurs: Kurs,
            neuer_name: str,
            neue_ects: int,
            anerkannt: bool
    ) -> None:
        """Übernimmt bereits erfasste Änderungen in einen bestehenden Kurs."""

        semester = self.zustand.aktuelles_semester

        if semester is None:
            raise ValueError("Es ist kein Semester ausgewählt.")

        vorhandener_kurs = semester.finde_kurs(neuer_name)

        if vorhandener_kurs is not None and vorhandener_kurs is not kurs:
            raise ValueError("In diesem Semester existiert bereits ein Kurs mit diesem Namen.")

        if not semester.kann_kurs_aufnehmen(neue_ects, bisherige_ects = kurs.ects):
            raise ValueError(
                f"Ein Semester darf höchstens {ECTS_PRO_SEMESTER} ECTS enthalten."
            )

        war_anerkannt = kurs.status == KursStatus.ANERKANNT

        kurs.name = neuer_name
        kurs.ects = neue_ects

        if anerkannt:
            kurs.status = KursStatus.ANERKANNT
            kurs.note = None
        elif war_anerkannt:
            kurs.status = KursStatus.NICHT_BEGONNEN
            kurs.note = None

        semester.sortiere_kurse()
        self.zustand.aktueller_kurs = kurs
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_beginnen(self, kurs: Kurs) -> None:
        """Setzt einen noch nicht begonnenen Kurs auf begonnen."""

        kurs.status = KursStatus.BEGONNEN
        kurs.note = None
        self.zustand.aktueller_kurs = kurs
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_stoppen(self, kurs: Kurs) -> None:
        """Setzt einen begonnenen oder abgeschlossenen Kurs vollständig zurück."""

        kurs.status = KursStatus.NICHT_BEGONNEN
        kurs.note = None
        self.zustand.aktueller_kurs = kurs
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_abschliessen(self, kurs: Kurs, note: float) -> None:
        """Schließt den Kurs ausschließlich mit einer zulässigen Kursnote ab."""

        note = float(note)

        if note not in ZULAESSIGE_KURSNOTEN:
            raise ValueError("Die Kursnote ist nicht zulässig.")

        kurs.note = note
        kurs.status = KursStatus.ABGESCHLOSSEN
        self.zustand.aktueller_kurs = kurs
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_loeschen(self, kurs: Kurs) -> None:
        """Löscht den Kurs aus dem aktuell ausgewählten Semester."""

        semester = self.zustand.aktuelles_semester

        if semester is None:
            return

        semester.kurse.remove(kurs)

        if self.zustand.aktueller_kurs is not kurs:
            return

        self.zustand.aktueller_kurs = None

        if semester.kurse:
            semester.sortiere_kurse()
            self.zustand.aktueller_kurs = semester.kurse[0]
# ======================================================================================================================================================
