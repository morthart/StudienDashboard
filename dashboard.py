# Dieses Modul: Bündelt die sichtbaren Dashboard-Bereiche und stößt deren Aktualisierung an.
"""Koordiniert die Darstellung des Dashboards über klar getrennte Komponenten."""

import tkinter as tk
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from dashboard_elemente import DashboardElemente
from konstanten import (
    FARBE_BLAU,
    FARBE_GELB,
    FARBE_GRAU,
    FARBE_GRUEN,
    FARBE_ROT,
    FARBE_HELLBLAU,
    FARBE_HINTERGRUND,
    FARBE_KARTE,
    FARBE_PROGRESS_HINTERGRUND,
    FARBE_RAND,
    FARBE_TEXT,
    FARBE_TEXT_GRAU
)
from dashboard_grundgeruest import DashboardGrundgeruest
from dashboard_kopf import DashboardKopfbereich
from kursdarstellung import KursDarstellung
from semesterdarstellung import SemesterDarstellung
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
# Klasse DashboardDarstellung: Besitzt die spezialisierten Darstellungsbereiche und koordiniert deren Aufbau.
class DashboardDarstellung:
    """Besitzt die spezialisierten Darstellungsbereiche und koordiniert deren Aufbau.

    Die Klasse verwendet Komposition statt Vererbung. Grundgerüst, Kopfbereich,
    Semesterdarstellung und Kursdarstellung bleiben dadurch eigenständige Komponenten.
    """
# ======================================================================================================================================================


# ======================================================================================================================================================
    def __init__(
            self,
            anwendung,
            zustand,
            steuerung,
            hilfebereich
    ) -> None:
        """Erzeugt alle Komponenten, die ausschließlich für die Darstellung zuständig sind."""

        self.anwendung = anwendung
        self.zustand = zustand
        self.elemente = DashboardElemente()

        self.grundgeruest = DashboardGrundgeruest(
            anwendung,
            steuerung,
            hilfebereich
        )
        self.kopfbereich = DashboardKopfbereich(anwendung, self.elemente)
        self.semesterbereich = SemesterDarstellung(
            anwendung,
            self.elemente,
            steuerung
        )
        self.kursbereich = KursDarstellung(
            anwendung,
            self.elemente,
            steuerung
        )
# ======================================================================================================================================================


# ======================================================================================================================================================
    def setze_ttk_stile(self) -> None:
        """Delegiert die Einrichtung der Tkinter-Stile an das Grundgerüst."""

        self.grundgeruest.setze_ttk_stile()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_grundgeruest(self) -> None:
        """Lässt das Grundgerüst des Hauptfensters erstellen."""

        self.grundgeruest.baue_grundgeruest()
# ======================================================================================================================================================


# ======================================================================================================================================================
    def aktualisiere_dashboard(self) -> None:
        """Baut die sichtbaren Dashboardbereiche aus dem aktuellen Anwendungszustand neu auf."""

        canvas = self.grundgeruest.canvas
        dashboard = self.grundgeruest.dashboard
        kopfbereich = self.grundgeruest.kopfbereich
        dashboard_fenster = self.grundgeruest.dashboard_fenster

        if canvas is None or dashboard is None or kopfbereich is None:
            return

        aktuelle_scrollposition = canvas.yview()
        canvas.itemconfigure(dashboard_fenster, state = "hidden")

        self.grundgeruest.entferne_alle_widgets(kopfbereich)
        self.grundgeruest.entferne_alle_widgets(dashboard)

        self.kopfbereich.baue_kopfbereich(kopfbereich)
        self.semesterbereich.baue_semesterbereich(dashboard)
        self.baue_unteren_bereich(dashboard)

        self.anwendung.update_idletasks()
        canvas.configure(scrollregion = canvas.bbox("all"))
        canvas.itemconfigure(dashboard_fenster, state = "normal")

        if aktuelle_scrollposition:
            canvas.yview_moveto(aktuelle_scrollposition[0])
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_unteren_bereich(self, parent: tk.Misc) -> None:
        """Erstellt die Kursübersicht für das aktuell ausgewählte Semester."""

        unterer_bereich = tk.Frame(parent, background = FARBE_HINTERGRUND)
        unterer_bereich.pack(fill = "both", expand = True, padx = 20, pady = (4, 20))

        kursbereich = self.elemente.erstelle_abschnitt(
            unterer_bereich,
            "Kursübersicht"
        )
        kursbereich.pack(fill = "both", expand = True)

        self.kursbereich.baue_kurskarten(kursbereich)
# ======================================================================================================================================================
