# Dieses Modul: Stellt gemeinsame Grundfunktionen bereit, die von mehreren Dialogen verwendet werden.
import tkinter as tk
from tkinter import messagebox, ttk
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
def fenster_zentrieren(fenster: tk.Toplevel, parent: tk.Misc) -> None:
    """Zentriert ein Dialogfenster über dem Hauptfenster."""

    fenster.update_idletasks()
    parent.update_idletasks()

    breite = fenster.winfo_reqwidth()
    hoehe = fenster.winfo_reqheight()

    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_breite = parent.winfo_width()
    parent_hoehe = parent.winfo_height()

    x_position = parent_x + ((parent_breite - breite) // 2)
    y_position = parent_y + ((parent_hoehe - hoehe) // 2)

    fenster.geometry(f"+{x_position}+{y_position}")
# ======================================================================================================================================================


# ======================================================================================================================================================
def zeige_eingabefehler(
        parent: tk.Misc,
        eingabefeld: ttk.Entry,
        meldung: str
) -> None:
    """Zeigt eine Fehlermeldung und setzt den Eingabefokus zurück auf das betroffene Feld."""

    messagebox.showerror(
        "Ungültige Eingabe",
        meldung,
        parent = parent
    )
    eingabefeld.focus_set()
# ======================================================================================================================================================
