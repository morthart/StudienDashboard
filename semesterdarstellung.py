import tkinter as tk
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from konstanten import (
    FARBE_BLAU,
    FARBE_KARTE,
    FARBE_PROGRESS_HINTERGRUND,
    FARBE_RAND,
    FARBE_TEXT,
    FARBE_TEXT_GRAU
)
from enums import KursStatus, SemesterStatus
from kurs import Kurs
from konstanten import ECTS_PRO_SEMESTER
from semester import Semester
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
class SemesterDarstellung:
    """Stellt Semesterkarten dar und enthält keine fachlichen Änderungsaktionen."""
# ======================================================================================================================================================


# ======================================================================================================================================================
    def __init__(self, anwendung, elemente, steuerung) -> None:
        """Verknüpft Darstellung, gemeinsame Elemente und Semestersteuerung."""

        self.anwendung = anwendung
        self.elemente = elemente
        self.steuerung = steuerung
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_semesterbereich(self, parent: tk.Misc) -> None:
        """Erstellt das dynamische Raster aus Semesterkarten und optionaler Anlegekarte."""

        bereich = self.elemente.erstelle_abschnitt(parent, "Semesterübersicht")
        bereich.pack(fill = "x", padx = 20, pady = (8, 8))

        raster = tk.Frame(bereich, background = FARBE_KARTE)
        raster.pack(fill = "x", padx = 14, pady = (4, 14))

        if self.anwendung.studiengang is None:
            hinweis = tk.Label(
                raster,
                text = "Bitte zuerst einen Studiengang anlegen oder wechseln.",
                font = ("Arial", 11),
                foreground = FARBE_TEXT_GRAU,
                background = FARBE_KARTE
            )
            hinweis.pack(anchor = "w", pady = 20)
            return

        max_semester = self.anwendung.studiengang.berechne_max_semester()

        if max_semester <= 4:
            spalten = 2
        else:
            spalten = 3

        for spalte in range(spalten):
            raster.columnconfigure(spalte, weight = 1, uniform = "semester")

        sichtbare_karten = list(self.anwendung.studiengang.semester)

        darf_anlegen = len(self.anwendung.studiengang.semester) < max_semester

        if darf_anlegen:
            sichtbare_karten.append(None)

        for index, semester in enumerate(sichtbare_karten):
            zeile = index // spalten
            spalte = index % spalten

            if semester is None:
                karte = self.baue_semester_anlegen_karte(raster)
            else:
                karte = self.baue_semesterkarte(raster, semester)

            karte.grid(
                row = zeile,
                column = spalte,
                sticky = "nsew",
                padx = 8,
                pady = 8
            )
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_semesterkarte(self, parent: tk.Misc, semester: Semester) -> tk.Frame:
        """Erstellt die Karte und lässt die einzelnen Bestandteile von Hilfsfunktionen bauen."""

        karte = self.elemente.erstelle_karte(parent, breite = 390, hoehe = 145)
        karte.grid_propagate(False)
        karte.columnconfigure(1, weight = 1)
        karte.rowconfigure(0, weight = 1)

        status = semester.berechne_status()
        status_farbe = self.elemente.semester_farbe(status, semester.hat_nicht_bestandenen_kurs())

        self.baue_semester_statusbereich(karte, semester, status_farbe)
        inhalt = self.baue_semester_inhalt(karte)

        klickbare_widgets = self.baue_semester_kopf(
            inhalt,
            semester,
            status,
            status_farbe
        )

        self.baue_semester_fortschritt(inhalt, semester, status_farbe)
        self.baue_semester_schnellwahl(inhalt, semester)
        self.baue_semester_loeschen_button(inhalt, semester)
        self.binde_semester_auswahl(klickbare_widgets, semester)

        if semester is self.anwendung.aktuelles_semester:
            karte.configure(highlightbackground = FARBE_BLAU, highlightthickness = 2)

        return karte
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_semester_statusbereich(
            self,
            karte: tk.Frame,
            semester: Semester,
            status_farbe: str
    ) -> None:
        """Zeigt links nur die Semesternummer und die berechnete Statusfarbe."""

        status_bereich = tk.Label(
            karte,
            text = str(semester.nummer),
            font = ("Arial", 20, "bold"),
            foreground = "white",
            background = status_farbe,
            width = 3
        )
        status_bereich.grid(row = 0, column = 0, sticky = "nsew")
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_semester_inhalt(self, karte: tk.Frame) -> tk.Frame:
        """Erstellt den weißen Inhaltsbereich rechts neben der Semesternummer."""

        inhalt = tk.Frame(karte, background = FARBE_KARTE, cursor = "hand2")
        inhalt.grid(row = 0, column = 1, sticky = "nsew", padx = 16, pady = 10)
        inhalt.columnconfigure(0, weight = 1)

        return inhalt
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_semester_kopf(
            self,
            inhalt: tk.Frame,
            semester: Semester,
            status: SemesterStatus,
            status_farbe: str
    ) -> list[tk.Misc]:
        """Baut Titel und Statustext und gibt beide als klickbare Widgets zurück."""

        titel = tk.Label(
            inhalt,
            text = f"Semester {semester.nummer}",
            font = ("Arial", 12, "bold"),
            foreground = FARBE_TEXT,
            background = FARBE_KARTE,
            cursor = "hand2"
        )
        titel.grid(row = 0, column = 0, sticky = "w")

        status_text = tk.Label(
            inhalt,
            text = self.elemente.semester_status_text(status),
            font = ("Arial", 9, "bold"),
            foreground = status_farbe,
            background = FARBE_KARTE,
            cursor = "hand2"
        )
        status_text.grid(row = 0, column = 1, sticky = "e")

        return [inhalt, titel, status_text]
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_semester_fortschritt(
            self,
            inhalt: tk.Frame,
            semester: Semester,
            status_farbe: str
    ) -> None:
        """Zeigt erreichte ECTS, Prozentwert und den schmalen Fortschrittsbalken."""

        erreicht = semester.berechne_erreichte_ects()
        prozent = (erreicht / ECTS_PRO_SEMESTER) * 100

        ects_text = tk.Label(
            inhalt,
            text = f"{erreicht} / {ECTS_PRO_SEMESTER} ECTS",
            font = ("Arial", 12, "bold"),
            foreground = FARBE_TEXT,
            background = FARBE_KARTE,
            cursor = "hand2"
        )
        ects_text.grid(row = 1, column = 0, sticky = "w", pady = (12, 4))

        prozent_text = tk.Label(
            inhalt,
            text = f"{prozent:.0f} %",
            font = ("Arial", 10),
            foreground = FARBE_TEXT,
            background = FARBE_KARTE,
            cursor = "hand2"
        )
        prozent_text.grid(row = 1, column = 1, sticky = "e", pady = (12, 4))

        balken_hintergrund = tk.Frame(
            inhalt,
            background = FARBE_PROGRESS_HINTERGRUND,
            height = 4
        )
        balken_hintergrund.grid(row = 2, column = 0, columnspan = 2, sticky = "ew")
        balken_hintergrund.grid_propagate(False)

        balken_fuellung = tk.Frame(
            balken_hintergrund,
            background = status_farbe,
            height = 4
        )
        balken_fuellung.place(relx = 0, rely = 0, relwidth = prozent / 100, relheight = 1)

        self.binde_semester_auswahl([ects_text, prozent_text], semester)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_semester_schnellwahl(self, inhalt: tk.Frame, semester: Semester) -> None:
        """Erzeugt für jeden Kurs einen kleinen Button direkt in der Semesterkarte."""

        kurs_schnellwahl = tk.Frame(inhalt, background = FARBE_KARTE)
        kurs_schnellwahl.grid(row = 3, column = 0, sticky = "w", pady = (8, 0))

        for kurs in semester.kurse:
            self.baue_semester_kursbutton(kurs_schnellwahl, semester, kurs)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_semester_loeschen_button(self, inhalt: tk.Frame, semester: Semester) -> None:
        """Setzt den Mülleimer rechts unten in die Semesterkarte."""

        loeschen = self.elemente.erstelle_symbol_button(
            parent = inhalt,
            symbol = "🗑",
            hilfetext = "Semester löschen",
            befehl = lambda: self.steuerung.semester_loeschen(semester)
        )
        loeschen.grid(row = 3, column = 1, sticky = "e", pady = (6, 0))
