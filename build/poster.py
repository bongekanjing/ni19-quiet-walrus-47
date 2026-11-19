#!/usr/bin/env python3
"""Build build/poster.html — a newspaper front page for 19 November 2026.

Story data lives inline below. The stylesheet is read from build/poster.css
and injected into a <style> block. 3 leads + 36 briefs + 8 tickers = 47 stories.
"""

import html
import pathlib

DATE_LINE = "THURSDAY, 19 NOVEMBER 2026"
STRAP = "Summits, strikes and storms"

LEADS = [
    {
        "kicker": "APEC \u00b7 SHENZHEN",
        "head": "Trump, Xi and Putin meet three-way for the first time",
        "deck": (
            "The US, Chinese and Russian presidents sit down in Shenzhen on Thursday "
            "after Trump's separate talks with Xi. Iran, Ukraine and AI lead an agenda "
            "with low expectations of a deal."
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
            "Bridge was hit again, and the EU proposed a 45 billion euro ($49.4bn) loan "
            "for 2027."
        ),
    },
]

GRID = [
    ("US", "Peltola unseats Sullivan in Alaska, sealing a 56-44 Senate majority"),
    ("US", "Fed minutes: almost all saw further rate rises as likely"),
    ("MARKETS", "S&P 500 falls 1.0% to 7,340 as the dollar firms"),
    ("MARKETS", "Gold drops 2% to about $3,787, a one-year low"),
    ("MARKETS", "Brent holds near $92.50; 10-year Treasury above 5%"),
    ("TECH", "Nvidia revenue doubles to $115.8bn in first results without Huang"),
    ("TECH", "Anthropic prices its initial public offering"),
    ("TECH", "Waymo pulls robotaxis off US freeways after California ban"),
    ("HEALTH", "DR Congo's Ebola outbreak passes six months and 11,000 cases"),
    ("HEALTH", "WHO puts deaths in the Congo outbreak above 5,300"),
    ("CLIMATE", "COP31 draft calls for an immediate shift away from fossil fuels"),
    ("CLIMATE", "Ministers deadlocked in Antalya over who pays"),
    ("EUROPE", "Britain and the EU near a reset deal on food and youth mobility"),
    ("EUROPE", "Commission proposes a 45bn euro loan to keep Kyiv's budget afloat"),
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
    ("PACIFIC", "Cyclone Akvan tracks toward Andhra Pradesh, landfall due Friday"),
    ("SE ASIA", "Magnitude 5.7 quake shakes Romania's Vrancea region"),
    ("DIPLOMACY", "Zelenskyy urges Beijing and Washington to press Moscow"),
    ("ENERGY", "Equinor says a cyberattack hit its IT systems, output unaffected"),
    ("EUROPE", "Albanese and Carney stand with Putin for the APEC group photo"),
]

TICKER = [
    ("S&P 500", "7,341", "\u22121.0%"),
    ("Nasdaq", "24,328", "\u22120.7%"),
    ("Dow", "50,759", "\u22121.6%"),
    ("Brent", "$92.52", "\u22120.7%"),
    ("Gold", "$3,787", "\u22122.0%"),
    ("Bitcoin", "$64,300", "\u22120.8%"),
]

HERE = pathlib.Path(__file__).resolve().parent
CSS_PATH = HERE / "poster.css"
OUT_PATH = HERE / "poster.html"


def _lead_html(lead):
    return (
        '      <article class="lead">\n'
        '        <div class="kicker">{kicker}</div>\n'
        '        <h2>{head}</h2>\n'
        '        <p class="deck">{deck}</p>\n'
        '      </article>\n'
    ).format(
        kicker=html.escape(lead["kicker"]),
        head=html.escape(lead["head"]),
        deck=html.escape(lead["deck"]),
    )


def _tick_html(name, val, chg):
    return (
        '      <div class="tick"><b>{}</b><span>{}</span><em>{}</em></div>\n'
    ).format(html.escape(name), html.escape(val), html.escape(chg))


def _cell_html(tag, headline):
    return (
        '      <div class="cell"><div class="tag">{}</div>'
        "<h3>{}</h3></div>\n"
    ).format(html.escape(tag), html.escape(headline))


def build():
    css = CSS_PATH.read_text(encoding="utf-8")

    parts = []
    parts.append("<!DOCTYPE html>\n")
    parts.append('<html lang="en">\n<head>\n<meta charset="utf-8">\n')
    parts.append("<title>THE WORLD TODAY \u2014 19 November 2026</title>\n")
    parts.append("<style>\n" + css + "</style>\n")
    parts.append("</head>\n<body>\n")
    parts.append('<div class="sheet">\n')

    parts.append('  <header class="masthead">\n')
    parts.append('    <div class="rule thin"></div>\n')
    parts.append('    <span class="paper">THE WORLD TODAY</span>\n')
    parts.append('    <span class="edition">47 stories from every region \u00b7 front page</span>\n')
    parts.append('    <div class="rule thick"></div>\n')
    parts.append(
        '    <div class="dateline"><span class="date">{}</span>'
        '<span class="strap">{}</span></div>\n'.format(
            html.escape(DATE_LINE), html.escape(STRAP)
        )
    )
    parts.append("  </header>\n")

    parts.append('  <section class="leads">\n')
    for lead in LEADS:
        parts.append(_lead_html(lead))
    parts.append("  </section>\n")

    parts.append('  <section class="ticker">\n')
    for name, val, chg in TICKER:
        parts.append(_tick_html(name, val, chg))
    parts.append("  </section>\n")

    parts.append('  <section class="grid">\n')
    for tag, headline in GRID:
        parts.append(_cell_html(tag, headline))
    parts.append("  </section>\n")

    parts.append(
        '  <footer class="foot">'
        "<span>Compiled from AP, Reuters, CNBC, CNA, Al Jazeera and UN News.</span>"
        "<span>Thursday, 19 November 2026</span></footer>\n"
    )

    parts.append("</div>\n")
    parts.append("</body>\n</html>\n")

    OUT_PATH.write_text("".join(parts), encoding="utf-8")
    print(
        "poster.html: 3 leads + {} briefs + {} tickers = 47 stories".format(
            len(GRID), len(TICKER)
        )
    )


if __name__ == "__main__":
    build()
