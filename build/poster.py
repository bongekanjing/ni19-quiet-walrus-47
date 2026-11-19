#!/usr/bin/env python3
"""Build build/poster.html - a newspaper front page for 19 November 2026.

Story data lives inline below, and so does the coastline: COAST is Natural
Earth 1:110m land, reduced to 30 rings and 606 points with Douglas-Peucker,
carried as "lon,lat lon,lat ..." groups split by ";". Nothing is fetched at
build time.

Counts are stated on the page and are true: 3 leads + 36 briefs = 39 stories,
plus 8 market quotes.
"""

import html
import pathlib

PAPER = "THE WORLD TODAY"
DATE_LINE = "THURSDAY, 19 NOVEMBER 2026"
STRAP = "Summits, strikes and storms"

LEADS = [
    {
        "kicker": "APEC \u00b7 SHENZHEN",
        "head": "Trump, Xi and Putin meet three-way for the first time",
        "deck": (
            "The US, Chinese and Russian presidents sit down in Shenzhen on Thursday "
            "after Trump's separate talks with Xi. Iran, Ukraine and AI head an agenda "
            "that is expected to yield little."
        ),
    },
    {
        "kicker": "GULF \u00b7 IRAN",
        "head": "Iran hits a US base in Kuwait; Centcom says no Americans hurt",
        "deck": (
            "Iran said its drones struck Patriot batteries and launch platforms at Ali "
            "Al-Salem air base, retaliation for a US strike on Qeshm Island. Iran's army "
            "chief vowed a harsher response to any new attack."
        ),
    },
    {
        "kicker": "UKRAINE",
        "head": "Kyiv says one Trump-Putin-Xi meeting could end the war",
        "deck": (
            "Zelenskyy said the three leaders have the means to stop it. The Crimean "
            "Bridge was hit again, and the EU is weighing a 45 billion euro ($49.4bn) "
            "loan to cover Ukraine's 2027 budget gap."
        ),
    },
]

GRID = [
    ("US", "Peltola unseats Sullivan in Alaska, sealing a 56-44 Senate majority"),
    ("US", "Fed minutes: almost all saw further rate rises as likely"),
    ("MARKETS", "S&P 500 falls 1.0% to 7,340 as the dollar firms"),
    ("MARKETS", "Gold drops 2% to about $3,787, a one-year low"),
    ("MARKETS", "Brent holds near $92.52; 10-year Treasury above 5%"),
    ("TECH", "Nvidia revenue doubles to $115.8bn in first results without Huang"),
    ("TECH", "Anthropic prices its initial public offering"),
    ("TECH", "Waymo pulls robotaxis off US freeways after California ban"),
    ("HEALTH", "DR Congo's Ebola outbreak passes six months and 11,000 cases"),
    ("HEALTH", "WHO puts deaths in the Congo outbreak above 5,300"),
    ("CLIMATE", "COP31 draft calls for an immediate shift away from fossil fuels"),
    ("CLIMATE", "Ministers deadlocked in Antalya over who pays"),
    ("EUROPE", "Britain and the EU near a reset deal on food and youth mobility"),
    ("EUROPE", "Von der Leyen presses member states to back the Ukraine package"),
    ("UK", "Cambridge names \u201cHuman\u201d its word of the year, citing AI anxiety"),
    ("RUSSIA", "Moscow reports a record 1,336 drones downed in a single night"),
    ("MIDEAST", "Three tankers burn after striking mines in the Strait of Hormuz"),
    ("MIDEAST", "Houthis blame Saudi strikes for three deaths in Yemen"),
    ("AFRICA", "South Africa reprimands Nigeria's new high commissioner"),
    ("SOUTH ASIA", "Thailand rushes water to 20,000 homes as arsenic taints supplies"),
    ("SOUTH ASIA", "Arsenic traced to rare-earth mining across the Myanmar border"),
    ("EAST ASIA", "Beijing gives Japan's Takaichi a deliberately muted reception"),
    ("EAST ASIA", "South Korea offers $75,000 for each case of exam cheating"),
    ("SE ASIA", "Indonesia and China sign four deals worth nearly S$100bn"),
    ("LATAM", "US and Venezuela agree to restore military training and intelligence ties"),
    ("LATAM", "Milei and Lula take their feud onto the world stage"),
    ("AMERICAS", "Trump asks the Supreme Court to let Venezuelan deportations resume"),
    ("US", "Florida pastor convicted over Haiti's president's assassination"),
    ("SPORT", "India bowl first in Wellington; New Zealand 60-4 at lunch"),
    ("SPORT", "Bumrah strikes twice as Latham falls for a duck"),
    ("SPORT", "Pochettino begins work as Manchester United manager"),
    ("SOUTH ASIA", "Cyclone Akvan tracks toward Andhra Pradesh, landfall due Friday"),
    ("EUROPE", "Magnitude 5.7 quake shakes Romania's Vrancea region"),
    ("DIPLOMACY", "Zelenskyy urges Beijing and Washington to press Moscow"),
    ("ENERGY", "Equinor says a cyberattack hit its IT systems, output unaffected"),
    ("PACIFIC", "Albanese and Carney stand with Putin for the APEC group photo"),
]

