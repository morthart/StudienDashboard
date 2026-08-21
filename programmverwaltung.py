from pathlib import Path
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from anwendungsdaten import Anwendungszustand, Configuration
from persistenzverwaltung import PersistenzVerwaltung
from studiengang import Studiengang
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
class ProgrammdatenVerwaltung:
    """Verwaltet technische Programmeinstellungen und den Zugriff auf gespeicherte Studiengänge."""
# ======================================================================================================================================================


# ======================================================================================================================================================
    def __init__(
            self,
            zustand: Anwendungszustand,
            persistenz: PersistenzVerwaltung,
            basisordner: Path
    ) -> None:
        """Verknüpft Programmdaten mit Zustand, Persistenz und dem Ordner der Anwendung."""

        self.zustand = zustand
        self.persistenz = persistenz
        self.basisordner = basisordner
# ======================================================================================================================================================


# ======================================================================================================================================================
    def startordner(self) -> Path:
        """Gibt den Ordner zurück, in dem die Ordnerauswahl standardmäßig starten soll."""

        return self.basisordner
# ======================================================================================================================================================


# ======================================================================================================================================================
    def ermittle_speicherort(self, basisordner: Path | None) -> Path:
        """Ermittelt aus einer Ordnerauswahl den tatsächlich verwendeten Studiengänge-Ordner."""

        if basisordner is None:
            basisordner = self.basisordner

        return basisordner / "Studiengaenge"
# ======================================================================================================================================================


# ======================================================================================================================================================
    def lade_vorhandene_configuration(self) -> Configuration | None:
        """Lädt eine vorhandene Configuration; ungültige Dateien werden wie nicht vorhanden behandelt."""

        return self.persistenz.lade_configuration_sicher(self.zustand.config_pfad)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def erstelle_configuration(self, speicherort: Path) -> Configuration:
        """Erstellt eine neue Configuration und speichert sie sofort."""

        configuration = Configuration(
            eyecatcher = "TresdinsConfig",
            schema_version = 3,
            speicherort = speicherort,
            letzter_studiengang = None
        )

        self.zustand.configuration = configuration
        self.speichere_configuration()
        return configuration
# ======================================================================================================================================================


# ======================================================================================================================================================
    def erstelle_configuration_aus_basisordner(self, basisordner: Path | None) -> Configuration:
        """Erstellt Speicherordner und Configuration aus einer Ordnerauswahl."""

        speicherort = self.ermittle_speicherort(basisordner)
        self.erstelle_ordner_falls_noetig(speicherort)
        return self.erstelle_configuration(speicherort)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def setze_speicherort_aus_basisordner(self, basisordner: Path) -> None:
        """Übernimmt einen neu ausgewählten Basisordner in die vorhandene Configuration."""

        if self.zustand.configuration is None:
            raise ValueError("Die Configuration wurde noch nicht geladen.")

        speicherort = self.ermittle_speicherort(basisordner)
        self.erstelle_ordner_falls_noetig(speicherort)
        self.zustand.configuration.speicherort = speicherort
        self.entferne_ungueltigen_letzten_studiengang(self.zustand.configuration)
        self.speichere_configuration()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def erstelle_ordner_falls_noetig(self, speicherort: Path) -> None:
        """Legt den Speicherordner an, wenn er noch nicht existiert."""

        if self.persistenz.ordner_existiert(speicherort):
            return

        self.persistenz.erstelle_ordner(speicherort)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def stelle_aktuellen_speicherort_wieder_her(self) -> None:
        """Legt den aktuell gespeicherten Studiengänge-Ordner erneut an."""

        if self.zustand.configuration is None:
            raise ValueError("Die Configuration wurde noch nicht geladen.")

        self.erstelle_ordner_falls_noetig(self.zustand.configuration.speicherort)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def speicherort_ist_vorhanden(self, configuration: Configuration | None = None) -> bool:
        """Prüft ausschließlich, ob der eingetragene Speicherordner vorhanden ist."""

        if configuration is None:
            configuration = self.zustand.configuration

        if configuration is None:
            return False

        return self.persistenz.ordner_existiert(configuration.speicherort)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def entferne_ungueltigen_letzten_studiengang(self, configuration: Configuration) -> None:
        """Entfernt einen gespeicherten Studiengangspfad, wenn die Datei nicht mehr existiert."""

        letzter_studiengang = configuration.letzter_studiengang

        if letzter_studiengang is None:
            return

        if self.persistenz.datei_existiert(letzter_studiengang):
            return

        configuration.letzter_studiengang = None
