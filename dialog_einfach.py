import tkinter as tk
from tkinter import messagebox, ttk
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from dialog_basis import fenster_zentrieren
from konstanten import ECTS_PRO_SEMESTER, MIN_ECTS_PRO_KURS
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
class EingabeDialog(tk.Toplevel):
    """Zentraler Dialog für Texteingaben; Escape bricht ohne Änderung ab."""

    def __init__(self, parent: tk.Misc, titel: str, beschriftung: str, startwert: str = "") -> None:
        """Baut einen einfachen Textdialog auf und wartet auf Eingabe oder Abbruch."""

        super().__init__(parent)

        self.ergebnis: str | None = None

        self.title(titel)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        inhalt = ttk.Frame(self, padding = 18)
        inhalt.pack(fill = "both", expand = True)

        beschriftung_label = ttk.Label(inhalt, text = beschriftung)
        beschriftung_label.pack(anchor = "w", pady = (0, 8))

        self.eingabe = ttk.Entry(inhalt, width = 44)
        self.eingabe.insert(0, startwert)
        self.eingabe.pack(fill = "x")

        knoepfe = ttk.Frame(inhalt)
        knoepfe.pack(fill = "x", pady = (18, 0))

        abbrechen = ttk.Button(knoepfe, text = "Abbrechen", command = self.abbrechen)
        abbrechen.pack(side = "right")

        uebernehmen = ttk.Button(knoepfe, text = "Übernehmen", command = self.uebernehmen)
        uebernehmen.pack(side = "right", padx = (0, 8))

        self.bind("<Escape>", self.escape_gedrueckt)
        self.bind("<Return>", self.enter_gedrueckt)
        self.protocol("WM_DELETE_WINDOW", self.abbrechen)

        fenster_zentrieren(self, parent)
        self.eingabe.focus_set()
        self.wait_window()

    def escape_gedrueckt(self, _ereignis: tk.Event) -> None:
        """Leitet Escape an die Abbruchfunktion weiter."""

        self.abbrechen()

    def enter_gedrueckt(self, _ereignis: tk.Event) -> None:
        """Leitet Enter an die Übernahmefunktion weiter."""

        self.uebernehmen()

    def uebernehmen(self) -> None:
        """Übernimmt die Eingabe und schließt den Dialog."""

        self.ergebnis = self.eingabe.get()
        self.destroy()

    def abbrechen(self) -> None:
        """Schließt den Dialog ohne eine Eingabe zurückzugeben."""

        self.ergebnis = None
        self.destroy()
# ======================================================================================================================================================


# ======================================================================================================================================================
class AuswahlDialog(tk.Toplevel):
    """Zentraler Dialog für eine Auswahl aus einer Liste."""

    def __init__(self, parent: tk.Misc, titel: str, beschriftung: str, werte: list[str]) -> None:
        """Baut eine Liste auf und wartet auf Auswahl oder Abbruch."""

        super().__init__(parent)

        self.ergebnis: int | None = None

        self.title(titel)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        inhalt = ttk.Frame(self, padding = 18)
        inhalt.pack(fill = "both", expand = True)

        beschriftung_label = ttk.Label(inhalt, text = beschriftung)
        beschriftung_label.pack(anchor = "w", pady = (0, 8))

        self.liste = tk.Listbox(
            inhalt,
            width = 52,
            height = min(max(len(werte), 5), 14),
            activestyle = "dotbox",
            exportselection = False
        )
        self.liste.pack(fill = "both", expand = True)

        for wert in werte:
            self.liste.insert("end", wert)

        if werte:
            self.liste.selection_set(0)

        knoepfe = ttk.Frame(inhalt)
        knoepfe.pack(fill = "x", pady = (18, 0))

        abbrechen = ttk.Button(knoepfe, text = "Abbrechen", command = self.abbrechen)
        abbrechen.pack(side = "right")

        auswaehlen = ttk.Button(knoepfe, text = "Auswählen", command = self.uebernehmen)
        auswaehlen.pack(side = "right", padx = (0, 8))

        self.bind("<Escape>", self.escape_gedrueckt)
        self.bind("<Return>", self.enter_gedrueckt)
        self.liste.bind("<Double-Button-1>", self.doppelklick)
        self.protocol("WM_DELETE_WINDOW", self.abbrechen)

        fenster_zentrieren(self, parent)
        self.liste.focus_set()
        self.wait_window()

    def escape_gedrueckt(self, _ereignis: tk.Event) -> None:
        """Bricht die Auswahl mit Escape ab."""

        self.abbrechen()

    def enter_gedrueckt(self, _ereignis: tk.Event) -> None:
        """Übernimmt die aktuelle Auswahl mit Enter."""

        self.uebernehmen()

    def doppelklick(self, _ereignis: tk.Event) -> None:
        """Übernimmt die Auswahl per Doppelklick."""

        self.uebernehmen()

    def uebernehmen(self) -> None:
        """Speichert den Index des ausgewählten Eintrags."""

        auswahl = self.liste.curselection()

        if not auswahl:
            return

        self.ergebnis = int(auswahl[0])
        self.destroy()

    def abbrechen(self) -> None:
        """Schließt den Dialog ohne Auswahl."""

        self.ergebnis = None
        self.destroy()