TICKER = [
    ("S&P 500", "7,340", "\u22121.0%"),
    ("Nasdaq", "24,328", "\u22120.7%"),
    ("Dow", "50,759", "\u22121.6%"),
    ("Brent", "$92.52", "\u22120.7%"),
    ("Gold", "$3,787", "\u22122.0%"),
    ("Bitcoin", "$64,300", "\u22120.8%"),
    ("WTI", "$88.40", "\u22120.6%"),
    ("10-yr UST", "5.02%", "+0.03"),
]

DOTS = [
    ("Washington", -77.0, 38.9),
    ("Brasilia", -47.9, -15.8),
    ("Brussels", 4.4, 50.8),
    ("London", -0.1, 51.5),
    ("Kyiv", 30.5, 50.5),
    ("Moscow", 37.6, 55.8),
    ("Tehran", 51.4, 35.7),
    ("Kuwait", 47.9, 29.4),
    ("Nairobi", 36.8, -1.3),
    ("New Delhi", 77.2, 28.6),
    ("Bangkok", 100.5, 13.8),
    ("Beijing", 116.4, 39.9),
    ("Tokyo", 139.7, 35.7),
    ("Sydney", 151.2, -33.9),
]

# Natural Earth 1:110m land: 30 rings, 606 points, as "lon,lat" pairs split by ";".
COAST = (
    "-45,-78 -43,-80 -54,-81 -45,-78;-68,-71 -71,-73 -75,-72 -70,-69 -68,-71;-59,-64 -66,-68 -62,-71 "
    "-61,-74 -71,-77 -77,-77 -74,-78 -78,-79 -58,-83 -29,-80 -36,-79 -35,-78 -18,-75 -7,-71 27,-70 34"
    ",-69 39,-70 55,-66 61,-68 69,-68 68,-72 70,-72 88,-66 96,-67 103,-66 106,-67 114,-66 120,-67 135"
    ",-65 137,-67 145,-67 171,-72 164,-76 167,-79 162,-79 160,-81 180,-85 180,-90 -180,-90 -179,-84 -"
    "143,-85 -154,-84 -153,-82 -157,-81 -146,-80 -155,-79 -158,-77 -114,-74 -101,-75 -104,-73 -75,-74"
    " -67,-72 -68,-67 -59,-64;-68,-54 -65,-55 -69,-55 -75,-53 -68,-54;173,-41 174,-41 173,-44 169,-47"
    " 167,-46 173,-41;175,-36 179,-38 175,-42 173,-35 175,-36;50,-14 47,-25 44,-25 44,-16 49,-12 50,-"
    "14;144,-14 153,-26 153,-32 150,-37 146,-39 141,-38 138,-34 137,-35 138,-33 136,-35 131,-31 118,-"
    "35 115,-34 116,-32 113,-26 114,-22 121,-20 126,-14 130,-15 132,-11 136,-12 136,-15 140,-18 142,-"
    "11 144,-14;134,-1 135,-3 138,-2 145,-4 151,-11 145,-8 143,-9 138,-8 138,-5 133,-4 132,-3 134,-2 "
    "131,-1 134,-1;125,1 120,0 121,-1 123,-1 122,-2 123,-5 121,-3 119,-5 120,1 125,1;106,-6 103,-4 95"
    ",5 104,0 106,-3 106,-6;118,2 119,1 116,-4 110,-3 109,0 110,2 117,7 119,5 118,2;141,37 140,35 136"
    ",33 131,34 132,33 130,31 129,33 139,38 140,41 142,40 141,37;-56,51 -53,49 -53,47 -59,48 -56,51;-"
    "3,59 -3,56 2,53 1,51 -5,50 -3,51 -5,52 -5,53 -3,54 -6,57 -3,59;-15,66 -14,65 -19,63 -24,66 -15,6"
    "6;-175,67 -170,66 -173,64 -179,66 -180,65 -180,69 -175,67;-91,69 -87,67 -86,70 -83,70 -81,68 -93"
    ",62 -95,59 -92,57 -82,55 -80,51 -79,53 -80,55 -77,57 -79,59 -78,62 -74,62 -70,61 -68,58 -65,60 -"
    "56,52 -60,50 -66,50 -71,47 -65,49 -64,46 -60,46 -65,44 -66,44 -64,45 -67,45 -71,43 -70,42 -76,39"
    " -76,37 -76,39 -76,36 -81,31 -80,25 -84,30 -97,28 -98,22 -96,19 -92,19 -90,21 -87,22 -89,16 -83,"
    "15 -84,11 -81,9 -77,9 -72,12 -72,9 -70,12 -68,11 -62,11 -57,6 -51,4 -50,0 -40,-3 -36,-5 -35,-7 -"
    "39,-13 -41,-22 -48,-25 -54,-34 -58,-34 -57,-37 -65,-41 -63,-43 -67,-46 -66,-48 -69,-51 -68,-52 -"
    "71,-54 -75,-52 -76,-49 -74,-47 -76,-47 -73,-42 -74,-43 -70,-20 -76,-15 -81,-6 -80,-3 -81,-1 -77,"
    "4 -78,8 -81,7 -86,10 -87,13 -104,18 -114,32 -115,30 -109,23 -112,25 -117,33 -121,35 -124,40 -125"
    ",48 -123,47 -123,49 -127,51 -134,58 -147,61 -152,59 -151,61 -158,56 -165,54 -157,59 -162,59 -166"
    ",62 -161,65 -168,66 -162,66 -167,68 -157,71 -137,69 -128,70 -109,67 -106,69 -96,67 -94,69 -96,70"
    " -95,72 -91,69;-114,73 -108,72 -108,73 -107,73 -101,70 -116,69 -117,70 -112,70 -119,72 -114,73;-"
    "87,73 -72,72 -68,70 -67,69 -69,69 -62,67 -64,65 -68,66 -65,63 -69,64 -66,62 -78,64 -74,65 -73,68"
    " -79,70 -89,70 -90,72 -87,73;-120,71 -126,72 -124,74 -125,74 -118,74 -116,73 -120,71;-108,76 -10"
    "6,75 -118,75 -108,76;58,71 52,71 56,75 69,77 58,74 55,72 58,71;-95,77 -80,75 -92,75 -97,77 -95,7"
    "7;107,77 114,76 109,74 127,74 131,71 140,71 140,73 161,69 179,69 180,69 180,65 177,65 179,63 170"
    ",60 164,60 162,55 157,51 156,57 164,63 160,61 157,61 155,59 142,59 135,55 140,54 141,52 138,46 1"
    "28,40 129,35 126,34 125,40 121,39 122,41 118,39 119,37 122,37 119,35 122,32 122,28 116,23 110,20"
    " 109,22 106,20 109,13 105,9 100,13 99,9 103,6 104,1 101,3 98,8 97,17 94,16 91,23 87,21 80,16 80,"
    "10 78,8 73,21 70,21 66,25 57,26 48,30 52,24 56,26 60,22 55,17 43,13 43,17 35,30 34,28 32,30 37,1"
    "9 43,12 45,10 51,12 51,11 48,4 39,-5 41,-15 35,-20 36,-24 33,-26 32,-29 26,-34 18,-34 12,-18 14,"
    "-11 9,-1 9,4 4,6 -9,5 -17,12 -17,22 -6,36 10,37 11,37 10,34 19,30 22,33 34,31 36,37 28,37 26,39 "
    "34,42 42,42 37,45 39,47 35,46 36,45 34,44 31,47 28,43 29,41 23,40 24,38 22,36 20,42 13,46 13,44 "
    "18,40 17,40 16,38 9,44 3,43 -2,37 -9,37 -9,43 -1,44 -1,46 -5,49 8,54 9,57 11,58 10,55 11,54 20,5"
    "4 22,57 24,57 23,59 29,60 21,61 22,63 25,65 22,66 18,63 17,61 19,60 16,56 13,55 10,59 6,59 5,62 "
    "15,68 25,71 40,68 40,66 33,67 37,64 37,65 44,66 43,69 46,68 46,67 54,69 60,68 61,70 69,68 67,71 "
    "73,73 74,68 72,66 75,68 73,71 75,73 76,71 82,72 81,74 87,75 107,77;18,80 22,79 16,77 10,80 18,80"
    ";100,79 91,80 96,81 100,79;-87,80 -91,78 -97,80 -92,81 -87,80;-68,83 -62,82 -77,79 -75,79 -81,76"
    " -89,76 -88,78 -85,78 -88,78 -85,79 -87,80 -82,80 -92,82 -68,83;-27,84 -21,83 -31,82 -12,81 -20,"
    "80 -18,80 -20,79 -18,77 -22,77 -19,74 -25,72 -22,71 -26,71 -26,70 -22,70 -40,65 -43,60 -48,61 -5"
    "2,64 -54,67 -51,70 -55,70 -51,71 -56,72 -55,73 -59,76 -69,76 -71,77 -67,77 -73,78 -66,79 -68,80 "
    "-63,82 -27,84"
)