# ======================================================================================================================================================


# ======================================================================================================================================================
    def speichere_configuration(self, configuration: Configuration | None = None) -> None:
        """Speichert die Configuration; Dateifehler werden an den Aufrufer weitergegeben."""

        if configuration is None:
            configuration = self.zustand.configuration

        if configuration is None:
            raise ValueError("Die Configuration wurde noch nicht geladen.")

        self.persistenz.speichere_configuration(configuration, self.zustand.config_pfad)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def lade_letzten_studiengang(self) -> Studiengang | None:
        """Lädt den zuletzt verwendeten Studiengang, sofern dessen Datei noch vorhanden ist."""

        configuration = self.zustand.configuration

        if configuration is None:
            return None

        dateipfad = configuration.letzter_studiengang

        if not self.persistenz.datei_existiert(dateipfad):
            configuration.letzter_studiengang = None
            return None

        studiengang = self.persistenz.lade_studiengang_sicher(dateipfad)

        if studiengang is None:
            configuration.letzter_studiengang = None

        return studiengang
# ======================================================================================================================================================


# ======================================================================================================================================================
    def finde_studiengaenge(self) -> list[str]:
        """Liest die Namen aller gültigen Studiengänge aus dem eingestellten Speicherordner."""

        if self.zustand.configuration is None:
            return []

        namen = []
        dateipfade = self.persistenz.finde_json_dateien(self.zustand.configuration.speicherort)

        for dateipfad in dateipfade:
            studiengang = self.persistenz.lade_studiengang_sicher(dateipfad)

            if studiengang is None:
                continue

            namen.append(studiengang.name)

        namen.sort(key = str.lower)
        return namen
# ======================================================================================================================================================


# ======================================================================================================================================================
    def studiengang_existiert(self, name: str) -> bool:
        """Prüft anhand des erzeugten Dateinamens, ob ein Studiengang bereits gespeichert ist."""

        if self.zustand.configuration is None:
            raise ValueError("Die Configuration wurde noch nicht geladen.")

        dateipfad = self.persistenz.studiengang_dateipfad(
            self.zustand.configuration.speicherort,
            name
        )
        return self.persistenz.datei_existiert(dateipfad)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def neuer_studiengangsname_ist_belegt(self, name: str) -> bool:
        """Prüft bei einer Umbenennung, ob der neue Dateiname bereits anderweitig verwendet wird."""

        if self.zustand.configuration is None:
            raise ValueError("Die Configuration wurde noch nicht geladen.")

        neuer_dateipfad = self.persistenz.studiengang_dateipfad(
            self.zustand.configuration.speicherort,
            name
        )
        alter_dateipfad = self.zustand.configuration.letzter_studiengang

        if neuer_dateipfad == alter_dateipfad:
            return False

        return self.persistenz.datei_existiert(neuer_dateipfad)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def lade_studiengang(self, name: str) -> Studiengang:
        """Lädt einen Studiengang anhand seines Namens und merkt dessen Datei in der Configuration."""

        if self.zustand.configuration is None:
            raise ValueError("Die Configuration wurde noch nicht geladen.")

        dateipfad = self.persistenz.studiengang_dateipfad(
            self.zustand.configuration.speicherort,
            name
        )
        studiengang = self.persistenz.lade_studiengang(dateipfad)
        self.zustand.configuration.letzter_studiengang = dateipfad
        self.speichere_configuration()
        return studiengang
