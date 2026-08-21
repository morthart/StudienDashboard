# Dieses Modul: Berechnet und zeigt Kennzahlen, Noten und Gesamtfortschritt im Kopfbereich.
import tkinter as tk
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from konstanten import ZULAESSIGE_BESTEHENSNOTEN
# ------------------------------------------------------------------------------------------------------------------------------------------------------
from konstanten import (
    FARBE_HINTERGRUND,
    FARBE_KARTE,
    FARBE_TEXT,
    FARBE_TEXT_GRAU,
    FARBE_GRUEN,
    FARBE_ROT,
    FARBE_PROGRESS_HINTERGRUND
)
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
# Klasse DashboardKopfbereich: Zeigt Studiengang, Gesamtfortschritt und die drei Notenkennzahlen an.
class DashboardKopfbereich:
    """Zeigt Studiengang, Gesamtfortschritt und die drei Notenkennzahlen an."""


    def __init__(self, anwendung, elemente) -> None:
        """Erhält den Anwendungszustand und die gemeinsamen Dashboardelemente."""

        self.anwendung = anwendung
        self.elemente = elemente
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_kopfbereich(self, parent: tk.Misc) -> None:
        """Zeigt den Studiengang, den Gesamtfortschritt und die drei Notenkennzahlen an."""

        titelbereich = tk.Frame(parent, background = FARBE_HINTERGRUND)
        titelbereich.pack(side = "left", fill = "both", expand = True)

        if self.anwendung.studiengang is None:
            name = "Kein Studiengang ausgewählt"
        else:
            name = self.anwendung.studiengang.name

        # Im linken Kopfbereich wird bewusst nur der Name des Studiengangs angezeigt.
        # Gesamt-ECTS und maximale Semesterzahl lassen sich aus den Daten ableiten und
        # müssen deshalb nicht zusätzlich als Text wiederholt werden.
        name_label = tk.Label(
            titelbereich,
            text = name,
            font = ("Arial", 18, "bold"),
            foreground = FARBE_TEXT,
            background = FARBE_HINTERGRUND
        )
        name_label.pack(anchor = "w", pady = (24, 4))

        if self.anwendung.studiengang is None:
            hinweis_label = tk.Label(
                titelbereich,
                text = "Über Menü einen Studiengang anlegen oder wechseln",
                font = ("Arial", 10),
                foreground = FARBE_TEXT_GRAU,
                background = FARBE_HINTERGRUND
            )
            hinweis_label.pack(anchor = "w")

        kartenbereich = tk.Frame(parent, background = FARBE_HINTERGRUND)
        kartenbereich.pack(side = "right", anchor = "ne")

        self.baue_fortschrittskarte(kartenbereich)
        self.baue_notenkarte(kartenbereich, "Wunschnote", self.wert_wunschnote(), "Ziel", 1)
        self.baue_notenkarte(kartenbereich, "Notenschnitt", self.wert_notenschnitt(), "Momentan", 2)
        self.baue_notenkarte(kartenbereich, "Benötigter Schnitt", self.wert_benoetigter_schnitt(), "Zur Wunschnote", 3)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_fortschrittskarte(self, parent: tk.Misc) -> None:
        """Erstellt die breite Karte für den gesamten Studienfortschritt."""

        karte = self.elemente.erstelle_karte(parent, breite = 560, hoehe = 120)
        karte.grid(row = 0, column = 0, padx = 6)
        karte.grid_propagate(False)

        titel = tk.Label(
            karte,
            text = "Studienfortschritt - Gesammelte ECTS",
            font = ("Arial", 10, "bold"),
            foreground = FARBE_TEXT,
            background = FARBE_KARTE
        )
        titel.pack(anchor = "w", padx = 16, pady = (12, 6))

        erreicht, gesamt, prozent = self.berechne_fortschrittswerte()

        if self.anwendung.studiengang is not None:
            if self.anwendung.studiengang.hat_nicht_bestandenen_kurs():
                self.baue_studienstatus(
                    karte,
                    text = "Studium derzeit nicht erfolgreich",
                    farbe = FARBE_ROT
                )
                return

            if gesamt > 0 and erreicht >= gesamt:
                self.baue_studienstatus(
                    karte,
                    text = "Studium erfolgreich abgeschlossen",
                    farbe = FARBE_GRUEN
                )
                return

        self.zeichne_fortschrittsbalken(karte, prozent)
        self.baue_fortschrittsbeschriftung(karte, erreicht, gesamt)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_studienstatus(self, parent: tk.Misc, text: str, farbe: str) -> None:
        """Ersetzt den Fortschrittsbalken bei einem eindeutigen Studienstatus durch einen Hinweis."""

        status_label = tk.Label(
            parent,
            text = text,
            font = ("Arial", 15, "bold"),
            foreground = farbe,
            background = FARBE_KARTE
        )
        status_label.pack(expand = True, pady = (4, 18))
# ======================================================================================================================================================


# ======================================================================================================================================================
    def berechne_fortschrittswerte(self) -> tuple[int, int, float]:
        """Berechnet erreichte ECTS, Gesamt-ECTS und den Prozentwert für die Anzeige."""

        if self.anwendung.studiengang is None:
            return 0, 0, 0.0

        erreicht = self.anwendung.studiengang.berechne_erreichte_ects()
        gesamt = self.anwendung.studiengang.gesamt_ects

        if gesamt <= 0:
            return erreicht, gesamt, 0.0

        prozent = (erreicht / gesamt) * 100

        return erreicht, gesamt, prozent
# ======================================================================================================================================================


