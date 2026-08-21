# Dieses Modul: Sammelt zentral verwendete fachliche und technische Konstanten.
"""Zentrale Konstanten des Studien-Dashboards.

Die Datei enthält sowohl fachliche Grenzwerte als auch feste Farbwerte der
Benutzeroberfläche. Dadurch liegen unveränderliche Werte an einer gemeinsamen,
leicht auffindbaren Stelle und müssen nicht in mehreren Modulen wiederholt werden.
"""

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# Fachliche Grenzwerte
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
ECTS_PRO_SEMESTER = 30
MIN_ECTS_PRO_KURS = 5
MIN_GESAMT_ECTS = 90
MAX_GESAMT_ECTS = 360

MIN_SEMESTER = MIN_GESAMT_ECTS // ECTS_PRO_SEMESTER
MAX_SEMESTER = MAX_GESAMT_ECTS // ECTS_PRO_SEMESTER
MAX_KURSE_PRO_SEMESTER = ECTS_PRO_SEMESTER // MIN_ECTS_PRO_KURS

ZULAESSIGE_KURSNOTEN = (
    1.0,
    1.3,
    1.7,
    2.0,
    2.3,
    2.7,
    3.0,
    3.3,
    3.7,
    4.0,
    5.0,
)

ZULAESSIGE_BESTEHENSNOTEN = (
    4.0,
    3.7,
    3.3,
    3.0,
    2.7,
    2.3,
    2.0,
    1.7,
    1.3,
    1.0,
)
# ======================================================================================================================================================


# ------------------------------------------------------------------------------------------------------------------------------------------------------
# Feste Farbwerte der grafischen Oberfläche
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================================================
FARBE_HINTERGRUND = "#f4f6f9"
FARBE_KARTE = "#ffffff"
FARBE_RAND = "#d8dee8"
FARBE_TEXT = "#14213d"
FARBE_TEXT_GRAU = "#667085"
FARBE_GRAU = "#98a2b3"
FARBE_GELB = "#fdb515"
FARBE_GRUEN = "#26a65b"
FARBE_BLAU = "#3b82f6"
FARBE_ROT = "#dc2626"
FARBE_HELLBLAU = "#dbeafe"
FARBE_PROGRESS_HINTERGRUND = "#e4e7ec"
# ======================================================================================================================================================
