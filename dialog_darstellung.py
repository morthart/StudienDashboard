# Dieses Modul: Bündelt die verschiedenen Dialogtypen hinter einer gemeinsamen Schnittstelle.
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from dialog_einfach import auswahl_treffen
from dialog_kurs import kursdaten_eingeben
from dialog_note import note_eingeben
from dialog_studiengang import studiengangsdaten_eingeben
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
# Klasse DialogDarstellung: Bündelt sämtliche Dialoge und Meldungsfenster der Anwendung.
class DialogDarstellung:
    """Bündelt sämtliche Dialoge und Meldungsfenster der Anwendung.

    Nur diese Darstellungsklasse kennt messagebox, filedialog und die konkreten
    Tkinter-Dialogfunktionen. Die Steuerungs- und Verwaltungsklassen arbeiten
    ausschließlich mit Rückgabewerten dieser Klasse.
    """
# ======================================================================================================================================================


# ======================================================================================================================================================
    def __init__(self, parent: tk.Misc) -> None:
        """Merkt sich das Hauptfenster als Elternfenster für alle Dialoge."""

        self.parent = parent
# ======================================================================================================================================================


# ======================================================================================================================================================
    def zeige_info(self, titel: str, text: str) -> None:
        """Zeigt eine normale Informationsmeldung an."""

        messagebox.showinfo(titel, text, parent = self.parent)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def zeige_fehler(self, titel: str, text: str) -> None:
        """Zeigt eine Fehlermeldung an."""

        messagebox.showerror(titel, text, parent = self.parent)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def zeige_warnung(self, titel: str, text: str) -> None:
        """Zeigt eine Warnmeldung an."""

        messagebox.showwarning(titel, text, parent = self.parent)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def frage_ja_nein(self, titel: str, text: str) -> bool:
        """Zeigt eine Ja-/Nein-Abfrage und gibt die Auswahl zurück."""

        return messagebox.askyesno(titel, text, parent = self.parent)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def frage_ja_nein_abbrechen(self, titel: str, text: str) -> bool | None:
        """Zeigt eine Ja-/Nein-/Abbrechen-Abfrage und gibt die Auswahl zurück."""

        return messagebox.askyesnocancel(titel, text, parent = self.parent)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def speicherort_auswaehlen(self, titel: str, startordner: Path) -> Path | None:
        """Lässt einen Basisordner auswählen und gibt diesen als Path zurück."""

        self.parent.withdraw()

        basisordner = filedialog.askdirectory(
            title = titel,
            initialdir = str(startordner),
            parent = self.parent
        )

        self.parent.deiconify()

        if not basisordner:
            return None

        return Path(basisordner)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def studiengangsdaten_eingeben(
            self,
            titel: str,
            start_name: str = "",
            start_wunschnote: float | None = None,
            start_gesamt_ects: int | None = None,
            min_gesamt_ects: int | None = None
    ) -> tuple[str, float, int] | None:
        """Öffnet den Dialog für die Daten eines Studiengangs."""

        argumente = {
            "parent": self.parent,
            "titel": titel,
            "start_name": start_name,
            "start_wunschnote": start_wunschnote,
            "start_gesamt_ects": start_gesamt_ects
        }

        if min_gesamt_ects is not None:
            argumente["min_gesamt_ects"] = min_gesamt_ects

        return studiengangsdaten_eingeben(**argumente)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def kursdaten_eingeben(
            self,
            titel: str,
            max_ects: int,
            start_name: str = "",
            start_ects: int | None = None,
            start_anerkannt: bool = False
    ) -> tuple[str, int, bool] | None:
        """Öffnet den Dialog für die Daten eines Kurses."""

        return kursdaten_eingeben(
            parent = self.parent,
            titel = titel,
            max_ects = max_ects,
            start_name = start_name,
            start_ects = start_ects,
            start_anerkannt = start_anerkannt
        )
# ======================================================================================================================================================


# ======================================================================================================================================================
    def note_eingeben(self, titel: str, beschriftung: str, startwert: str = "") -> float | None:
        """Öffnet den Dialog zur Eingabe einer Kursnote."""

        return note_eingeben(
            self.parent,
            titel,
            beschriftung,
            startwert
        )
# ======================================================================================================================================================


# ======================================================================================================================================================
    def auswahl_treffen(self, titel: str, beschriftung: str, werte: list[str]) -> int | None:
        """Öffnet einen allgemeinen Auswahldialog."""

        return auswahl_treffen(
            self.parent,
            titel,
            beschriftung,
            werte
        )
# ======================================================================================================================================================
