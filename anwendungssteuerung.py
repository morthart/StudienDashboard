from anwendungsdaten import Anwendungszustand
from dialog_darstellung import DialogDarstellung
from enums import KursStatus
from konstanten import ECTS_PRO_SEMESTER
from kurs import Kurs
from fachverwaltung import KursVerwaltung
from programmverwaltung import ProgrammdatenVerwaltung
from semester import Semester
from fachverwaltung import SemesterVerwaltung
from fachverwaltung import StudiengangVerwaltung
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
class AnwendungsSteuerung:
    """Verbindet Benutzeraktionen, Verwaltung, Darstellung und Speichern.

    Die Klasse übernimmt die Controller-Aufgabe. Sie wertet Benutzereingaben aus,
    ruft die passenden Verwaltungsmethoden auf und veranlasst anschließend Speichern
    und Aktualisieren der Oberfläche. Die Verwaltungsklassen selbst kennen keine GUI.
    """
# ======================================================================================================================================================


# ======================================================================================================================================================
    def __init__(
            self,
            anwendung,
            zustand: Anwendungszustand,
            dialoge: DialogDarstellung,
            programmdaten: ProgrammdatenVerwaltung,
            studiengang_verwaltung: StudiengangVerwaltung,
            semester_verwaltung: SemesterVerwaltung,
            kurs_verwaltung: KursVerwaltung
    ) -> None:
        """Übernimmt alle Komponenten, die für die Steuerung benötigt werden."""

        self.anwendung = anwendung
        self.zustand = zustand
        self.dialoge = dialoge
        self.programmdaten = programmdaten
        self.studiengang_verwaltung = studiengang_verwaltung
        self.semester_verwaltung = semester_verwaltung
        self.kurs_verwaltung = kurs_verwaltung
        self.dashboard_darstellung = None
        self.hilfebereich = None
# ======================================================================================================================================================


# ======================================================================================================================================================
    def setze_darstellung(self, dashboard_darstellung, hilfebereich) -> None:
        """Verknüpft die Steuerung nach deren Erzeugung mit den sichtbaren Bereichen."""

        self.dashboard_darstellung = dashboard_darstellung
        self.hilfebereich = hilfebereich
# ======================================================================================================================================================


# ======================================================================================================================================================
    def initialisiere_programmdaten(self) -> None:
        """Lädt die Configuration oder führt die Erstkonfiguration durch."""

        configuration = self.programmdaten.lade_vorhandene_configuration()

        if configuration is None:
            self.dialoge.zeige_info(
                "Erster Programmstart",
                (
                    "Halli hallo :)\n\n"
                    "Das hier scheint der erste Programmstart zu sein.\n"
                    "Du wirst daher gleich gefragt, in welchem Ordner du die "
                    "Studiengänge ablegen möchtest."
                )
            )
            configuration = self.erstelle_erste_configuration()
        else:
            self.zustand.configuration = configuration

            if not self.pruefe_speicherort():
                configuration = self.erstelle_erste_configuration()

        self.zustand.configuration = configuration
        self.zustand.studiengang = self.programmdaten.lade_letzten_studiengang()
        self.programmdaten.waehle_ersten_kontext()

        try:
            self.programmdaten.speichere_configuration()
        except OSError:
            pass
# ======================================================================================================================================================