# ======================================================================================================================================================
    def zeichne_fortschrittsbalken(self, parent: tk.Misc, prozent: float) -> None:
        """Zeichnet den grünen Balken und setzt die Prozentzahl direkt in seine Mitte."""

        balken_breite = 528
        balken_hoehe = 22

        balken = tk.Canvas(
            parent,
            width = balken_breite,
            height = balken_hoehe,
            background = FARBE_PROGRESS_HINTERGRUND,
            highlightthickness = 0
        )
        balken.pack(padx = 16)

        anteil = prozent / 100

        if anteil < 0:
            anteil = 0

        if anteil > 1:
            anteil = 1

        gefuellte_pixel = balken_breite * anteil

        balken.create_rectangle(
            0,
            0,
            gefuellte_pixel,
            balken_hoehe,
            fill = FARBE_GRUEN,
            outline = ""
        )

        balken.create_text(
            balken_breite / 2,
            balken_hoehe / 2,
            text = f"{prozent:.1f} %",
            font = ("Arial", 9, "bold"),
            fill = FARBE_TEXT
        )
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_fortschrittsbeschriftung(
            self,
            parent: tk.Misc,
            erreicht: int,
            gesamt: int
    ) -> None:
        """Setzt die Werte 0, aktuell erreicht und Gesamt-ECTS unter den Balken."""

        beschriftung = tk.Frame(parent, background = FARBE_KARTE)
        beschriftung.pack(fill = "x", padx = 16, pady = (8, 0))

        beschriftung.columnconfigure(0, weight = 1)
        beschriftung.columnconfigure(1, weight = 1)
        beschriftung.columnconfigure(2, weight = 1)

        self.baue_fortschrittswert(
            beschriftung,
            text = "0",
            spalte = 0,
            ausrichtung = "w"
        )

        self.baue_fortschrittswert(
            beschriftung,
            text = str(erreicht),
            spalte = 1,
            ausrichtung = ""
        )

        gesamt_text = "-"

        if gesamt > 0:
            gesamt_text = str(gesamt)

        self.baue_fortschrittswert(
            beschriftung,
            text = gesamt_text,
            spalte = 2,
            ausrichtung = "e"
        )
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_fortschrittswert(
            self,
            parent: tk.Misc,
            text: str,
            spalte: int,
            ausrichtung: str
    ) -> None:
        """Baut einen einzelnen fett dargestellten Wert unter dem Fortschrittsbalken."""

        label = tk.Label(
            parent,
            text = text,
            font = ("Arial", 10, "bold"),
            foreground = FARBE_TEXT,
            background = FARBE_KARTE
        )

        if ausrichtung:
            label.grid(row = 0, column = spalte, sticky = ausrichtung)
        else:
            label.grid(row = 0, column = spalte)
# ======================================================================================================================================================


# ======================================================================================================================================================
    def baue_notenkarte(
            self,
            parent: tk.Misc,
            titel: str,
            wert: str,
            untertitel: str,
            spalte: int
    ) -> None:
        """Erstellt eine einheitliche Kennzahlenkarte für Notenwerte."""

        karte = self.elemente.erstelle_karte(parent, breite = 145, hoehe = 120)
        karte.grid(row = 0, column = spalte, padx = 6)
        karte.grid_propagate(False)

        titel_label = tk.Label(
            karte,
            text = titel,
            font = ("Arial", 10, "bold"),
            foreground = FARBE_TEXT,
            background = FARBE_KARTE
        )
        titel_label.pack(pady = (14, 6))

        schriftgroesse = 22

        if len(wert) > 8:
            schriftgroesse = 12

        wert_label = tk.Label(
            karte,
            text = wert,
            font = ("Arial", schriftgroesse, "bold"),
            foreground = FARBE_TEXT,
            background = FARBE_KARTE
        )
        wert_label.pack()

        untertitel_label = tk.Label(
            karte,
            text = untertitel,
            font = ("Arial", 9),
            foreground = FARBE_TEXT_GRAU,
            background = FARBE_KARTE
        )
        untertitel_label.pack(pady = (4, 0))
# ======================================================================================================================================================


# ======================================================================================================================================================
    def wert_wunschnote(self) -> str:
        """Formatiert die Wunschnote für die Kennzahlenkarte."""

        if self.anwendung.studiengang is None:
            return "-"

        return f"{self.anwendung.studiengang.wunschnote:.1f}"
# ======================================================================================================================================================


# ======================================================================================================================================================
    def wert_notenschnitt(self) -> str:
        """Formatiert den aktuellen Notenschnitt für die Kennzahlenkarte."""

        if self.anwendung.studiengang is None:
            return "-"

        notenschnitt = self.anwendung.studiengang.berechne_notenschnitt()

        if notenschnitt is None:
            return "-"

        return f"{notenschnitt:.1f}"
# ======================================================================================================================================================


# ======================================================================================================================================================
    def wert_benoetigter_schnitt(self) -> str:
        """Gibt die benötigte zulässige Notenstufe für die Anzeige zurück."""

        if self.anwendung.studiengang is None:
            return "-"

        benoetigter_schnitt = self.anwendung.studiengang.berechne_benoetigten_schnitt()

        if benoetigter_schnitt is None:
            return "-"

        if benoetigter_schnitt < 1.0:
            return "Nicht mehr\nerreichbar"

        if benoetigter_schnitt >= 4.0:
            return "Einfach nur\nbestehen :)"

        # Die vorhandenen Elemente werden nacheinander ausgewertet, damit aus ihrem aktuellen Zustand das Ergebnis ermittelt werden kann.
        for note in ZULAESSIGE_BESTEHENSNOTEN:
            if benoetigter_schnitt >= note:
                return f"{note:.1f}"

        return "Nicht mehr\nerreichbar"
# ======================================================================================================================================================