HERE = pathlib.Path(__file__).resolve().parent
CSS_PATH = HERE / "poster.css"
OUT_PATH = HERE / "poster.html"

STORIES = len(LEADS) + len(GRID)
QUOTES = len(TICKER)
EDITION = "{} stories from every region \u00b7 {} market quotes".format(STORIES, QUOTES)

MAP_W, MAP_H = 880, 92
LAT_TOP, LAT_BOT = 78.0, -58.0


def _rings():
    out = []
    for group in COAST.split(";"):
        pts = []
        for pair in group.split():
            lon, lat = pair.split(",")
            pts.append((int(lon), int(lat)))
        if len(pts) >= 3:
            out.append(pts)
    return out


def _px(lon, lat):
    x = (lon + 180.0) * (MAP_W / 360.0)
    y = (LAT_TOP - lat) * (MAP_H / (LAT_TOP - LAT_BOT))
    return round(x, 1), round(y, 1)


def _map_svg():
    land = []
    for ring in _rings():
        pts = " ".join("{},{}".format(*_px(lon, lat)) for lon, lat in ring)
        land.append('<polygon points="{}"/>'.format(pts))

    dots = []
    for name, lon, lat in DOTS:
        x, y = _px(lon, lat)
        dots.append('<circle cx="{}" cy="{}" r="2.6"/>'.format(x, y))

    return (
        '  <section class="mapband">\n'
        '    <div class="maplabel">Where the<br>day happened</div>\n'
        '    <svg viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet" '
        'role="img" aria-label="World map marking the day\u2019s datelines">\n'
        '      <g class="land">{land}</g>\n'
        '      <g class="pins">{dots}</g>\n'
        "    </svg>\n"
        "  </section>\n"
    ).format(w=MAP_W, h=MAP_H, land="".join(land), dots="".join(dots))


def _lead_html(lead):
    return (
        '  <article class="lead">\n'
        '    <div class="kicker">{kicker}</div>\n'
        '    <h2>{head}</h2>\n'
        '    <p class="deck">{deck}</p>\n'
        "  </article>\n"
    ).format(
        kicker=html.escape(lead["kicker"]),
        head=html.escape(lead["head"]),
        deck=html.escape(lead["deck"]),
    )


def _tick_html(name, val, chg):
    return '  <div class="tick"><b>{}</b><span>{}</span><em>{}</em></div>\n'.format(
        html.escape(name), html.escape(val), html.escape(chg)
    )


def _cell_html(tag, headline):
    return '  <div class="cell"><div class="tag">{}</div><h3>{}</h3></div>\n'.format(
        html.escape(tag), html.escape(headline)
    )


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
