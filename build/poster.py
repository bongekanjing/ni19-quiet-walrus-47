#!/usr/bin/env python3
"""Render build/poster.html: a newspaper front page for Thursday 19 November 2026.

Every story is held inline in this file, so the counts printed on the page are
computed from the data and cannot drift from what is actually printed:

    3 leads + 36 briefs = 39 editorial stories, plus 8 market quotes.

Layout is fixed at 1024 wide. build/render.sh screenshots 1024x1200 and crops
the top 1024 rows, so the sheet is laid out to run its ink off the bottom of
that crop rather than stopping short of it.
"""

import html
import pathlib

DATE_LINE = "THURSDAY, 19 NOVEMBER 2026"
PAPER = "THE WORLD TODAY"
STRAP = "Summits, strikes and storms"

# --- three leads: kicker, headline, three-sentence deck --------------------
LEADS = [
    {
        "kicker": "APEC \u00b7 SHENZHEN",
        "head": "Trump, Xi and Putin meet three-way for the first time",
        "deck": (
            "The US, Chinese and Russian presidents sit down in Shenzhen on "
            "Thursday after Trump's separate talks with Xi. Iran, Ukraine, "
            "strategic stability and AI lead an agenda with low expectations of "
            "a deal."
        ),
    },
    {
        "kicker": "GULF \u00b7 KUWAIT",
        "head": "Iran hits a US base in Kuwait; Centcom says no Americans hurt",
        "deck": (
            "Tehran said its drones struck Patriot batteries and launch platforms "
            "at Ali Al-Salem air base, retaliation for a US strike on Qeshm "
            "Island. Kuwait said its air defences engaged hostile drones, and US "
            "Central Command said no American personnel were wounded."
        ),
    },
    {
        "kicker": "UKRAINE",
        "head": "Kyiv says one Trump-Putin-Xi meeting could end the war",
        "deck": (
            "Zelenskyy said the three leaders have the means to stop it, and his "
            "foreign minister urged Beijing and Washington to press Moscow. The "
            "Crimean Bridge was hit again, and the EU proposed a 45 billion euro "
            "($49.4bn) loan for 2027."
        ),
    },
]

# --- 36 briefs: region tag + one-line headline -----------------------------
# Tags are drawn from a fixed vocabulary; each names the region the headline
# is actually about. 4 columns x 9 rows.
GRID = [
    ("US", "Peltola unseats Sullivan in Alaska, sealing a 56-44 Senate majority"),
    ("US", "Fed minutes: almost all saw further rate rises as likely"),
    ("US", "Fed puts AI at the centre of the inflation debate"),
    ("US", "Waymo pulls robotaxis off US freeways after California ban"),

    ("LATAM", "US and Venezuela agree to restore military training and intelligence ties"),
    ("LATAM", "Milei and Lula take their feud onto the world stage"),
    ("US", "Trump asks the Supreme Court to let Venezuelan deportations resume"),
    ("EUROPE", "Britain and the EU signal a reset deal on food and youth mobility"),

    ("EUROPE", "Von der Leyen presses member states to back the Ukraine package at a Brussels summit"),
    ("EUROPE", "Magnitude 5.7 quake shakes Romania's Vrancea region"),
    ("EUROPE", "Berlin and London reject US criticism of Kyiv deep strikes"),
    ("UK", "Cambridge names \u201cHuman\u201d its word of the year, citing AI anxiety"),

    ("RUSSIA", "Moscow reports a record 1,336 drones downed in a single night"),
    ("MIDEAST", "Three tankers burn after striking mines in the Strait of Hormuz"),
    ("MIDEAST", "Houthis blame Saudi strikes for three deaths in Yemen"),
    ("AFRICA", "South Africa reprimands Nigeria's new high commissioner"),

    ("AFRICA", "Senegal's President Faye expelled from the ruling party"),
    ("HEALTH", "DR Congo's Ebola outbreak passes six months and 11,000 cases"),
    ("HEALTH", "WHO puts deaths in the Congo outbreak above 5,300"),
    ("SOUTH ASIA", "Cyclone Akvan tracks toward Andhra Pradesh, landfall due Friday"),

    ("SOUTH ASIA", "Akvan to bring 120-130 km/h winds, gusting to 145"),
    ("EAST ASIA", "Beijing gives Japan's Takaichi a deliberately muted reception"),
    ("EAST ASIA", "South Korea offers $75,000 for each case of exam cheating"),
    ("SE ASIA", "Arsenic traced to rare-earth mining across the Myanmar border"),

    ("SE ASIA", "Thailand rushes water to 20,000 homes as arsenic taints supplies"),
    ("SE ASIA", "Indonesia and China sign four deals worth nearly S$100bn"),
    ("TECH", "Nvidia revenue doubles to $115.8bn in first results without Huang"),
    ("TECH", "Anthropic prices its initial public offering"),

    ("PACIFIC", "Albanese and Carney stand with Putin for the APEC group photo"),
    ("PACIFIC", "Fiji declares a national disaster as El Nino drought bites"),
    ("CLIMATE", "COP31 draft calls for an immediate shift away from fossil fuels"),
    ("CLIMATE", "Ministers deadlocked in Antalya over who pays"),

    ("SPORT", "India bowl first in Wellington; New Zealand 60-4 at lunch"),
    ("MARKETS", "S&P 500 falls 1.0% to 7,340 as the dollar firms"),
    ("MARKETS", "Gold drops 2% to about $3,787, a one-year low"),
    ("MARKETS", "Brent holds near $92.50; 10-year Treasury above 5%"),
]

