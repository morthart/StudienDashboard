# Dieses Modul: Erfasst eine Kursnote und übergibt nur eine bestätigte, gültige Eingabe.
import tkinter as tk
from tkinter import ttk
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from dialog_basis import fenster_zentrieren, zeige_eingabefehler
from dialog_pruefungen import pruefe_kursnote
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
# Klasse NoteDialog: Erfasst eine Kursnote mit derselben Feldgröße und demselben Hinweis wie die Wunschnote.
class NoteDialog(tk.Toplevel):
    """Erfasst eine Kursnote mit derselben Feldgröße und demselben Hinweis wie die Wunschnote."""

    def __init__(
            self,
            parent: tk.Misc,
            titel: str,
            beschriftung: str,
            startwert: str = ""
    ) -> None:
        """Baut den Notendialog auf und wartet auf Übernahme oder Abbruch."""

        super().__init__(parent)

        self.ergebnis: float | None = None

        self.title(titel)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        inhalt = ttk.Frame(self, padding = 20)
        inhalt.pack(fill = "both", expand = True)

        note_label = ttk.Label(inhalt, text = beschriftung)
        note_label.grid(row = 0, column = 0, sticky = "w", padx = (0, 12), pady = (0, 12))

        note_bereich = ttk.Frame(inhalt)
        note_bereich.grid(row = 0, column = 1, sticky = "w", pady = (0, 12))

        self.note_eingabe = ttk.Entry(note_bereich, width = 12)
        self.note_eingabe.insert(0, startwert)
        self.note_eingabe.pack(side = "left")

        note_hinweis = ttk.Label(
            note_bereich,
            text = "1.0 / 1.3 / 1.7 / 2.0 / 2.3 / 2.7 / 3.0 / 3.3 / 3.7 / 4.0 / 5.0",
            foreground = "#667085"
        )
        note_hinweis.pack(side = "left", padx = (10, 0))

        knoepfe = ttk.Frame(inhalt)
        knoepfe.grid(row = 1, column = 0, columnspan = 2, sticky = "ew", pady = (8, 0))

        abbrechen = ttk.Button(knoepfe, text = "Abbrechen", command = self.abbrechen)
        abbrechen.pack(side = "right")

        uebernehmen = ttk.Button(knoepfe, text = "Übernehmen", command = self.uebernehmen)
        uebernehmen.pack(side = "right", padx = (0, 8))

        self.bind("<Escape>", self.escape_gedrueckt)
        self.bind("<Return>", self.enter_gedrueckt)
        self.protocol("WM_DELETE_WINDOW", self.abbrechen)

        fenster_zentrieren(self, parent)
        self.note_eingabe.focus_set()
        self.wait_window()

    def escape_gedrueckt(self, _ereignis: tk.Event) -> None:
        """Bricht die Noteneingabe mit Escape ab."""

        self.abbrechen()

    def enter_gedrueckt(self, _ereignis: tk.Event) -> None:
        """Versucht, die Note mit Enter zu übernehmen."""

        self.uebernehmen()

    def uebernehmen(self) -> None:
        """Prüft die Note und übernimmt ausschließlich eine zulässige Kursnote."""

        # Fehler bei Datei-, Konfigurations- oder Benutzervorgängen werden hier kontrolliert behandelt, statt die Anwendung abzubrechen.
        try:
            note = pruefe_kursnote(self.note_eingabe.get())
        except ValueError as fehler:
            zeige_eingabefehler(self, self.note_eingabe, str(fehler))
            return

        self.ergebnis = note
        self.destroy()

    def abbrechen(self) -> None:
        """Schließt den Dialog ohne eine Note zurückzugeben."""

        self.ergebnis = None
        self.destroy()
# ======================================================================================================================================================


# ======================================================================================================================================================
def note_eingeben(
        parent: tk.Misc,
        titel: str,
        beschriftung: str,
        startwert: str = ""
) -> float | None:
    """Öffnet den einheitlichen Notendialog und gibt eine gültige Note zurück."""

    dialog = NoteDialog(
        parent = parent,
        titel = titel,
        beschriftung = beschriftung,
        startwert = startwert
    )

    return dialog.ergebnis
# ======================================================================================================================================================
