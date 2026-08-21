import tkinter as tk
from tkinter import ttk
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from dashboard import (
    FARBE_BLAU,
    FARBE_GELB,
    FARBE_GRAU,
    FARBE_GRUEN,
    FARBE_ROT,
    FARBE_KARTE,
    FARBE_TEXT
)
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
class Hilfebereich:
    """Baut das Hilfefenster auf und erklärt die sichtbaren Bereiche und Symbole."""


    def __init__(self, anwendung) -> None:
        """Verknüpft das Hilfefenster mit dem Hauptfenster."""

        self.anwendung = anwendung
# ======================================================================================================================================================


# ======================================================================================================================================================
    def hilfe_anzeigen(self) -> None:
        """Öffnet ein zentriertes Hilfefenster und baut seine Abschnitte nacheinander auf."""

        hilfe = tk.Toplevel(self.anwendung)
        hilfe.title("Hilfe zum StudienDashboard")
        hilfe.resizable(False, False)
        hilfe.transient(self.anwendung)
        hilfe.grab_set()

        inhalt = ttk.Frame(hilfe, padding = 22)
        inhalt.pack(fill = "both", expand = True)

        naechste_zeile = 0
        naechste_zeile = self.baue_hilfe_bereiche(inhalt, naechste_zeile)
        naechste_zeile = self.baue_hilfe_symbole(inhalt, naechste_zeile)
        naechste_zeile = self.baue_hilfe_statusfarben(inhalt, naechste_zeile)

        schliessen = ttk.Button(
            inhalt,
            text = "Schließen",
            command = hilfe.destroy
        )
        schliessen.grid(
            row = naechste_zeile,
            column = 0,
            columnspan = 2,
            sticky = "e",
            pady = (18, 0)
        )

        hilfe.bind("<Escape>", lambda _ereignis: hilfe.destroy())
        self.zentriere_hilfefenster(hilfe)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_hilfe_bereiche(self, parent: tk.Misc, startzeile: int) -> int:
        """Erklärt die drei großen Bereiche des Dashboards."""

        titel = ttk.Label(
            parent,
            text = "Was macht welcher Bereich?",
            font = ("Arial", 14, "bold")
        )
        titel.grid(
            row = startzeile,
            column = 0,
            columnspan = 2,
            sticky = "w",
            pady = (0, 12)
        )

        zeile = startzeile + 1

        bereiche = [
            (
                "Studienfortschritt",
                "Zeigt die bereits gesammelten ECTS im Verhältnis zu den Gesamt-ECTS."
            ),
            (
                "Semesterübersicht",
                "Zeigt alle Semester und ihren Fortschritt. Ein Klick auf die weiße Fläche wählt das Semester aus."
            ),
            (
                "Kursübersicht",
                "Zeigt die Kurse des gewählten Semesters. Ein Klick auf die weiße Fläche wählt den Kurs aus."
            )
        ]

        for bezeichnung, erklaerung in bereiche:
            self.baue_hilfe_textzeile(parent, zeile, bezeichnung, erklaerung)
            zeile = zeile + 1

        return self.baue_hilfe_trennung(parent, zeile)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_hilfe_symbole(self, parent: tk.Misc, startzeile: int) -> int:
        """Zeigt die Symbole, die auch auf Semester- und Kurskarten verwendet werden."""

        titel = ttk.Label(
            parent,
            text = "Was bewirken die Symbole?",
            font = ("Arial", 14, "bold")
        )
        titel.grid(
            row = startzeile,
            column = 0,
            columnspan = 2,
            sticky = "w",
            pady = (0, 10)
        )

        zeile = startzeile + 1

        symbole = [
            ("▶", "Kurs beginnen"),
            ("■", "Kurs zurücksetzen; bei abgeschlossenen Kursen wird auch die Note entfernt"),
            ("✎", "Kurs bearbeiten"),
            ("✓", "Note eintragen und Kurs abschließen"),
            ("🗑", "Semester oder Kurs nach Rückfrage löschen"),
            ("+", "Neues Semester oder neuen Kurs anlegen, solange noch Platz vorhanden ist")
        ]

        for symbol, erklaerung in symbole:
            symbol_label = tk.Label(
                parent,
                text = symbol,
                font = ("Segoe UI Symbol", 13, "bold"),
                foreground = FARBE_TEXT,
                background = FARBE_KARTE,
                width = 3
            )
            symbol_label.grid(row = zeile, column = 0, sticky = "w", pady = 3)

            text = ttk.Label(
                parent,
                text = erklaerung,
                wraplength = 520,
                justify = "left"
            )
            text.grid(row = zeile, column = 1, sticky = "w", pady = 3)

            zeile = zeile + 1

        return self.baue_hilfe_trennung(parent, zeile)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_hilfe_statusfarben(self, parent: tk.Misc, startzeile: int) -> int:
        """Erklärt die verwendeten Statusfarben."""

        titel = ttk.Label(
            parent,
            text = "Statusfarben",
            font = ("Arial", 14, "bold")
        )
        titel.grid(
            row = startzeile,
            column = 0,
            columnspan = 2,
            sticky = "w",
            pady = (0, 10)
        )

        zeile = startzeile + 1

        statuswerte = [
            (FARBE_GRAU, "Nicht begonnen"),
            (FARBE_GELB, "Begonnen"),
            (FARBE_GRUEN, "Abgeschlossen"),
            (FARBE_BLAU, "Anerkannt"),
            (FARBE_ROT, "Nicht bestanden")
        ]

        for farbe, erklaerung in statuswerte:
            farbfeld = tk.Label(parent, text = "", background = farbe, width = 3)
            farbfeld.grid(row = zeile, column = 0, sticky = "w", pady = 3)

            text = ttk.Label(parent, text = erklaerung)
            text.grid(row = zeile, column = 1, sticky = "w", pady = 3)

            zeile = zeile + 1

        return zeile
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_hilfe_textzeile(
            self,
            parent: tk.Misc,
            zeile: int,
            bezeichnung: str,
            erklaerung: str
    ) -> None:
        """Baut eine zweispaltige Erklärungszeile auf."""

        name = ttk.Label(
            parent,
            text = bezeichnung + ":",
            font = ("Arial", 10, "bold")
        )
        name.grid(row = zeile, column = 0, sticky = "nw", padx = (0, 12), pady = 3)

        text = ttk.Label(
            parent,
            text = erklaerung,
            wraplength = 520,
            justify = "left"
        )
        text.grid(row = zeile, column = 1, sticky = "w", pady = 3)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_hilfe_trennung(self, parent: tk.Misc, zeile: int) -> int:
        """Setzt eine Trennlinie und gibt die nächste freie Zeile zurück."""

        trennung = ttk.Separator(parent, orient = "horizontal")
        trennung.grid(
            row = zeile,
            column = 0,
            columnspan = 2,
            sticky = "ew",
            pady = 14
        )

        return zeile + 1
# ======================================================================================================================================================


# ======================================================================================================================================================
    def zentriere_hilfefenster(self, hilfe: tk.Toplevel) -> None:
        """Positioniert das Hilfefenster mittig über dem Hauptfenster."""

        hilfe.update_idletasks()

        breite = hilfe.winfo_reqwidth()
        hoehe = hilfe.winfo_reqheight()
        x_position = self.anwendung.winfo_rootx() + (self.anwendung.winfo_width() - breite) // 2
        y_position = self.anwendung.winfo_rooty() + (self.anwendung.winfo_height() - hoehe) // 2

        hilfe.geometry(f"{breite}x{hoehe}+{x_position}+{y_position}")
# ======================================================================================================================================================
