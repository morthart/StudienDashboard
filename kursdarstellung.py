# Dieses Modul: Zeigt die Kurse des ausgewählten Semesters als GUI-Karten an.
import tkinter as tk
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from konstanten import (
    FARBE_BLAU,
    FARBE_KARTE,
    FARBE_RAND,
    FARBE_TEXT,
    FARBE_TEXT_GRAU
)
from enums import KursStatus
from konstanten import ECTS_PRO_SEMESTER
from kurs import Kurs
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
# Klasse KursDarstellung: Stellt Kurskarten dar und enthält keine fachlichen Änderungsaktionen.
class KursDarstellung:
    """Stellt Kurskarten dar und enthält keine fachlichen Änderungsaktionen."""
# ======================================================================================================================================================


# ======================================================================================================================================================
    def __init__(self, anwendung, elemente, steuerung) -> None:
        """Verknüpft Darstellung, gemeinsame Elemente und Kurssteuerung."""

        self.anwendung = anwendung
        self.elemente = elemente
        self.steuerung = steuerung
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_kurskarten(self, parent: tk.Misc) -> None:
        """Erstellt die Kursübersicht für das aktuell ausgewählte Semester."""

        inhalt = tk.Frame(parent, background = FARBE_KARTE)
        inhalt.pack(fill = "both", expand = True, padx = 14, pady = (0, 14))

        if self.anwendung.studiengang is None:
            self.zeige_kurshinweis(inhalt, "Bitte zuerst einen Studiengang anlegen oder wechseln.")
            return

        if self.anwendung.aktuelles_semester is None:
            self.zeige_kurshinweis(inhalt, "Bitte ein Semester auswählen oder anlegen.")
            return

        sichtbare_karten = self.erstelle_sichtbare_kurskarten()
        anzahl_zeilen = self.berechne_kurszeilen(len(sichtbare_karten))
        status_farbe = self.elemente.semester_farbe(
            self.anwendung.aktuelles_semester.berechne_status(),
            self.anwendung.aktuelles_semester.hat_nicht_bestandenen_kurs()
        )

        self.baue_kurs_semesteranzeige(inhalt, anzahl_zeilen, status_farbe)
        raster = self.baue_kursraster(inhalt, anzahl_zeilen)
        self.fuelle_kursraster(raster, sichtbare_karten)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def erstelle_sichtbare_kurskarten(self) -> list[Kurs | None]:
        """Erstellt die Kartenliste und ergänzt bei freiem Platz die Anlegekarte."""

        sichtbare_karten: list[Kurs | None] = []

        for kurs in self.anwendung.aktuelles_semester.kurse:
            sichtbare_karten.append(kurs)

        if self.anwendung.aktuelles_semester.kann_weiteren_kurs_aufnehmen():
            sichtbare_karten.append(None)

        return sichtbare_karten
# ======================================================================================================================================================


# ======================================================================================================================================================
    def berechne_kurszeilen(self, anzahl_karten: int) -> int:
        """Berechnet bei drei Spalten die benötigte Anzahl an Kurszeilen."""

        if anzahl_karten == 0:
            return 1

        return (anzahl_karten + 2) // 3
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_kurs_semesteranzeige(
            self,
            parent: tk.Frame,
            anzahl_zeilen: int,
            status_farbe: str
    ) -> None:
        """Zeigt links die Nummer und Statusfarbe des aktuell ausgewählten Semesters."""

        semester_bereich = tk.Label(
            parent,
            text = str(self.anwendung.aktuelles_semester.nummer),
            font = ("Arial", 22, "bold"),
            foreground = "white",
            background = status_farbe,
            width = 4
        )
        semester_bereich.grid(
            row = 0,
            column = 0,
            rowspan = anzahl_zeilen,
            sticky = "nsew",
            padx = (0, 10),
            pady = 6
        )
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_kursraster(self, parent: tk.Frame, anzahl_zeilen: int) -> tk.Frame:
        """Erstellt das Raster rechts neben der Semesternummer."""

        raster = tk.Frame(parent, background = FARBE_KARTE)
        raster.grid(row = 0, column = 1, sticky = "nsew")

        parent.columnconfigure(1, weight = 1)
        parent.rowconfigure(0, weight = 1)

        for spalte in range(3):
            raster.columnconfigure(spalte, weight = 1, uniform = "kurs")

        for zeile in range(anzahl_zeilen):
            raster.rowconfigure(zeile, weight = 1, uniform = "kurszeile")

        return raster
# ======================================================================================================================================================