# ======================================================================================================================================================
    def erstelle_erste_configuration(self):
        """Erfragt den ersten Speicherort und erstellt die dazugehörige Configuration."""

        basisordner = self.dialoge.speicherort_auswaehlen(
            "Speicherordner für Studiengänge wählen",
            self.programmdaten.startordner()
        )

        try:
            return self.programmdaten.erstelle_configuration_aus_basisordner(basisordner)
        except OSError as fehler:
            self.dialoge.zeige_fehler(
                "Speicherordner konnte nicht angelegt werden",
                str(fehler)
            )

            return self.programmdaten.erstelle_configuration_aus_basisordner(None)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def pruefe_speicherort(self) -> bool:
        """Stellt einen fehlenden Speicherordner gemeinsam mit dem Benutzer wieder her."""

        configuration = self.zustand.configuration

        if configuration is None:
            return False

        if self.programmdaten.speicherort_ist_vorhanden(configuration):
            return True

        auswahl = self.dialoge.frage_ja_nein_abbrechen(
            "Speicherordner nicht gefunden",
            (
                "Der gespeicherte Ordner für Studiengänge wurde nicht gefunden:\n\n"
                f"{configuration.speicherort}\n\n"
                "Ja: Ordner am bisherigen Speicherort neu anlegen\n"
                "Nein: Anderen Speicherort auswählen\n"
                "Abbrechen: Vorgang abbrechen"
            )
        )

        if auswahl is None:
            return False

        try:
            if auswahl:
                self.programmdaten.stelle_aktuellen_speicherort_wieder_her()
            else:
                basisordner = self.dialoge.speicherort_auswaehlen(
                    "Neuen Speicherordner für Studiengänge wählen",
                    self.programmdaten.startordner()
                )

                if basisordner is None:
                    return False

                self.programmdaten.setze_speicherort_aus_basisordner(basisordner)
        except OSError as fehler:
            self.dialoge.zeige_fehler(
                "Speicherordner konnte nicht angelegt werden",
                str(fehler)
            )
            return False

        self.programmdaten.entferne_ungueltigen_letzten_studiengang(configuration)

        try:
            self.programmdaten.speichere_configuration(configuration)
        except OSError as fehler:
            self.dialoge.zeige_fehler(
                "Configuration konnte nicht gespeichert werden",
                str(fehler)
            )
            return False

        return True
# ======================================================================================================================================================


# ======================================================================================================================================================
    def speichern_und_aktualisieren(self) -> None:
        """Speichert den aktuellen Zustand und zeichnet danach das Dashboard neu."""

        try:
            self.programmdaten.speichern()
        except OSError as fehler:
            self.dialoge.zeige_fehler("Daten konnten nicht gespeichert werden", str(fehler))

        self.aktualisiere_dashboard()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def aktualisiere_dashboard(self) -> None:
        """Aktualisiert die Darstellung, sofern sie bereits erzeugt wurde."""

        if self.dashboard_darstellung is not None:
            self.dashboard_darstellung.aktualisiere_dashboard()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def studiengang_anlegen(self) -> None:
        """Steuert Dialog, Prüfung, Speicherung und Übernahme eines neuen Studiengangs."""

        if not self.pruefe_speicherort():
            return

        daten = self.dialoge.studiengangsdaten_eingeben("Studiengang anlegen")

        if daten is None:
            return

        name, wunschnote, gesamt_ects = daten
        ueberschreiben = False

        try:
            if self.programmdaten.studiengang_existiert(name):
                ueberschreiben = self.dialoge.frage_ja_nein(
                    "Studiengang existiert bereits",
                    "Unter diesem Namen existiert bereits ein Studiengang. Soll er überschrieben werden?"
                )

                if not ueberschreiben:
                    return

            studiengang = self.studiengang_verwaltung.erstelle_studiengang(
                name,
                wunschnote,
                gesamt_ects
            )
            self.programmdaten.speichere_neuen_studiengang(
                studiengang,
                ueberschreiben = ueberschreiben
            )
            self.studiengang_verwaltung.uebernehme_aktuellen_studiengang(studiengang)
        except (OSError, ValueError, FileExistsError) as fehler:
            self.dialoge.zeige_fehler("Studiengang konnte nicht angelegt werden", str(fehler))
            return

        self.programmdaten.waehle_ersten_kontext()
        self.speichern_und_aktualisieren()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def studiengang_wechseln(self) -> None:
        """Zeigt die Studiengangsauswahl und wechselt zum gewählten Eintrag."""

        self.studiengang_auswahl_anzeigen("Studiengang wechseln")
# ======================================================================================================================================================