# ======================================================================================================================================================


# ======================================================================================================================================================
    def speichere_neuen_studiengang(self, studiengang: Studiengang, ueberschreiben: bool = False) -> None:
        """Speichert einen neuen Studiengang und merkt dessen Datei in der Configuration."""

        if self.zustand.configuration is None:
            raise ValueError("Die Configuration wurde noch nicht geladen.")

        dateipfad = self.persistenz.studiengang_dateipfad(
            self.zustand.configuration.speicherort,
            studiengang.name
        )

        if self.persistenz.datei_existiert(dateipfad) and not ueberschreiben:
            raise FileExistsError("Unter diesem Namen existiert bereits ein Studiengang.")

        self.persistenz.speichere_studiengang(studiengang, dateipfad)
        self.zustand.configuration.letzter_studiengang = dateipfad
        self.speichere_configuration()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def speichere_bearbeiteten_studiengang(
            self,
            studiengang: Studiengang,
            ueberschreiben: bool = False
    ) -> None:
        """Speichert einen bearbeiteten Studiengang und entfernt bei Umbenennung die alte Datei."""

        if self.zustand.configuration is None:
            raise ValueError("Die Configuration wurde noch nicht geladen.")

        alter_dateipfad = self.zustand.configuration.letzter_studiengang
        neuer_dateipfad = self.persistenz.studiengang_dateipfad(
            self.zustand.configuration.speicherort,
            studiengang.name
        )

        if (
                neuer_dateipfad != alter_dateipfad
                and self.persistenz.datei_existiert(neuer_dateipfad)
                and not ueberschreiben
        ):
            raise FileExistsError("Unter dem neuen Namen existiert bereits ein Studiengang.")

        self.persistenz.speichere_studiengang(studiengang, neuer_dateipfad)

        if alter_dateipfad is not None and alter_dateipfad != neuer_dateipfad:
            self.persistenz.loesche_datei(alter_dateipfad)

        self.zustand.configuration.letzter_studiengang = neuer_dateipfad
        self.speichere_configuration()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def loesche_aktuellen_studiengang(self) -> None:
        """Löscht die aktuell gemerkte Studiengangsdatei und aktualisiert die Configuration."""

        if self.zustand.configuration is None:
            raise ValueError("Die Configuration wurde noch nicht geladen.")

        self.persistenz.loesche_datei(self.zustand.configuration.letzter_studiengang)
        self.zustand.configuration.letzter_studiengang = None
        self.speichere_configuration()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def waehle_ersten_kontext(self) -> None:
        """Wählt nach dem Laden das erste Semester und den ersten Kurs aus."""

        self.zustand.aktuelles_semester = None
        self.zustand.aktueller_kurs = None

        if self.zustand.studiengang is None:
            return

        if not self.zustand.studiengang.semester:
            return

        self.zustand.studiengang.sortiere_semester()
        self.zustand.aktuelles_semester = self.zustand.studiengang.semester[0]

        if not self.zustand.aktuelles_semester.kurse:
            return

        self.zustand.aktuelles_semester.sortiere_kurse()
        self.zustand.aktueller_kurs = self.zustand.aktuelles_semester.kurse[0]
# ======================================================================================================================================================


# ======================================================================================================================================================
    def speichern(self) -> None:
        """Speichert aktuellen Studiengang und Configuration."""

        if self.zustand.configuration is None:
            return

        if self.zustand.studiengang is not None:
            dateipfad = self.zustand.configuration.letzter_studiengang

            if dateipfad is None:
                dateipfad = self.persistenz.studiengang_dateipfad(
                    self.zustand.configuration.speicherort,
                    self.zustand.studiengang.name
                )
                self.zustand.configuration.letzter_studiengang = dateipfad

            self.persistenz.speichere_studiengang(self.zustand.studiengang, dateipfad)

        self.speichere_configuration()
# ======================================================================================================================================================
