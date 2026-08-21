# Dieses Modul: Erzeugt die Anwendung und setzt die benötigten Komponenten zur Laufzeit zusammen.
import tkinter as tk
from pathlib import Path
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from anwendungssteuerung import AnwendungsSteuerung
from anwendungsdaten import Anwendungszustand
from dashboard import DashboardDarstellung, FARBE_HINTERGRUND
from dialog_darstellung import DialogDarstellung
from hilfebereich import Hilfebereich
from persistenzverwaltung import PersistenzVerwaltung
from fachverwaltung import KursVerwaltung
from programmverwaltung import ProgrammdatenVerwaltung
from fachverwaltung import SemesterVerwaltung
from fachverwaltung import StudiengangVerwaltung
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
# Klasse StudienDashboard: Stellt das Tkinter-Hauptfenster bereit und verbindet die Anwendungskomponenten.
class StudienDashboard(tk.Tk):
    """Stellt das Tkinter-Hauptfenster bereit und verbindet die Anwendungskomponenten.

    Das Hauptfenster besitzt keine fachliche Verwaltungslogik. Der veränderliche
    Anwendungszustand liegt in Anwendungszustand, Benutzeraktionen werden durch
    AnwendungsSteuerung koordiniert und die sichtbare Oberfläche durch die
    Darstellungsklassen aufgebaut.
    """
# ======================================================================================================================================================


# ======================================================================================================================================================
    def __init__(self) -> None:
        """Erzeugt Zustand, Verwaltung, Steuerung und Darstellung in klar getrennten Schritten."""

        super().__init__()

        self.richte_hauptfenster_ein()

        config_pfad = Path(__file__).parent / "dashboard_config.json"
        self.zustand = Anwendungszustand(config_pfad = config_pfad)

        self.persistenz = PersistenzVerwaltung()
        self.programmdaten = ProgrammdatenVerwaltung(
            self.zustand,
            self.persistenz,
            Path(__file__).parent
        )
        self.studiengang_verwaltung = StudiengangVerwaltung(self.zustand)
        self.semester_verwaltung = SemesterVerwaltung(self.zustand)
        self.kurs_verwaltung = KursVerwaltung(self.zustand)

        self.dialog_darstellung = DialogDarstellung(self)
        self.steuerung = AnwendungsSteuerung(
            self,
            self.zustand,
            self.dialog_darstellung,
            self.programmdaten,
            self.studiengang_verwaltung,
            self.semester_verwaltung,
            self.kurs_verwaltung
        )

        self.steuerung.initialisiere_programmdaten()

        self.hilfebereich = Hilfebereich(self)
        self.dashboard_darstellung = DashboardDarstellung(
            self,
            self.zustand,
            self.steuerung,
            self.hilfebereich
        )
        self.steuerung.setze_darstellung(
            self.dashboard_darstellung,
            self.hilfebereich
        )

        self.dashboard_darstellung.setze_ttk_stile()
        self.dashboard_darstellung.baue_grundgeruest()
        self.dashboard_darstellung.aktualisiere_dashboard()

        self.protocol("WM_DELETE_WINDOW", self.steuerung.beenden)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def richte_hauptfenster_ein(self) -> None:
        """Legt Titel, Startgröße, Mindestgröße und Hintergrund des Fensters fest."""

        self.title("StudienDashboard")
        self.geometry("1500x940")
        self.minsize(1180, 760)
        self.configure(background = FARBE_HINTERGRUND)
# ======================================================================================================================================================


# ======================================================================================================================================================
    @property
    def configuration(self):
        """Stellt der Darstellung die aktuelle Configuration lesbar bereit."""

        return self.zustand.configuration
# ======================================================================================================================================================


# ======================================================================================================================================================
    @property
    def studiengang(self):
        """Stellt der Darstellung den aktuell geladenen Studiengang bereit."""

        return self.zustand.studiengang
# ======================================================================================================================================================


# ======================================================================================================================================================
    @property
    def aktuelles_semester(self):
        """Stellt der Darstellung das aktuell ausgewählte Semester bereit."""

        return self.zustand.aktuelles_semester
# ======================================================================================================================================================


# ======================================================================================================================================================
    @property
    def aktueller_kurs(self):
        """Stellt der Darstellung den aktuell ausgewählten Kurs bereit."""

        return self.zustand.aktueller_kurs
# ======================================================================================================================================================