# ======================================================================================================================================================
    def studiengang_auswahl_anzeigen(self, titel: str) -> None:
        """Zeigt vorhandene Studiengänge sowie den Eintrag zum Neuanlegen."""

        if not self.pruefe_speicherort():
            return

        studiengaenge = self.programmdaten.finde_studiengaenge()
        anzeigenamen = list(studiengaenge)
        anzeigenamen.append("< Neuen Studiengang anlegen >")

        auswahl = self.dialoge.auswahl_treffen(
            titel,
            "Studiengang auswählen:",
            anzeigenamen
        )

        if auswahl is None:
            return

        if auswahl == len(studiengaenge):
            self.studiengang_anlegen()
            return

        name = studiengaenge[auswahl]

        try:
            studiengang = self.programmdaten.lade_studiengang(name)
            self.studiengang_verwaltung.uebernehme_aktuellen_studiengang(studiengang)
        except (OSError, ValueError, KeyError, TypeError) as fehler:
            self.dialoge.zeige_fehler("Studiengang konnte nicht geladen werden", str(fehler))
            return

        self.programmdaten.waehle_ersten_kontext()
        self.speichern_und_aktualisieren()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def studiengang_bearbeiten(self) -> None:
        """Erfasst neue Studiengangsdaten und koordiniert Fachlogik und Speicherung."""

        if not self.pruefe_speicherort():
            return

        studiengang = self.zustand.studiengang

        if studiengang is None:
            self.dialoge.zeige_info(
                "Kein Studiengang",
                "Bitte zuerst einen Studiengang anlegen oder wechseln."
            )
            return

        daten = self.dialoge.studiengangsdaten_eingeben(
            "Studiengang bearbeiten",
            start_name = studiengang.name,
            start_wunschnote = studiengang.wunschnote,
            start_gesamt_ects = studiengang.gesamt_ects,
            min_gesamt_ects = studiengang.berechne_min_gesamt_ects()
        )

        if daten is None:
            return

        name, wunschnote, gesamt_ects = daten
        ueberschreiben = False

        try:
            if self.programmdaten.neuer_studiengangsname_ist_belegt(name):
                ueberschreiben = self.dialoge.frage_ja_nein(
                    "Studiengang existiert bereits",
                    "Unter dem neuen Namen existiert bereits ein Studiengang. Soll er überschrieben werden?"
                )

                if not ueberschreiben:
                    return

            bearbeiteter_studiengang = self.studiengang_verwaltung.erstelle_bearbeiteten_studiengang(
                name,
                wunschnote,
                gesamt_ects
            )
            self.programmdaten.speichere_bearbeiteten_studiengang(
                bearbeiteter_studiengang,
                ueberschreiben = ueberschreiben
            )
            self.studiengang_verwaltung.uebernehme_aktuellen_studiengang(
                bearbeiteter_studiengang,
                auswahl_zuruecksetzen = False
            )
        except (OSError, ValueError, FileExistsError) as fehler:
            self.dialoge.zeige_fehler("Studiengang konnte nicht bearbeitet werden", str(fehler))
            return

        self.speichern_und_aktualisieren()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def studiengang_loeschen(self) -> None:
        """Fragt nach einer Bestätigung und löscht anschließend Studiengang und gespeicherte Datei."""

        if not self.pruefe_speicherort():
            return

        if self.zustand.studiengang is None:
            self.dialoge.zeige_info(
                "Kein Studiengang",
                "Bitte zuerst einen Studiengang anlegen oder wechseln."
            )
            return

        bestaetigung = self.dialoge.frage_ja_nein(
            "Studiengang löschen",
            f"Soll der Studiengang '{self.zustand.studiengang.name}' endgültig gelöscht werden?"
        )

        if not bestaetigung:
            return

        try:
            self.programmdaten.loesche_aktuellen_studiengang()
            self.studiengang_verwaltung.studiengang_loeschen()
        except (OSError, ValueError) as fehler:
            self.dialoge.zeige_fehler("Studiengang konnte nicht gelöscht werden", str(fehler))
            return

        self.aktualisiere_dashboard()
        self.studiengang_auswahl_anzeigen("Studiengang auswählen")
# ======================================================================================================================================================