# ======================================================================================================================================================
    def fuelle_kursraster(
            self,
            raster: tk.Frame,
            sichtbare_karten: list[Kurs | None]
    ) -> None:
        """Setzt vorhandene Kurse und eine mögliche Anlegekarte in das Raster."""

        # Die vorhandenen Elemente werden nacheinander ausgewertet, damit aus ihrem aktuellen Zustand das Ergebnis ermittelt werden kann.
        for index, kurs in enumerate(sichtbare_karten):
            zeile = index // 3
            spalte = index % 3

            if kurs is None:
                karte = self.baue_kurs_anlegen_karte(raster)
            else:
                karte = self.baue_kurskarte(raster, kurs)

            karte.grid(
                row = zeile,
                column = spalte,
                sticky = "nsew",
                padx = 6,
                pady = 6
            )
# ======================================================================================================================================================


# ======================================================================================================================================================
    def zeige_kurshinweis(self, parent: tk.Misc, text: str) -> None:
        """Zeigt einen einfachen Hinweis im leeren Kursbereich."""

        hinweis = tk.Label(
            parent,
            text = text,
            font = ("Arial", 11),
            foreground = FARBE_TEXT_GRAU,
            background = FARBE_KARTE
        )
        hinweis.pack(anchor = "w", pady = 24)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_kurskarte(self, parent: tk.Misc, kurs: Kurs) -> tk.Frame:
        """Erstellt eine Kurskarte und verteilt Aufbau und Aktionen auf Hilfsfunktionen."""

        karte = self.elemente.erstelle_karte(parent, breite = 390, hoehe = 145)
        karte.grid_propagate(False)
        karte.columnconfigure(1, weight = 1)
        karte.rowconfigure(0, weight = 1)

        farbe = self.elemente.kurs_farbe(kurs.status, kurs.ist_nicht_bestanden())
        self.baue_kurs_statusbereich(karte, kurs, farbe)
        inhalt = self.baue_kurs_inhalt(karte)

        name = self.baue_kurs_name(inhalt, kurs)
        status, details = self.baue_kurs_details(inhalt, kurs, farbe)
        self.baue_kurs_aktionen(inhalt, kurs)
        self.binde_kurs_auswahl([inhalt, name, status, details], kurs)

        if kurs is self.anwendung.aktueller_kurs:
            karte.configure(highlightbackground = FARBE_BLAU, highlightthickness = 2)

        return karte
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_kurs_statusbereich(self, karte: tk.Frame, kurs: Kurs, farbe: str) -> None:
        """Zeigt links ausschließlich Statusfarbe und gegebenenfalls die Kursnote."""

        status_bereich = tk.Label(
            karte,
            text = self.elemente.kurs_linker_text(kurs),
            font = ("Arial", 12, "bold"),
            foreground = "white",
            background = farbe,
            width = 5
        )
        status_bereich.grid(row = 0, column = 0, sticky = "nsew")
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_kurs_inhalt(self, karte: tk.Frame) -> tk.Frame:
        """Erstellt den weißen Inhaltsbereich der Kurskarte."""

        inhalt = tk.Frame(karte, background = FARBE_KARTE, cursor = "hand2")
        inhalt.grid(row = 0, column = 1, sticky = "nsew", padx = 14, pady = 10)
        inhalt.columnconfigure(0, weight = 1)
        inhalt.columnconfigure(1, minsize = 115)
        inhalt.rowconfigure(0, weight = 1)
        inhalt.rowconfigure(1, weight = 1)

        return inhalt
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_kurs_name(self, inhalt: tk.Frame, kurs: Kurs) -> tk.Label:
        """Zeigt den Kursnamen groß auf der linken Seite der weißen Kartenfläche."""

        name = tk.Label(
            inhalt,
            text = kurs.name,
            font = ("Arial", 13, "bold"),
            foreground = FARBE_TEXT,
            background = FARBE_KARTE,
            justify = "left",
            anchor = "w",
            wraplength = 210,
            cursor = "hand2"
        )
        name.grid(row = 0, column = 0, rowspan = 3, sticky = "nsew", padx = (0, 12))

        return name
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_kurs_details(
            self,
            inhalt: tk.Frame,
            kurs: Kurs,
            farbe: str
    ) -> tuple[tk.Label, tk.Label]:
        """Zeigt rechts Status und ECTS des Kurses."""

        status = tk.Label(
            inhalt,
            text = self.elemente.kurs_status_text(kurs.status),
            font = ("Arial", 9, "bold"),
            foreground = farbe,
            background = FARBE_KARTE,
            anchor = "e",
            cursor = "hand2"
        )
        status.grid(row = 0, column = 1, sticky = "ne")

        details = tk.Label(
            inhalt,
            text = f"{kurs.ects} ECTS",
            font = ("Arial", 9),
            foreground = FARBE_TEXT_GRAU,
            background = FARBE_KARTE,
            anchor = "e",
            cursor = "hand2"
        )
        details.grid(row = 1, column = 1, sticky = "ne", pady = (3, 0))

        return status, details
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_kurs_aktionen(self, inhalt: tk.Frame, kurs: Kurs) -> None:
        """Erstellt abhängig vom Status nur die Aktionen, die gerade sinnvoll sind."""

        aktionen = tk.Frame(inhalt, background = FARBE_KARTE)
        aktionen.grid(row = 2, column = 1, sticky = "se", pady = (8, 0))

        if kurs.status == KursStatus.NICHT_BEGONNEN:
            self.fuege_kurs_aktion_hinzu(aktionen, "▶", "Kurs beginnen", self.steuerung.kurs_beginnen, kurs)
            self.fuege_kurs_aktion_hinzu(aktionen, "✎", "Kurs bearbeiten", self.steuerung.kurs_bearbeiten, kurs)
            self.fuege_kurs_aktion_hinzu(aktionen, "✓", "Note eintragen", self.steuerung.kurs_abschliessen, kurs)

        if kurs.status == KursStatus.BEGONNEN:
            self.fuege_kurs_aktion_hinzu(aktionen, "■", "Kurs zurücksetzen", self.steuerung.kurs_stoppen, kurs)
            self.fuege_kurs_aktion_hinzu(aktionen, "✎", "Kurs bearbeiten", self.steuerung.kurs_bearbeiten, kurs)
            self.fuege_kurs_aktion_hinzu(aktionen, "✓", "Note eintragen", self.steuerung.kurs_abschliessen, kurs)

        if kurs.status == KursStatus.ABGESCHLOSSEN:
            self.fuege_kurs_aktion_hinzu(aktionen, "■", "Abschluss zurücksetzen", self.steuerung.kurs_stoppen, kurs)
            self.fuege_kurs_aktion_hinzu(aktionen, "✎", "Kurs bearbeiten", self.steuerung.kurs_bearbeiten, kurs)

        # Anerkannte Kurse zählen zu den erreichten ECTS, besitzen aber keine reguläre Kursnote.
        if kurs.status == KursStatus.ANERKANNT:
            self.fuege_kurs_aktion_hinzu(aktionen, "✎", "Kurs bearbeiten", self.steuerung.kurs_bearbeiten, kurs)

        self.fuege_kurs_aktion_hinzu(aktionen, "🗑", "Kurs löschen", self.steuerung.kurs_loeschen, kurs)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def fuege_kurs_aktion_hinzu(
            self,
            parent: tk.Frame,
            symbol: str,
            hilfetext: str,
            funktion,
            kurs: Kurs
    ) -> None:
        """Erstellt einen Symbolbutton und hängt ihn rechts an die vorhandenen Aktionen an."""

        button = self.elemente.erstelle_symbol_button(
            parent,
            symbol,
            hilfetext,
            lambda: funktion(kurs)
        )
        button.pack(side = "left")
