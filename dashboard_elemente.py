# Dieses Modul: Enthält wiederverwendbare Hilfsfunktionen und GUI-Elemente des Dashboards.
import tkinter as tk
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from konstanten import (
    FARBE_HINTERGRUND,
    FARBE_KARTE,
    FARBE_RAND,
    FARBE_TEXT,
    FARBE_GRAU,
    FARBE_GELB,
    FARBE_GRUEN,
    FARBE_BLAU,
    FARBE_ROT,
    FARBE_HELLBLAU
)
from enums import KursStatus, SemesterStatus
from kurs import Kurs
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
# Klasse DashboardElemente: Enthält wiederverwendbare Karten, Buttons und Statusdarstellungen.
class DashboardElemente:
    """Enthält wiederverwendbare Karten, Buttons und Statusdarstellungen."""

# ======================================================================================================================================================


# ======================================================================================================================================================
    def erstelle_symbol_button(
            self,
            parent: tk.Misc,
            symbol: str,
            hilfetext: str,
            befehl
    ) -> tk.Button:
        """Erstellt einen kleinen Symbolbutton und hinterlegt den Hilfetext als Widgetname."""

        button = tk.Button(
            parent,
            text = symbol,
            font = ("Segoe UI Symbol", 10, "bold"),
            foreground = FARBE_TEXT,
            background = FARBE_KARTE,
            activebackground = FARBE_HELLBLAU,
            activeforeground = FARBE_TEXT,
            borderwidth = 0,
            cursor = "hand2",
            padx = 5,
            pady = 1,
            command = befehl,
            takefocus = True
        )

        # Der Hilfetext ist für die Tastatur- und Codeorientierung hinterlegt. Tkinter
        # besitzt standardmäßig keine Tooltips; der Button bleibt trotzdem selbsterklärend.
        button.hilfetext = hilfetext

        return button
# ======================================================================================================================================================


# ======================================================================================================================================================
    def erstelle_abschnitt(self, parent: tk.Misc, titel: str) -> tk.Frame:
        """Erstellt einen weißen Dashboardabschnitt mit Überschrift."""

        rahmen = tk.Frame(
            parent,
            background = FARBE_KARTE,
            highlightbackground = FARBE_RAND,
            highlightthickness = 1
        )

        titel_label = tk.Label(
            rahmen,
            text = titel,
            font = ("Arial", 12, "bold"),
            foreground = FARBE_TEXT,
            background = FARBE_KARTE
        )
        titel_label.pack(anchor = "w", padx = 16, pady = (14, 8))

        return rahmen
# ======================================================================================================================================================


# ======================================================================================================================================================
    def erstelle_karte(self, parent: tk.Misc, breite: int, hoehe: int) -> tk.Frame:
        """Erstellt eine einheitliche weiße Karte mit Rand."""

        return tk.Frame(
            parent,
            background = FARBE_KARTE,
            highlightbackground = FARBE_RAND,
            highlightthickness = 1,
            width = breite,
            height = hoehe
        )
# ======================================================================================================================================================


# ======================================================================================================================================================
    def mache_widget_klickbar(self, widget: tk.Misc, befehl) -> None:
        """Bindet einen Klick an ein Widget und alle bereits vorhandenen Kinder."""

        widget.bind("<Button-1>", lambda _ereignis: befehl())

        for kind in widget.winfo_children():
            self.mache_widget_klickbar(kind, befehl)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def semester_farbe(self, status: SemesterStatus, nicht_bestanden: bool = False) -> str:
        """Ordnet einem Semesterstatus seine Dashboardfarbe zu."""

        if nicht_bestanden:
            return FARBE_ROT

        if status == SemesterStatus.BEGONNEN:
            return FARBE_GELB

        if status == SemesterStatus.ABGESCHLOSSEN:
            return FARBE_GRUEN

        return FARBE_GRAU
# ======================================================================================================================================================


# ======================================================================================================================================================
    def semester_status_text(self, status: SemesterStatus) -> str:
        """Formatiert einen Semesterstatus als lesbaren Text."""

        if status == SemesterStatus.BEGONNEN:
            return "BEGONNEN"

        if status == SemesterStatus.ABGESCHLOSSEN:
            return "ABGESCHLOSSEN"

        return "NICHT BEGONNEN"
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_farbe(self, status: KursStatus, nicht_bestanden: bool = False) -> str:
        """Ordnet einem Kursstatus seine Dashboardfarbe zu."""

        if nicht_bestanden:
            return FARBE_ROT

        if status == KursStatus.BEGONNEN:
            return FARBE_GELB

        if status == KursStatus.ABGESCHLOSSEN:
            return FARBE_GRUEN

        if status == KursStatus.ANERKANNT:
            return FARBE_BLAU

        return FARBE_GRAU
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_status_text(self, status: KursStatus) -> str:
        """Formatiert einen Kursstatus als lesbaren Text."""

        if status == KursStatus.BEGONNEN:
            return "BEGONNEN"

        if status == KursStatus.ABGESCHLOSSEN:
            return "ABGESCHLOSSEN"

        if status == KursStatus.ANERKANNT:
            return "ANERKANNT"

        return "NICHT BEGONNEN"
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kurs_linker_text(self, kurs: Kurs) -> str:
        """Erstellt den kurzen Text im farbigen Statusbereich einer Kurskarte.

        Eine vorhandene Note wird direkt angezeigt. Kurse ohne Note erhalten nur einen
        neutralen Punkt. Die ECTS werden ausschließlich im Inhaltsbereich ausgegeben.
        """

        # Nur tatsächlich vorhandene Noten dürfen in den gewichteten Notenschnitt einfließen.
        if kurs.note is not None:
            return f"{kurs.note:.1f}"

        return "●"
# ======================================================================================================================================================