# --- market tape: label, level, move. One value per figure, page-wide. -----
TICKER = [
    ("S&P 500", "7,340", "\u22121.0%"),
    ("Nasdaq", "24,328", "\u22120.7%"),
    ("Dow", "50,759", "\u22121.6%"),
    ("Brent", "$92.50", "\u22120.7%"),
    ("Gold", "$3,787", "\u22122.0%"),
    ("Bitcoin", "$64,300", "\u22120.8%"),
    ("WTI", "$88.40", "\u22120.6%"),
    ("10-yr UST", "5.02%", "+0.03"),
]

# --- dateline dots for the map band: lat, lon ------------------------------
DOTS = [
    (38.9, -77.0),     # Washington
    (-15.8, -47.9),    # Brasilia
    (50.8, 4.4),       # Brussels
    (51.5, -0.1),      # London
    (50.4, 30.5),      # Kyiv
    (55.8, 37.6),      # Moscow
    (35.7, 51.4),      # Tehran
    (29.4, 48.0),      # Kuwait
    (-1.3, 36.8),      # Nairobi
    (28.6, 77.2),      # New Delhi
    (13.8, 100.5),     # Bangkok
    (39.9, 116.4),     # Beijing
    (35.7, 139.7),     # Tokyo
    (-33.9, 151.2),    # Sydney
]

# Seven crude landmasses in (lon, lat). Flat, no gradients: enough to read as
# a world at 870px wide without any external asset.
LAND = [
    # North America
    [(-168, 65), (-158, 71), (-130, 70), (-100, 72), (-80, 70), (-64, 60),
     (-56, 48), (-70, 44), (-76, 36), (-81, 25), (-97, 26), (-105, 20),
     (-115, 30), (-124, 40), (-128, 50), (-140, 58), (-160, 58)],
    # South America
    [(-80, 9), (-62, 11), (-50, 0), (-35, -6), (-39, -16), (-48, -25),
     (-58, -34), (-66, -45), (-72, -52), (-75, -45), (-70, -30), (-70, -18),
     (-78, -4)],
    # Europe
    [(-9, 37), (-9, 44), (-2, 49), (4, 52), (9, 55), (12, 58), (20, 60),
     (25, 65), (30, 70), (40, 68), (40, 58), (40, 50), (35, 45), (28, 41),
     (20, 40), (13, 45), (3, 43), (-2, 38)],
    # Africa
    [(-17, 15), (-6, 5), (9, 4), (9, -2), (13, -8), (13, -18), (18, -28),
     (20, -34), (28, -33), (33, -26), (40, -16), (41, -4), (51, 12),
     (43, 12), (35, 22), (32, 31), (25, 32), (10, 37), (0, 36), (-10, 30)],
    # Asia
    [(35, 45), (45, 48), (55, 52), (60, 55), (70, 58), (80, 60), (90, 62),
     (105, 62), (120, 58), (135, 55), (145, 50), (140, 44), (130, 40),
     (122, 32), (120, 25), (110, 20), (105, 10), (100, 5), (97, 17),
     (92, 22), (88, 22), (80, 15), (72, 8), (68, 22), (60, 25), (52, 28),
     (45, 38), (38, 40)],
    # India
    [(68, 24), (72, 20), (77, 8), (80, 10), (88, 22), (92, 25), (85, 27),
     (78, 30), (70, 28)],
    # Australia
    [(114, -22), (122, -18), (130, -12), (138, -12), (144, -14), (147, -19),
     (153, -25), (150, -37), (141, -38), (130, -32), (118, -34)],
]