# ======================================================================================================================================================
    def semester_anlegen(self) -> None:
        """Legt ein Semester an und behandelt mögliche fachliche Fehler in der Darstellung."""

        try:
            self.semester_verwaltung.semester_anlegen()
        except ValueError as fehler:
            self.dialoge.zeige_info("Semester kann nicht angelegt werden", str(fehler))
            return

        self.speichern_und_aktualisieren()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def semester_auswaehlen(self, semester: Semester) -> None:
        """Wählt ein Semester und aktualisiert die sichtbaren Bereiche."""

        self.semester_verwaltung.semester_auswaehlen(semester)
        self.aktualisiere_dashboard()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def semester_loeschen(self, semester: Semester) -> None:
        """Fragt nach der Löschbestätigung und übergibt danach an die Semesterverwaltung."""

        bestaetigung = self.dialoge.frage_ja_nein(
            "Semester löschen",
            (
                f"Soll Semester {semester.nummer} einschließlich aller enthaltenen "
                "Kurse endgültig gelöscht werden?"
            )
        )

        if not bestaetigung:
            return

        self.semester_verwaltung.semester_loeschen(semester)
        self.speichern_und_aktualisieren()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_anlegen(self) -> None:
        """Erfasst Kursdaten und lässt die Kursverwaltung den Kurs anlegen."""

        semester = self.zustand.aktuelles_semester

        if semester is None:
            self.dialoge.zeige_info(
                "Kein Semester",
                "Bitte zuerst ein Semester auswählen oder anlegen."
            )
            return

        if not semester.kann_weiteren_kurs_aufnehmen():
            self.dialoge.zeige_info(
                "Kein weiterer Kurs möglich",
                f"Das Semester hat die maximale Kursanzahl oder {ECTS_PRO_SEMESTER} ECTS erreicht."
            )
            return

        kursdaten = self.dialoge.kursdaten_eingeben(
            "Kurs anlegen",
            semester.berechne_freie_ects()
        )

        if kursdaten is None:
            return

        name, ects, anerkannt = kursdaten

        try:
            self.kurs_verwaltung.kurs_anlegen(name, ects, anerkannt)
        except ValueError as fehler:
            self.dialoge.zeige_fehler("Kurs konnte nicht angelegt werden", str(fehler))
            return

        self.speichern_und_aktualisieren()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_auswaehlen(self, kurs: Kurs) -> None:
        """Wählt einen Kurs und aktualisiert anschließend die Darstellung."""

        self.kurs_verwaltung.kurs_auswaehlen(kurs)
        self.aktualisiere_dashboard()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_bearbeiten(self, kurs: Kurs) -> None:
        """Erfasst neue Kursdaten und übergibt die Änderung an die Kursverwaltung."""

        semester = self.zustand.aktuelles_semester

        if semester is None:
            return

        maximaler_wert = semester.berechne_freie_ects() + kurs.ects
        kursdaten = self.dialoge.kursdaten_eingeben(
            "Kurs bearbeiten",
            maximaler_wert,
            start_name = kurs.name,
            start_ects = kurs.ects,
            start_anerkannt = kurs.status == KursStatus.ANERKANNT
        )

        if kursdaten is None:
            return

        name, ects, anerkannt = kursdaten

        try:
            self.kurs_verwaltung.kurs_bearbeiten(kurs, name, ects, anerkannt)
        except ValueError as fehler:
            self.dialoge.zeige_fehler("Kurs konnte nicht bearbeitet werden", str(fehler))
            return

        self.speichern_und_aktualisieren()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_beginnen(self, kurs: Kurs) -> None:
        """Startet einen Kurs und speichert die Änderung."""

        self.kurs_verwaltung.kurs_beginnen(kurs)
        self.speichern_und_aktualisieren()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_stoppen(self, kurs: Kurs) -> None:
        """Setzt einen Kurs zurück und speichert die Änderung."""

        self.kurs_verwaltung.kurs_stoppen(kurs)
        self.speichern_und_aktualisieren()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_abschliessen(self, kurs: Kurs) -> None:
        """Erfasst die Note und schließt den Kurs über die Verwaltung ab."""

        if kurs.note is None:
            startwert = ""
        else:
            startwert = str(kurs.note)

        note = self.dialoge.note_eingeben(
            "Kurs abschließen",
            "Erreichte Note:",
            startwert
        )

        if note is None:
            return

        self.kurs_verwaltung.kurs_abschliessen(kurs, note)
        self.speichern_und_aktualisieren()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_loeschen(self, kurs: Kurs) -> None:
        """Fragt nach der Löschbestätigung und löscht danach den Kurs."""

        bestaetigung = self.dialoge.frage_ja_nein(
            "Kurs löschen",
            f"Soll der Kurs '{kurs.name}' endgültig gelöscht werden?"
        )

        if not bestaetigung:
            return

        self.kurs_verwaltung.kurs_loeschen(kurs)
        self.speichern_und_aktualisieren()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def hilfe_anzeigen(self) -> None:
        """Leitet die Hilfeaktion an die Hilfedarstellung weiter."""

        if self.hilfebereich is not None:
            self.hilfebereich.hilfe_anzeigen()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def beenden(self) -> None:
        """Speichert nach Möglichkeit und beendet anschließend das Hauptfenster."""

        try:
            self.programmdaten.speichern()
        except OSError as fehler:
            self.dialoge.zeige_fehler("Daten konnten nicht gespeichert werden", str(fehler))
            return

        self.anwendung.destroy()
# ======================================================================================================================================================
