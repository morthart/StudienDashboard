import tkinter as tk
from tkinter import ttk
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from dialog_basis import fenster_zentrieren, zeige_eingabefehler
from konstanten import ECTS_PRO_SEMESTER, MIN_GESAMT_ECTS
from dialog_pruefungen import pruefe_gesamt_ects_wert, pruefe_name, pruefe_wunschnote
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
class StudiengangDatenDialog(tk.Toplevel):
    """Erfasst Name, Wunschnote und Gesamt-ECTS eines Studiengangs in einem Fenster."""

    def __init__(
            self,
            parent: tk.Misc,
            titel: str,
            start_name: str = "",
            start_wunschnote: float | None = None,
            start_gesamt_ects: int | None = None,
            min_gesamt_ects: int = MIN_GESAMT_ECTS
    ) -> None:
        """Baut den gemeinsamen Dialog für Anlegen und Bearbeiten auf."""

        super().__init__(parent)

        self.ergebnis: tuple[str, float, int] | None = None
        self.min_gesamt_ects = min_gesamt_ects

        self.title(titel)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        inhalt = ttk.Frame(self, padding = 20)
        inhalt.pack(fill = "both", expand = True)
        inhalt.columnconfigure(1, weight = 1)

        name_label = ttk.Label(inhalt, text = "Name:")
        name_label.grid(row = 0, column = 0, sticky = "w", padx = (0, 12), pady = (0, 12))

        self.name_eingabe = ttk.Entry(inhalt, width = 48)
        self.name_eingabe.insert(0, start_name)
        self.name_eingabe.grid(row = 0, column = 1, sticky = "ew", pady = (0, 12))

        wunschnote_label = ttk.Label(inhalt, text = "Wunschnote:")
        wunschnote_label.grid(row = 1, column = 0, sticky = "w", padx = (0, 12), pady = (0, 12))

        wunschnote_bereich = ttk.Frame(inhalt)
        wunschnote_bereich.grid(row = 1, column = 1, sticky = "w", pady = (0, 12))

        self.wunschnote_eingabe = ttk.Entry(wunschnote_bereich, width = 12)

        if start_wunschnote is not None:
            self.wunschnote_eingabe.insert(0, f"{start_wunschnote:.1f}")

        self.wunschnote_eingabe.pack(side = "left")

        wunschnote_hinweis = ttk.Label(
            wunschnote_bereich,
            text = "1.0 bis 4.0",
            foreground = "#667085"
        )
        wunschnote_hinweis.pack(side = "left", padx = (10, 0))

        gesamt_ects_label = ttk.Label(inhalt, text = "Gesamt-ECTS:")
        gesamt_ects_label.grid(row = 2, column = 0, sticky = "w", padx = (0, 12), pady = (0, 12))

        gesamt_ects_bereich = ttk.Frame(inhalt)
        gesamt_ects_bereich.grid(row = 2, column = 1, sticky = "w", pady = (0, 12))

        self.gesamt_ects_eingabe = ttk.Entry(gesamt_ects_bereich, width = 12)

        if start_gesamt_ects is not None:
            self.gesamt_ects_eingabe.insert(0, str(start_gesamt_ects))

        self.gesamt_ects_eingabe.pack(side = "left")

        gesamt_ects_hinweis = ttk.Label(
            gesamt_ects_bereich,
            text = f"{ECTS_PRO_SEMESTER} ECTS pro Semester",
            foreground = "#667085"
        )
        gesamt_ects_hinweis.pack(side = "left", padx = (10, 0))

        knoepfe = ttk.Frame(inhalt)
        knoepfe.grid(row = 3, column = 0, columnspan = 2, sticky = "ew", pady = (20, 0))

        abbrechen = ttk.Button(knoepfe, text = "Abbrechen", command = self.abbrechen)
        abbrechen.pack(side = "right")

        uebernehmen = ttk.Button(knoepfe, text = "Übernehmen", command = self.uebernehmen)
        uebernehmen.pack(side = "right", padx = (0, 8))

        self.bind("<Escape>", self.escape_gedrueckt)
        self.bind("<Return>", self.enter_gedrueckt)
        self.protocol("WM_DELETE_WINDOW", self.abbrechen)

        fenster_zentrieren(self, parent)
        self.name_eingabe.focus_set()
        self.wait_window()

    def escape_gedrueckt(self, _ereignis: tk.Event) -> None:
        """Bricht den Dialog mit Escape ohne Änderungen ab."""

        self.abbrechen()

    def enter_gedrueckt(self, _ereignis: tk.Event) -> None:
        """Versucht, alle Eingaben mit Enter zu übernehmen."""

        self.uebernehmen()

    def uebernehmen(self) -> None:
        """Prüft die drei Felder nacheinander und übernimmt nur vollständige Daten."""

        try:
            name = pruefe_name(
                self.name_eingabe.get(),
                "Bitte Studiengangnamen eingeben."
            )
        except ValueError as fehler:
            zeige_eingabefehler(self, self.name_eingabe, str(fehler))
            return

        try:
            wunschnote = pruefe_wunschnote(self.wunschnote_eingabe.get())
        except ValueError as fehler:
            zeige_eingabefehler(self, self.wunschnote_eingabe, str(fehler))
            return

        try:
            gesamt_ects = pruefe_gesamt_ects_wert(
                self.gesamt_ects_eingabe.get(),
                self.min_gesamt_ects
            )
        except ValueError as fehler:
            zeige_eingabefehler(self, self.gesamt_ects_eingabe, str(fehler))
            return

        self.ergebnis = (name, wunschnote, gesamt_ects)
        self.destroy()

    def abbrechen(self) -> None:
        """Schließt den Dialog ohne Studiengangsdaten zurückzugeben."""

        self.ergebnis = None
        self.destroy()
# ======================================================================================================================================================


# ======================================================================================================================================================
def studiengangsdaten_eingeben(
        parent: tk.Misc,
        titel: str,
        start_name: str = "",
        start_wunschnote: float | None = None,
        start_gesamt_ects: int | None = None,
        min_gesamt_ects: int = MIN_GESAMT_ECTS
) -> tuple[str, float, int] | None:
    """Öffnet den gemeinsamen Dialog zum Anlegen oder Bearbeiten eines Studiengangs."""

    dialog = StudiengangDatenDialog(
        parent = parent,
        titel = titel,
        start_name = start_name,
        start_wunschnote = start_wunschnote,
        start_gesamt_ects = start_gesamt_ects,
        min_gesamt_ects = min_gesamt_ects
    )

    return dialog.ergebnis
# ======================================================================================================================================================