# ======================================================================================================================================================


# ======================================================================================================================================================
def text_eingeben(
        parent: tk.Misc,
        titel: str,
        beschriftung: str,
        startwert: str = "",
        darf_leer_sein: bool = False
) -> str | None:
    """Liest einen Text ein und verhindert leere Pflichtfelder."""

    while True:
        dialog = EingabeDialog(parent, titel, beschriftung, startwert)

        if dialog.ergebnis is None:
            return None

        wert = dialog.ergebnis.strip()

        if wert:
            return wert

        if darf_leer_sein:
            return wert

        messagebox.showerror(
            "Ungültige Eingabe",
            "Die Eingabe darf nicht leer sein.",
            parent = parent
        )
# ======================================================================================================================================================


# ======================================================================================================================================================
def ganze_zahl_eingeben(
        parent: tk.Misc,
        titel: str,
        beschriftung: str,
        startwert: str = ""
) -> int | None:
    """Liest eine ganze Zahl über die zentrale Eingabefunktion ein."""

    while True:
        wert = text_eingeben(parent, titel, beschriftung, startwert)

        if wert is None:
            return None

        try:
            zahl = int(wert)
        except ValueError:
            messagebox.showerror(
                "Ungültige Eingabe",
                "Bitte eine ganze Zahl eingeben.",
                parent = parent
            )
            continue

        return zahl
# ======================================================================================================================================================


# ======================================================================================================================================================
def ects_eingeben(
        parent: tk.Misc,
        titel: str,
        beschriftung: str,
        max_ects: int,
        startwert: str = ""
) -> int | None:
    """Liest einen positiven, durch fünf teilbaren ECTS-Wert ein."""

    while True:
        ects = ganze_zahl_eingeben(parent, titel, beschriftung, startwert)

        if ects is None:
            return None

        if ects <= 0:
            messagebox.showerror(
                "Ungültige Eingabe",
                "Die ECTS müssen größer als 0 sein.",
                parent = parent
            )
            continue

        if ects % MIN_ECTS_PRO_KURS != 0:
            messagebox.showerror(
                "Ungültige Eingabe",
                f"Bitte ein Vielfaches von {MIN_ECTS_PRO_KURS} eingeben",
                parent = parent
            )
            continue

        if ects > max_ects:
            messagebox.showerror(
                "Ungültige Eingabe",
                f"Es können maximal {max_ects} ECTS eingetragen werden.",
                parent = parent
            )
            continue

        return ects
# ======================================================================================================================================================


# ======================================================================================================================================================
def gesamt_ects_eingeben(
        parent: tk.Misc,
        titel: str,
        beschriftung: str,
        startwert: str = ""
) -> int | None:
    """Liest Gesamt-ECTS ein, die positiv und durch die ECTS pro Semester teilbar sind."""

    while True:
        ects = ganze_zahl_eingeben(parent, titel, beschriftung, startwert)

        if ects is None:
            return None

        if ects <= 0:
            messagebox.showerror(
                "Ungültige Eingabe",
                "Die Gesamt-ECTS müssen größer als 0 sein.",
                parent = parent
            )
            continue

        if ects % ECTS_PRO_SEMESTER != 0:
            messagebox.showerror(
                "Ungültige Eingabe",
                "Die Gesamt-ECTS müssen durch die ECTS pro Semester teilbar sein.",
                parent = parent
            )
            continue

        return ects
# ======================================================================================================================================================


# ======================================================================================================================================================
def auswahl_treffen(
        parent: tk.Misc,
        titel: str,
        beschriftung: str,
        werte: list[str]
) -> int | None:
    """Zeigt eine zentrierte Listenauswahl und gibt den gewählten Index zurück."""

    if not werte:
        messagebox.showinfo(
            "Keine Einträge",
            "Es stehen keine Einträge zur Auswahl.",
            parent = parent
        )
        return None

    dialog = AuswahlDialog(parent, titel, beschriftung, werte)

    return dialog.ergebnis
# ======================================================================================================================================================
