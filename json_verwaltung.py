import json
from pathlib import Path
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from anwendungsdaten import Configuration
from enums import KursStatus
from kurs import Kurs
from semester import Semester
from studiengang import Studiengang
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
class JsonDatenhaltung:
    """Kapselt das JSON-Format und trennt die Fachklassen von der Speicherung.

    Studiengang, Semester und Kurs kennen dadurch nur noch ihre fachlichen Daten.
    Die Umwandlung in Dictionaries und zurück findet vollständig in dieser Klasse statt.
    """
# ======================================================================================================================================================


# ======================================================================================================================================================
    def speichere_studiengang(self, studiengang: Studiengang, dateipfad: Path) -> None:
        """Speichert einen vollständigen Studiengang in einer JSON-Datei."""

        daten = {
            "eyecatcher": "TresdinsDashboard",
            "schema_version": 3,
            "studiengang": self.studiengang_zu_dict(studiengang)
        }

        with dateipfad.open("w", encoding = "utf-8") as datei:
            json.dump(daten, datei, ensure_ascii = False, indent = 4)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def lade_studiengang(self, dateipfad: Path) -> Studiengang:
        """Lädt einen vollständigen Studiengang aus einer JSON-Datei."""

        with dateipfad.open("r", encoding = "utf-8") as datei:
            daten = json.load(datei)

        if not isinstance(daten, dict):
            raise ValueError("Die Studiengangsdatei enthält kein Dictionary.")

        eyecatcher = daten.get("eyecatcher")

        if eyecatcher not in {"TresdinsDashboard", "DashboardFM"}:
            raise ValueError("Die Studiengangsdatei gehört nicht zum StudienDashboard.")

        if "studiengang" not in daten:
            raise KeyError("Der Studiengangseintrag fehlt in der JSON-Datei.")

        return self.studiengang_aus_dict(daten["studiengang"])
# ======================================================================================================================================================


# ======================================================================================================================================================
    def speichere_configuration(self, configuration: Configuration, dateipfad: Path) -> None:
        """Speichert die technischen Programmeinstellungen als JSON."""

        daten = {
            "eyecatcher": configuration.eyecatcher,
            "schema_version": configuration.schema_version,
            "speicherort": str(configuration.speicherort),
            "letzter_studiengang": (
                str(configuration.letzter_studiengang)
                if configuration.letzter_studiengang is not None
                else None
            )
        }

        with dateipfad.open("w", encoding = "utf-8") as datei:
            json.dump(daten, datei, ensure_ascii = False, indent = 4)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def lade_configuration(self, dateipfad: Path) -> Configuration:
        """Lädt die technischen Programmeinstellungen aus einer JSON-Datei."""

        with dateipfad.open("r", encoding = "utf-8") as datei:
            daten = json.load(datei)

        if not isinstance(daten, dict):
            raise ValueError("Die Config-Datei enthält kein Dictionary.")

        letzter_studiengang = daten.get("letzter_studiengang")

        if letzter_studiengang is not None:
            letzter_studiengang = Path(letzter_studiengang)

        return Configuration(
            eyecatcher = str(daten.get("eyecatcher", "TresdinsConfig")),
            schema_version = int(daten.get("schema_version", 1)),
            speicherort = Path(daten["speicherort"]),
            letzter_studiengang = letzter_studiengang
        )
# ======================================================================================================================================================


# ======================================================================================================================================================
    def studiengang_zu_dict(self, studiengang: Studiengang) -> dict:
        """Überführt einen Studiengang einschließlich Semester in JSON-kompatible Daten."""

        semester_daten = []

        for semester in studiengang.semester:
            semester_daten.append(self.semester_zu_dict(semester))

        return {
            "name": studiengang.name,
            "wunschnote": studiengang.wunschnote,
            "gesamt_ects": studiengang.gesamt_ects,
            "semester": semester_daten
        }
# ======================================================================================================================================================


# ======================================================================================================================================================
    def studiengang_aus_dict(self, daten: dict) -> Studiengang:
        """Erzeugt einen Studiengang einschließlich Semester aus gespeicherten Daten."""

        semester_liste = []

        for semester_daten in daten.get("semester", []):
            semester_liste.append(self.semester_aus_dict(semester_daten))

        studiengang = Studiengang(
            name = str(daten["name"]),
            wunschnote = round(float(daten["wunschnote"]), 1),
            gesamt_ects = int(daten["gesamt_ects"]),
            semester = semester_liste
        )

        studiengang.sortiere_semester()
        return studiengang
# ======================================================================================================================================================


# ======================================================================================================================================================
    def semester_zu_dict(self, semester: Semester) -> dict:
        """Überführt ein Semester einschließlich Kurse in JSON-kompatible Daten."""

        kurs_daten = []

        for kurs in semester.kurse:
            kurs_daten.append(self.kurs_zu_dict(kurs))

        return {
            "nummer": semester.nummer,
            "kurse": kurs_daten
        }
# ======================================================================================================================================================


# ======================================================================================================================================================
    def semester_aus_dict(self, daten: dict) -> Semester:
        """Erzeugt ein Semester einschließlich Kurse aus gespeicherten Daten."""

        kurse = []

        for kurs_daten in daten.get("kurse", []):
            kurse.append(self.kurs_aus_dict(kurs_daten))

        semester = Semester(
            nummer = int(daten["nummer"]),
            kurse = kurse
        )
        semester.sortiere_kurse()
        return semester
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_zu_dict(self, kurs: Kurs) -> dict:
        """Überführt einen Kurs in JSON-kompatible Daten."""

        return {
            "name": kurs.name,
            "status": kurs.status.value,
            "ects": kurs.ects,
            "note": kurs.note
        }
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_aus_dict(self, daten: dict) -> Kurs:
        """Erzeugt einen Kurs aus gespeicherten Daten."""

        return Kurs(
            name = str(daten["name"]),
            status = KursStatus(daten["status"]),
            ects = int(daten["ects"]),
            note = daten.get("note")
        )
# ======================================================================================================================================================