HERE = pathlib.Path(__file__).resolve().parent
CSS_PATH = HERE / "poster.css"
OUT_PATH = HERE / "poster.html"

STORIES = len(LEADS) + len(GRID)
QUOTES = len(TICKER)
EDITION = "{} stories from every region \u00b7 {} market quotes".format(
    STORIES, QUOTES
)

MAP_W, MAP_VB_H = 980, 90
LAT_TOP, LAT_BOT = 78.0, -58.0


def _xy(lat, lon):
    """Equirectangular projection into the 980x90 map viewBox."""
    x = (lon + 180.0) / 360.0 * MAP_W
    y = (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_VB_H
    return round(x, 1), round(y, 1)


def _map_svg():
    """Inline world map: seven muted landmasses, today's datelines in red."""
    blobs = []
    for poly in LAND:
        pts = " ".join("{},{}".format(*_xy(lat, lon)) for lon, lat in poly)
        blobs.append('<polygon points="{}"/>'.format(pts))

    dots = "".join(
        '<circle cx="{}" cy="{}" r="2.9"/>'.format(*_xy(lat, lon))
        for lat, lon in DOTS
    )

    return (
        '<section class="mapband">\n'
        '    <div class="maplabel">WHERE THE DAY HAPPENED</div>\n'
        '    <svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" '
        'role="img" aria-label="Stylised world map marking the day\u2019s '
        'datelines">\n'
        '      <g class="land">{land}</g>\n'
        '      <g class="pins">{dots}</g>\n'
        "    </svg>\n"
        "  </section>\n"
    ).format(w=MAP_W, h=MAP_VB_H, land="".join(blobs), dots=dots)


def _lead_html(lead):
    return (
        '    <article class="lead">\n'
        '      <div class="kicker">{kicker}</div>\n'
        '      <h2>{head}</h2>\n'
        '      <p class="deck">{deck}</p>\n'
        "    </article>\n"
    ).format(
        kicker=html.escape(lead["kicker"]),
        head=html.escape(lead["head"]),
        deck=html.escape(lead["deck"]),
    )


def _tick_html(name, val, chg):
    return (
        '    <div class="tick"><b>{}</b><span>{}</span><em>{}</em></div>\n'
    ).format(html.escape(name), html.escape(val), html.escape(chg))


def _cell_html(tag, headline):
    return (
        '    <div class="cell"><div class="tag">{}</div>'
        "<h3>{}</h3></div>\n"
    ).format(html.escape(tag), html.escape(headline))


def build():
    css = CSS_PATH.read_text(encoding="utf-8")
    parts = [
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n",
        "<title>{} \u2014 19 November 2026</title>\n".format(PAPER),
        "<style>\n" + css + "</style>\n</head>\n<body>\n",
        '<div class="sheet">\n',
        '  <header class="masthead">\n',
        '    <div class="rule thin"></div>\n',
        '    <span class="paper">{}</span>\n'.format(PAPER),
        '    <span class="edition">{}</span>\n'.format(html.escape(EDITION)),
        '    <div class="rule thick"></div>\n',
        '    <div class="dateline"><span class="date">{}</span>'
        '<span class="strap">{}</span></div>\n'.format(
            html.escape(DATE_LINE), html.escape(STRAP)
        ),
        "  </header>\n",
        '  <section class="leads">\n',
    ]
    for lead in LEADS:
        parts.append(_lead_html(lead))
    parts.append("  </section>\n")

    parts.append('  <section class="ticker">\n')
    for name, val, chg in TICKER:
        parts.append(_tick_html(name, val, chg))
    parts.append("  </section>\n")

    parts.append(_map_svg())

    parts.append('  <section class="grid">\n')
    for tag, headline in GRID:
        parts.append(_cell_html(tag, headline))
    parts.append("  </section>\n")

    parts.append(
        '  <footer class="foot">'
        "<span>Compiled from AP, Reuters, CNBC, CNA, Al Jazeera and UN News. "
        "Contested claims are attributed.</span>"
        "<span>{}</span></footer>\n".format(html.escape(DATE_LINE))
    )
    parts.append("</div>\n</body>\n</html>\n")

    OUT_PATH.write_text("".join(parts), encoding="utf-8")
    print(
        "poster.html: {} leads + {} briefs = {} stories, + {} market quotes".format(
            len(LEADS), len(GRID), STORIES, QUOTES
        )
    )


if __name__ == "__main__":
    build()