# ======================================================================================================================================================


# ======================================================================================================================================================
    def binde_semester_auswahl(
            self,
            widgets: list[tk.Misc],
            semester: Semester
    ) -> None:
        """Bindet die Auswahl nur an die übergebenen weißen Informationswidgets."""

        for widget in widgets:
            widget.bind(
                "<Button-1>",
                lambda _ereignis, aktuelles_semester = semester: self.steuerung.semester_auswaehlen(
                    aktuelles_semester
                )
            )
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_semester_kursbutton(
            self,
            parent: tk.Misc,
            semester: Semester,
            kurs: Kurs
    ) -> None:
        """Erzeugt einen kleinen Kursbutton innerhalb einer Semesterkarte."""

        farbe = self.elemente.kurs_farbe(kurs.status, kurs.ist_nicht_bestanden())

        if kurs.status == KursStatus.ABGESCHLOSSEN and kurs.note is not None:
            text = f"{kurs.note:.1f}"
        else:
            text = "•"

        button = tk.Button(
            parent,
            text = text,
            font = ("Arial", 9, "bold"),
            foreground = "white",
            background = farbe,
            activebackground = farbe,
            activeforeground = "white",
            borderwidth = 0,
            cursor = "hand2",
            width = 4,
            command = lambda: self.steuerung.semester_kurs_auswaehlen(semester, kurs)
        )
        button.pack(side = "left", padx = (0, 5))
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_semester_anlegen_karte(self, parent: tk.Misc) -> tk.Frame:
        """Erstellt die Anlegekarte, solange noch Semester angelegt werden dürfen."""

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
        plus.pack(pady = (22, 2))

        text = tk.Label(
            karte,
            text = "Neues Semester anlegen",
            font = ("Arial", 11),
            foreground = FARBE_TEXT,
            background = FARBE_KARTE,
            cursor = "hand2"
        )
        text.pack()

        max_text = tk.Label(
            karte,
            text = f"Maximal {self.anwendung.studiengang.berechne_max_semester()} Semester",
            font = ("Arial", 9),
            foreground = FARBE_TEXT_GRAU,
            background = FARBE_KARTE,
            cursor = "hand2"
        )
        max_text.pack(pady = (5, 0))

        self.elemente.mache_widget_klickbar(karte, self.steuerung.semester_anlegen)

        return karte
# ======================================================================================================================================================


# ======================================================================================================================================================