# ======================================================================================================================================================


# ======================================================================================================================================================
    def binde_kurs_auswahl(self, widgets: list[tk.Misc], kurs: Kurs) -> None:
        """Bindet die Auswahl nur an die weißen Informationsfelder der Kurskarte."""

        for widget in widgets:
            widget.bind(
                "<Button-1>",
                lambda _ereignis, aktueller_kurs = kurs: self.steuerung.kurs_auswaehlen(
                    aktueller_kurs
                )
            )
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_kurs_anlegen_karte(self, parent: tk.Misc) -> tk.Frame:
        """Erstellt die Anlegekarte, solange Kursanzahl und ECTS-Limit dies erlauben."""

        karte = tk.Frame(
            parent,
            background = FARBE_KARTE,
            highlightbackground = FARBE_RAND,
            highlightthickness = 1,
            cursor = "hand2",
            width = 390,
            height = 145
        )
        karte.grid_propagate(False)

        plus = tk.Label(
            karte,
            text = "+",
            font = ("Arial", 30),
            foreground = FARBE_TEXT_GRAU,
            background = FARBE_KARTE,
            cursor = "hand2"
        )
        plus.pack(pady = (30, 4))

        text = tk.Label(
            karte,
            text = "Neuen Kurs anlegen",
            font = ("Arial", 11),
            foreground = FARBE_TEXT,
            background = FARBE_KARTE,
            cursor = "hand2",
            justify = "center"
        )
        text.pack()

        self.elemente.mache_widget_klickbar(karte, self.steuerung.kurs_anlegen)

        return karte
# ======================================================================================================================================================


# ======================================================================================================================================================
