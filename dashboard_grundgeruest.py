# Dieses Modul: Erzeugt das Grundgerüst des Hauptfensters und ordnet die großen GUI-Bereiche an.
import tkinter as tk
from tkinter import ttk
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from konstanten import FARBE_HINTERGRUND, FARBE_PROGRESS_HINTERGRUND, FARBE_GRUEN
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
# Klasse DashboardGrundgeruest: Baut ausschließlich das Hauptfenster, Menü und den scrollbaren Bereich auf.
class DashboardGrundgeruest:
    """Baut ausschließlich das Hauptfenster, Menü und den scrollbaren Bereich auf."""
# ======================================================================================================================================================


# ======================================================================================================================================================
    def __init__(self, anwendung, steuerung, hilfebereich) -> None:
        """Erhält die für Menüaktionen benötigten Komponenten gezielt als Abhängigkeiten."""

        self.anwendung = anwendung
        self.steuerung = steuerung
        self.hilfebereich = hilfebereich

        self.kopfbereich: tk.Frame | None = None
        self.canvas: tk.Canvas | None = None
        self.scrollbar: ttk.Scrollbar | None = None
        self.dashboard: tk.Frame | None = None
        self.dashboard_fenster: int | None = None
# ======================================================================================================================================================


# ======================================================================================================================================================
    def setze_ttk_stile(self) -> None:
        """Definiert wenige, einheitliche Tkinter-Stile für das Dashboard."""

        stil = ttk.Style(self.anwendung)

        # Fehler bei Datei-, Konfigurations- oder Benutzervorgängen werden hier kontrolliert behandelt, statt die Anwendung abzubrechen.
        try:
            stil.theme_use("clam")
        except tk.TclError:
            pass

        stil.configure(
            "Dashboard.Horizontal.TProgressbar",
            troughcolor = FARBE_PROGRESS_HINTERGRUND,
            background = FARBE_GRUEN,
            bordercolor = FARBE_PROGRESS_HINTERGRUND,
            lightcolor = FARBE_GRUEN,
            darkcolor = FARBE_GRUEN,
            thickness = 14
        )

        stil.configure(
            "TButton",
            font = ("Arial", 10),
            padding = (10, 7)
        )
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_grundgeruest(self) -> None:
        """Erstellt Menüleiste, Kopfbereich und den scrollbaren Dashboardbereich."""

        self.baue_menu()

        self.kopfbereich = tk.Frame(self.anwendung, background = FARBE_HINTERGRUND)
        self.kopfbereich.pack(fill = "x", padx = 20, pady = (18, 8))

        self.canvas = tk.Canvas(
            self.anwendung,
            background = FARBE_HINTERGRUND,
            highlightthickness = 0
        )
        self.canvas.pack(side = "left", fill = "both", expand = True)

        self.scrollbar = ttk.Scrollbar(
            self.anwendung,
            orient = "vertical",
            command = self.canvas.yview
        )
        self.scrollbar.pack(side = "right", fill = "y")

        self.canvas.configure(yscrollcommand = self.scrollbar.set)

        self.dashboard = tk.Frame(self.canvas, background = FARBE_HINTERGRUND)
        self.dashboard_fenster = self.canvas.create_window(
            (0, 0),
            window = self.dashboard,
            anchor = "nw"
        )

        self.dashboard.bind("<Configure>", self.dashboard_groesse_geaendert)
        self.canvas.bind("<Configure>", self.canvas_groesse_geaendert)
        self.canvas.bind_all("<MouseWheel>", self.mausrad)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_menu(self) -> None:
        """Erstellt das Studiengang-Menü links oben im Hauptfenster."""

        menuleiste = tk.Menu(self.anwendung)
        studiengang_menu = tk.Menu(menuleiste, tearoff = False)

        studiengang_menu.add_command(
            label = "Studiengang anlegen...",
            command = self.steuerung.studiengang_anlegen
        )
        studiengang_menu.add_command(
            label = "Studiengang wechseln...",
            command = self.steuerung.studiengang_wechseln
        )
        studiengang_menu.add_command(
            label = "Studiengang bearbeiten...",
            command = self.steuerung.studiengang_bearbeiten
        )
        studiengang_menu.add_command(
            label = "Studiengang löschen...",
            command = self.steuerung.studiengang_loeschen
        )
        studiengang_menu.add_separator()
        studiengang_menu.add_command(
            label = "Beenden",
            command = self.steuerung.beenden
        )

        menuleiste.add_cascade(label = "Menü", menu = studiengang_menu)
        menuleiste.add_command(label = "?", command = self.steuerung.hilfe_anzeigen)

        self.anwendung.configure(menu = menuleiste)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def dashboard_groesse_geaendert(self, _ereignis: tk.Event) -> None:
        """Aktualisiert den Scrollbereich nach Änderungen am Dashboard."""

        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
# ======================================================================================================================================================


# ======================================================================================================================================================
    def canvas_groesse_geaendert(self, ereignis: tk.Event) -> None:
        """Passt die Breite des Dashboardframes an die Fensterbreite an."""

        self.canvas.itemconfigure(self.dashboard_fenster, width = ereignis.width)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def mausrad(self, ereignis: tk.Event) -> None:
        """Ermöglicht vertikales Scrollen mit dem Mausrad."""

        richtung = int(-1 * (ereignis.delta / 120))
        self.canvas.yview_scroll(richtung, "units")
# ======================================================================================================================================================


# ======================================================================================================================================================
    def entferne_alle_widgets(self, parent: tk.Misc) -> None:
        """Entfernt alle untergeordneten Widgets eines Containers."""

        for widget in parent.winfo_children():
            widget.destroy()
# ======================================================================================================================================================
