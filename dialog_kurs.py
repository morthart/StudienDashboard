# Dieses Modul: Erfasst und prüft die Daten beim Anlegen oder Bearbeiten eines Kurses.
import tkinter as tk
from tkinter import ttk
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from dialog_basis import fenster_zentrieren, zeige_eingabefehler
from dialog_pruefungen import pruefe_kurs_ects_wert, pruefe_name
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
# Klasse KursDatenDialog: Erfasst den Namen, die ECTS und die Anerkennung eines Kurses in einem Fenster.
class KursDatenDialog(tk.Toplevel):
    """Erfasst den Namen, die ECTS und die Anerkennung eines Kurses in einem Fenster."""

    def __init__(
            self,
            parent: tk.Misc,
            titel: str,
            max_ects: int,
            start_name: str = "",
            start_ects: int | None = None,
            start_anerkannt: bool = False
    ) -> None:
        """Baut den Dialog auf und wartet, bis er übernommen oder abgebrochen wird."""

        super().__init__(parent)

        self.ergebnis: tuple[str, int, bool] | None = None
        self.max_ects = max_ects

        self.title(titel)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        inhalt = ttk.Frame(self, padding = 20)
        inhalt.pack(fill = "both", expand = True)
        inhalt.columnconfigure(1, weight = 1)

        name_label = ttk.Label(inhalt, text = "Name:")
        name_label.grid(row = 0, column = 0, sticky = "w", padx = (0, 12), pady = (0, 12))

        self.name_eingabe = ttk.Entry(inhalt, width = 46)
        self.name_eingabe.insert(0, start_name)
        self.name_eingabe.grid(row = 0, column = 1, sticky = "ew", pady = (0, 12))

        ects_label = ttk.Label(inhalt, text = "ECTS:")
        ects_label.grid(row = 1, column = 0, sticky = "w", padx = (0, 12), pady = (0, 12))

        ects_bereich = ttk.Frame(inhalt)
        ects_bereich.grid(row = 1, column = 1, sticky = "w", pady = (0, 12))

        self.ects_eingabe = ttk.Entry(ects_bereich, width = 12)

        if start_ects is not None:
            self.ects_eingabe.insert(0, str(start_ects))

        self.ects_eingabe.pack(side = "left")

        ects_hinweis = ttk.Label(
            ects_bereich,
            text = f"Noch verfügbar: {max_ects}",
            foreground = "#667085"
        )
        ects_hinweis.pack(side = "left", padx = (10, 0))

        anerkannt_label = ttk.Label(inhalt, text = "Anerkannt:")
        anerkannt_label.grid(row = 2, column = 0, sticky = "w", padx = (0, 12), pady = (0, 4))

        self.anerkannt_variable = tk.BooleanVar(value = start_anerkannt)

        anerkannt = ttk.Checkbutton(
            inhalt,
            text = "",
            variable = self.anerkannt_variable
        )
        anerkannt.grid(row = 2, column = 1, sticky = "w", pady = (0, 4))

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
        """Bricht den Dialog mit Escape ohne Änderung ab."""

        self.abbrechen()

    def enter_gedrueckt(self, _ereignis: tk.Event) -> None:
        """Versucht, die Eingaben mit Enter zu übernehmen."""

        self.uebernehmen()

    def uebernehmen(self) -> None:
        """Prüft Name und ECTS und übernimmt danach auch den Anerkannt-Haken."""

        # Fehler bei Datei-, Konfigurations- oder Benutzervorgängen werden hier kontrolliert behandelt, statt die Anwendung abzubrechen.
        try:
            name = pruefe_name(
                self.name_eingabe.get(),
                "Bitte Kursnamen eingeben."
            )
        except ValueError as fehler:
            zeige_eingabefehler(self, self.name_eingabe, str(fehler))
            return

        # Fehler bei Datei-, Konfigurations- oder Benutzervorgängen werden hier kontrolliert behandelt, statt die Anwendung abzubrechen.
        try:
            ects = pruefe_kurs_ects_wert(
                self.ects_eingabe.get(),
                self.max_ects
            )
        except ValueError as fehler:
            zeige_eingabefehler(self, self.ects_eingabe, str(fehler))
            return

        anerkannt = self.anerkannt_variable.get()
        self.ergebnis = (name, ects, anerkannt)
        self.destroy()

    def abbrechen(self) -> None:
        """Schließt den Dialog, ohne Kursdaten zurückzugeben."""

        self.ergebnis = None
        self.destroy()
# ======================================================================================================================================================


# ======================================================================================================================================================
def kursdaten_eingeben(
        parent: tk.Misc,
        titel: str,
        max_ects: int,
        start_name: str = "",
        start_ects: int | None = None,
        start_anerkannt: bool = False
) -> tuple[str, int, bool] | None:
    """Öffnet den gemeinsamen Dialog für das Anlegen oder Bearbeiten eines Kurses."""

    dialog = KursDatenDialog(
        parent = parent,
        titel = titel,
        max_ects = max_ects,
        start_name = start_name,
        start_ects = start_ects,
        start_anerkannt = start_anerkannt
    )

    return dialog.ergebnis
# ======================================================================================================================================================
