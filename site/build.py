#!/usr/bin/env python3
"""Genererar alla sidor för nya nykael.se: python3 site/build.py

Samma uppbyggnad som Bloms El & Data: navbar, fotohero med överlappande bildkort,
växlande split-sektioner, bildkort, citat, bildremsa, mörk sektion, bildband och förtroenderad.
Gamla adresser (/, /foretaget/, /kontakta-oss/) finns kvar så att befintliga länkar fungerar.
All fakta kommer från nykael.se (startsida, Företaget, Kontakta oss och mediabiblioteket).
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE_URL = "https://nykael.se"

CO = {
    "name": "Nyberg & Karlsons Elektriska AB",
    "street": "Norra Ågatan 10",
    "zip": "416 64",
    "city": "Göteborg",
    "phone": "031-80 13 50",
    "tel": "+4631801350",
    "email": "mail@nykael.se",
    "founded": "1910",
}
MAPS = "https://www.google.com/maps/search/?api=1&query=Norra+%C3%85gatan+10%2C+416+64+G%C3%B6teborg"

# Projektledarna som de presenteras på nykael.se/kontakta-oss/
PEOPLE = [
    {"name": "Mikael Nyberg", "initials": "MN", "mobile": "0707-44 26 26", "tel": "+46707442626", "email": "mikael.nyberg@nykael.se"},
    {"name": "Reine Ekstorm", "initials": "RE", "mobile": "0705-61 74 65", "tel": "+46705617465", "email": "reine@nykael.se"},
]

ICON = {
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "form": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13.5 6.5l4 4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l5 5"/>',
}


def icon(name):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg>'


# Verksamhetsområden enligt nykael.se: i huvudsak servicearbeten åt industri, fastighetsförvaltning
# och butiker, men även en del nyproduktion och ombyggnader.
# Bilderna på områdena är CC0-bilder (se README), inte foton av företagets egna arbeten.
AREAS = [
    {"id": "service", "title": "Servicearbeten", "img": "bild-elservice", "alt": "Elektriker monterar ett vägguttag",
     "text": "Servicearbeten är huvuddelen av vår verksamhet. Vi utför elservice åt en stor kundkrets inom industri, fastighetsförvaltning och butiker."},
    {"id": "industri", "title": "Industri", "img": "bild-industri-elcentral", "alt": "Elektriker arbetar i ett elskåp",
     "text": "Vi utför elinstallationer och servicearbeten åt kunder inom industrin i Göteborgsområdet."},
    {"id": "fastighet", "title": "Fastighetsförvaltning", "img": "bild-fastighet-kontorshus", "alt": "Fasad på ett kontorshus",
     "text": "Vi arbetar åt kunder inom fastighetsförvaltning med servicearbeten och elinstallationer."},
    {"id": "butik", "title": "Butiker", "img": "bild-butik-interior", "alt": "Interiör i en klädbutik",
     "text": "Vi utför servicearbeten och elinstallationer åt kunder med butiker."},
    {"id": "nyproduktion", "title": "Nyproduktion", "img": "bild-nyproduktion-kabelstegar", "alt": "Kablar dragna på kabelstegar",
     "text": "Utöver servicearbetena utför vi en del elinstallationer i nyproduktion."},
    {"id": "ombyggnad", "title": "Ombyggnader", "img": "bild-ombyggnad-belysning", "alt": "Elektriker byter belysning i ett tak",
     "text": "Vi utför även elarbeten vid ombyggnader."},
]
BYID = {a["id"]: a for a in AREAS}


def picture(p, name, alt, w, h, eager=False, style=""):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    st = f' style="{style}"' if style else ""
    return (f'<picture><source srcset="{p}img/{name}.webp" type="image/webp">'
            f'<img src="{p}img/{name}.jpg" alt="{alt}" width="{w}" height="{h}" {load} decoding="async"{st}></picture>')


BUILDING = ("foretaget-lokaler-servicebilar", "Nyberg &amp; Karlsons Elektriska AB:s kontorsbyggnad med företagsskylt, med personal och fem servicebilar uppställda framför", 800, 452)
VAN = ("servicebil-dekal", "Servicebil med Nyberg &amp; Karlsons logotyp och texten Sedan 1910", 806, 456)


# ------------------------------------------------------------------ gemensamma delar
def head(p, page, title, desc, path, extra=""):
    canon = SITE_URL + path
    return f"""<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#1b2457">
<meta property="og:type" content="website">
<meta property="og:locale" content="sv_SE">
<meta property="og:site_name" content="{escape(CO['name'])}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE_URL}/img/og-bild.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{p}img/favicon.png">
<link rel="apple-touch-icon" href="{p}img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap">
<link rel="stylesheet" href="{p}assets/style.css">
{extra}</head>
<body data-page="{page}">
"""


def nav(p, current):
    items = [("index", "Hem", f"{p}index.html"), ("verksamhet", "Verksamhet", f"{p}verksamhet/"),
             ("foretaget", "Företaget", f"{p}foretaget/"), ("kontakt", "Kontakt", f"{p}kontakta-oss/")]
    cur = ' aria-current="page"'
    lis = "".join(f'<li><a href="{href}"{cur if key == current else ""}>{label}</a></li>' for key, label, href in items)
    return f"""<a class="skip" href="#innehall">Hoppa till innehållet</a>
<header class="nav"><div class="wrap">
<a class="logo" href="{p}index.html"><img src="{p}img/logo-nyberg-karlsons-vit.png" width="640" height="176" alt="Nyberg &amp; Karlsons Elektriska AB, sedan 1910"></a>
<button class="burger" type="button" aria-expanded="false" aria-controls="meny"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>Meny</button>
<ul class="menu" id="meny">{lis}</ul>
</div></header>
<main id="innehall">
"""


def foot(p):
    people = "".join(f'<li><a href="mailto:{x["email"]}">{x["name"]}</a><small>{x["mobile"]}</small></li>' for x in PEOPLE)
    return f"""</main>
<footer class="foot"><div class="wrap">
<div class="foot-grid">
<div><a class="logo" href="{p}index.html"><img src="{p}img/logo-nyberg-karlsons-vit.png" width="640" height="176" alt="Nyberg &amp; Karlsons Elektriska AB" loading="lazy"></a>
<p>Elinstallationer i Göteborgsområdet sedan 1910. Främst servicearbeten åt industri, fastighetsförvaltning och butiker.</p></div>
<div><h2>Kontakt</h2><ul><li><a href="tel:{CO['tel']}">{CO['phone']}</a></li><li><a href="mailto:{CO['email']}">{CO['email']}</a></li><li>{CO['street']}</li><li>{CO['zip']} {CO['city']}</li></ul></div>
<div><h2>Sidor</h2><ul><li><a href="{p}verksamhet/">Verksamhet</a></li><li><a href="{p}foretaget/">Företaget</a></li><li><a href="{p}kontakta-oss/">Kontakt</a></li><li><a href="{p}kontakta-oss/#projektledare">Projektledare</a></li></ul></div>
<div><h2>Projektledare</h2><ul>{people}</ul></div>
</div>
<div class="foot-bottom"><span>© 2026 {escape(CO['name'])}</span><span>{CO['street']}, {CO['zip']} {CO['city']}</span></div>
</div></footer>
<script src="{p}assets/main.js"></script>
</body>
</html>
"""


def schema():
    data = {
        "@context": "https://schema.org",
        "@type": "Electrician",
        "name": CO["name"],
        "url": SITE_URL + "/",
        "logo": SITE_URL + "/img/logo-nyberg-karlsons.png",
        "image": SITE_URL + "/img/foretaget-lokaler-servicebilar.jpg",
        "telephone": "+46 31 80 13 50",
        "email": CO["email"],
        "foundingDate": CO["founded"],
        "description": "Elinstallationer i Göteborgsområdet sedan 1910. Främst servicearbeten åt industri, fastighetsförvaltning och butiker, samt nyproduktion och ombyggnader.",
        "address": {"@type": "PostalAddress", "streetAddress": CO["street"], "postalCode": CO["zip"].replace(" ", ""),
                    "addressLocality": CO["city"], "addressCountry": "SE"},
        "areaServed": {"@type": "Place", "name": "Göteborgsområdet"},
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n'


def ring(cls="btn-red"):
    return f'<a class="btn {cls}" href="tel:{CO["tel"]}">Ring oss</a>'


def kontakt_btn(p, cls="btn-line"):
    return f'<a class="btn {cls} arrow" href="{p}kontakta-oss/">Kontakta oss </a>'


def img_card(p, a, href):
    return (f'<a class="card" href="{href}"><div class="img">{picture(p, a["img"], "", 960, 540)}</div>'
            f'<div class="row">{a["title"]}<span aria-hidden="true">→</span></div></a>')


def person_card(x):
    return f"""<article class="person"><div class="av" aria-hidden="true">{x['initials']}</div><div>
<h3>{x['name']}</h3><p class="role">Projektledare</p>
<ul><li><a href="tel:{x['tel']}">{icon('phone')}{x['mobile']}</a></li><li><a href="mailto:{x['email']}">{icon('mail')}{x['email']}</a></li></ul>
</div></article>"""


def split(p, img, inner, gray=False, rev=False, sec_id="", seal=False, media_cls=""):
    cls = "sec gray" if gray else "sec"
    sid = f' id="{sec_id}"' if sec_id else ""
    sl = '<div class="seal"><div><small>Sedan</small>1910</div></div>' if seal else ""
    mc = f"media {media_cls}".strip()
    return (f'<section class="{cls}"{sid}><div class="wrap split{" rev" if rev else ""}">'
            f'<div class="{mc}">{picture(p, *img)}{sl}</div><div class="prose">{inner}</div></div></section>\n')


def trust():
    return f"""<section class="sec gray" style="padding-block:48px"><div class="wrap"><div class="trust">
<div><span class="ic">{icon('clock')}</span><span><b>SEDAN 1910</b><small>Elinstallationer i Göteborgsområdet</small></span></div>
<a href="https://www.elsakerhetsverket.se/" target="_blank" rel="noopener"><span class="ic">{icon('search')}</span><span><b>KOLLA ELFÖRETAGET</b><small>Kontrollera elföretag hos Elsäkerhetsverket</small></span></a>
</div></div></section>
"""


def hero(p, img, h1, lead, eyebrow="", cards="", img_style=""):
    eb = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ""
    cls = "hero" if cards else "hero no-cards"
    cards_html = f'<div class="hero-cards">{cards}</div>' if cards else ""
    return f"""<section class="{cls}"><div class="hero-bg">{picture(p, img[0], '', img[2], img[3], eager=True, style=img_style)}</div><div class="wrap">
<div class="hero-text">{eb}<h1>{h1}</h1><p class="lead">{lead}</p>
<div class="btns">{ring()}{kontakt_btn(p, 'btn-ghost')}</div></div>
{cards_html}</div></section>
"""


# ------------------------------------------------------------------ Hem
def page_index():
    p = ""
    cards = "".join(img_card(p, BYID[k], f"verksamhet/#{k}") for k in ["service", "industri", "fastighet", "butik"])
    tjanster = "".join(img_card(p, a, f"verksamhet/#{a['id']}") for a in AREAS)
    people = "".join(person_card(x) for x in PEOPLE)
    body = hero(p, BUILDING, "Elinstallationer i Göteborg sedan 1910",
                "Nyberg &amp; Karlsons Elektriska AB har sedan 1910 utfört elinstallationer i Göteborgsområdet, främst servicearbeten åt industri, fastighetsförvaltning och butiker.",
                cards=cards, img_style="object-position:center 40%")
    body += split(p, ("bild-elservice", "Elektriker monterar ett vägguttag", 960, 639),
                  '<span class="eyebrow">Verksamheten</span><h2 class="h2">Servicearbeten, nyproduktion och ombyggnader</h2>'
                  '<p>Verksamheten består i huvudsak av servicearbeten åt en stor kundkrets inom industri, fastighetsförvaltning och butiker, men även en del nyproduktion och ombyggnader.</p>'
                  '<div class="btns"><a class="btn btn-line arrow" href="verksamhet/">Läs mer om verksamheten </a></div>')
    body += split(p, ("bild-industri-elcentral", "Elektriker arbetar i ett elskåp", 960, 639),
                  '<span class="eyebrow">Företag och fastigheter</span><h2 class="h2">Elfirma i Göteborg för industri, fastighet och butik</h2>'
                  '<p>Våra kunder finns inom industri, fastighetsförvaltning och butiker. Det är åt dem vi utför den största delen av våra servicearbeten.</p>'
                  f'<p>Ni når våra projektledare direkt, eller växeln på <a href="tel:{CO["tel"]}">{CO["phone"]}</a>.</p>'
                  f'<div class="btns">{ring()}</div>', gray=True, rev=True)
    body += (f'<section class="sec" id="tjanster"><div class="wrap"><div class="sec-head"><div class="prose"><span class="eyebrow">Verksamhet</span>'
             f'<h2 class="h2">Det här arbetar vi med</h2></div>{ring()}</div><div class="grid g3">{tjanster}</div></div></section>\n')
    body += split(p, BUILDING,
                  '<span class="eyebrow">Företaget</span><h2 class="h2">Mer än hundra år i Göteborgsområdet</h2>'
                  '<p>Nyberg &amp; Karlsons Elektriska AB startades 1910 och har sedan dess utfört elinstallationer i Göteborgsområdet.</p>'
                  f'<p>Kontoret finns på {CO["street"]} i Göteborg.</p>'
                  '<div class="btns"><a class="btn btn-line arrow" href="foretaget/">Läs mer om företaget </a></div>', gray=True, seal=True)
    body += (f'<section class="sec" id="projektledare"><div class="wrap split"><div><span class="eyebrow">Personal</span>'
             f'<p class="quote">Kontakta våra <em>projektledare</em> direkt.</p></div><div class="prose">'
             f'<p>Har ni ett servicejobb, en ombyggnad eller ett nytt projekt? Ring eller mejla någon av våra projektledare.</p>'
             f'<div class="grid" style="gap:16px">{people}</div></div></div></section>\n')
    body += f'<div class="photo-strip">{picture(p, "bild-nyproduktion-kabelstegar", "Kablar dragna på kabelstegar", 1400, 1050, style="object-position:center 55%")}</div>\n'
    body += (f'<section class="sec dark"><div class="wrap split"><div class="prose"><span class="eyebrow">Varför Nyberg &amp; Karlsons</span>'
             f'<h2 class="h2">Ett etablerat elföretag sedan 1910</h2>'
             f'<p>Nyberg &amp; Karlsons Elektriska AB har funnits sedan 1910 och har under hela den tiden utfört elinstallationer i Göteborgsområdet.</p>'
             f'<p>Servicearbetena är kärnan i verksamheten, och kundkretsen finns inom industri, fastighetsförvaltning och butiker.</p>'
             f'<div class="btns">{ring()}{kontakt_btn(p, "btn-ghost")}</div></div>'
             f'<div class="prose"><ul class="checklist"><li class="chk">Elinstallationer i Göteborgsområdet sedan 1910</li><li class="chk">Främst servicearbeten</li>'
             f'<li class="chk">Kunder inom industri, fastighetsförvaltning och butiker</li><li class="chk">Även nyproduktion och ombyggnader</li>'
             f'<li class="chk">Projektledare som ni når direkt</li></ul></div></div></section>\n')
    body += (f'<section class="band">{picture(p, *BUILDING)}<div class="wrap"><div class="prose"><span class="eyebrow">Kontakt</span>'
             f'<h2 class="h2">Behöver ni hjälp med el?</h2><p>Berätta vad som ska göras så återkommer vi. Ni når oss på {CO["phone"]} eller {CO["email"]}.</p>'
             f'<div class="btns">{kontakt_btn(p, "btn-white")}</div></div></div></section>\n')
    body += trust()
    return (head(p, "index", "Elinstallationer i Göteborg sedan 1910 | Nyberg & Karlsons Elektriska AB",
                 "Nyberg & Karlsons Elektriska AB utför elinstallationer i Göteborgsområdet sedan 1910. Främst servicearbeten åt industri, fastighetsförvaltning och butiker.",
                 "/", schema()) + nav(p, "index") + body + foot(p))


# ------------------------------------------------------------------ Verksamhet (motsvarar Bloms Tjänster)
def page_verksamhet():
    p = "../"
    cards = "".join(img_card(p, BYID[k], f"#{k}") for k in ["service", "industri", "fastighet", "butik"])
    body = hero(p, ("bild-elcentral-plintar", "", 1024, 576), "Vår verksamhet",
                "Främst servicearbeten åt kunder inom industri, fastighetsförvaltning och butiker, men även en del nyproduktion och ombyggnader i Göteborgsområdet.",
                eyebrow="Elinstallationer Göteborg", cards=cards)
    for i, a in enumerate(AREAS):
        body += split(p, (a["img"], a["alt"], 960, 640),
                      f'<span class="eyebrow">Verksamhet</span><h2 class="h2">{a["title"]}</h2><p>{a["text"]}</p>'
                      f'<div class="btns">{ring()}{kontakt_btn(p)}</div>', gray=bool(i % 2), rev=bool(i % 2), sec_id=a["id"])
    body += trust()
    return (head(p, "verksamhet", "Verksamhet – elservice för industri, fastighet och butik | Nyberg & Karlsons Elektriska AB",
                 "Servicearbeten och elinstallationer för industri, fastighetsförvaltning och butiker samt nyproduktion och ombyggnader i Göteborgsområdet.",
                 "/verksamhet/") + nav(p, "verksamhet") + body + foot(p))


# ------------------------------------------------------------------ Företaget
def page_foretaget():
    p = "../"
    body = hero(p, BUILDING, "Om Nyberg &amp; Karlsons Elektriska AB",
                "Ett elföretag i Göteborg som har utfört elinstallationer i Göteborgsområdet sedan 1910.", eyebrow="Företaget",
                img_style="object-position:center 40%")
    body += split(p, BUILDING,
                  '<span class="eyebrow">Sedan 1910</span><h2 class="h2">Elinstallationer i Göteborgsområdet i mer än hundra år</h2>'
                  '<p>Nyberg &amp; Karlsons Elektriska AB startades 1910 och har sedan dess utfört elinstallationer i Göteborgsområdet.</p>'
                  '<p>Verksamheten består i huvudsak av servicearbeten åt en stor kundkrets inom industri, fastighetsförvaltning och butiker, men även en del nyproduktion och ombyggnader.</p>'
                  f'<div class="btns">{ring()}{kontakt_btn(p)}</div>', seal=True)
    checks = "".join(f'<li class="chk">{a["title"]}</li>' for a in AREAS)
    body += split(p, VAN,
                  '<span class="eyebrow">Verksamhet</span><h2 class="h2">Service i första hand</h2>'
                  '<p>Det mesta vi gör är servicearbeten åt en stor kundkrets. Vid sidan av servicen utför vi även en del nyproduktion och ombyggnader.</p>'
                  f'<ul class="checklist">{checks}</ul><div class="btns"><a class="btn btn-line arrow" href="../verksamhet/">Läs mer om verksamheten </a></div>',
                  gray=True, rev=True, media_cls="left")
    kunder = "".join(img_card(p, BYID[k], "../verksamhet/#" + k) for k in ["industri", "fastighet", "butik"])
    body += (f'<section class="sec"><div class="wrap"><div class="sec-head"><div class="prose"><span class="eyebrow">Kunder</span>'
             f'<h2 class="h2">Vilka vi arbetar åt</h2></div>{ring()}</div><div class="grid g3">{kunder}</div></div></section>\n')
    contacts = "".join(f'<li class="chk">{x["name"]}, projektledare · <a href="tel:{x["tel"]}">{x["mobile"]}</a></li>' for x in PEOPLE)
    body += (f'<section class="sec dark"><div class="wrap split"><div class="prose"><span class="eyebrow">Personal</span>'
             f'<h2 class="h2">Kontakta våra projektledare</h2><p>Ni når våra projektledare direkt på mobil eller e-post, eller växeln på {CO["phone"]}.</p>'
             f'<div class="btns">{ring()}{kontakt_btn(p, "btn-ghost")}</div></div><div class="prose"><ul class="checklist">{contacts}'
             f'<li class="chk">Växel · <a href="tel:{CO["tel"]}">{CO["phone"]}</a></li><li class="chk"><a href="mailto:{CO["email"]}">{CO["email"]}</a></li></ul></div></div></section>\n')
    body += trust()
    return (head(p, "foretaget", "Företaget – elföretag i Göteborg sedan 1910 | Nyberg & Karlsons Elektriska AB",
                 "Nyberg & Karlsons Elektriska AB startades 1910 och utför elinstallationer i Göteborgsområdet, främst servicearbeten åt industri, fastighetsförvaltning och butiker.",
                 "/foretaget/") + nav(p, "foretaget") + body + foot(p))


# ------------------------------------------------------------------ Kontakt
def page_kontakt():
    p = "../"
    people = "".join(person_card(x) for x in PEOPLE)
    cards = (f'<a class="card icon" href="tel:{CO["tel"]}"><div class="ic">{icon("phone")}</div><div class="row">Ring oss<small>{CO["phone"]}</small></div></a>'
             f'<a class="card icon" href="mailto:{CO["email"]}"><div class="ic">{icon("mail")}</div><div class="row">Mejla oss<small>{CO["email"]}</small></div></a>'
             f'<a class="card icon" href="#karta"><div class="ic">{icon("pin")}</div><div class="row">Besök oss<small>{CO["street"]}, {CO["zip"]} {CO["city"]}</small></div></a>'
             f'<a class="card icon" href="#formular"><div class="ic">{icon("form")}</div><div class="row">Skicka förfrågan<small>Beskriv vad ni behöver hjälp med</small></div></a>')
    options = "".join(f"<option>{o}</option>" for o in ["Service / felsökning", "Industri", "Fastighetsförvaltning", "Butik", "Nyproduktion", "Ombyggnad", "Annat"])
    body = (f'<section class="hero"><div class="hero-bg">{picture(p, VAN[0], "", VAN[2], VAN[3], eager=True)}</div><div class="wrap">'
            f'<div class="hero-text"><span class="eyebrow">{escape(CO["name"])}</span><h1>Kontakta oss</h1>'
            f'<p class="lead">Vad kan vi hjälpa er med? Ring växeln, mejla eller kontakta någon av våra projektledare direkt.</p></div>'
            f'<div class="hero-cards">{cards}</div></div></section>\n')
    body += (f'<section class="sec" id="projektledare"><div class="wrap"><div class="sec-head"><div class="prose"><span class="eyebrow">Personal</span>'
             f'<h2 class="h2">Kontakta våra projektledare</h2></div>{ring()}</div><div class="grid g2">{people}</div></div></section>\n')
    body += f"""<section class="sec gray" id="formular"><div class="wrap split"><div class="prose"><span class="eyebrow">Vi vill höra av er!</span><h2 class="h2">Berätta vad ni behöver hjälp med</h2><p>Beskriv vad som ska göras och var, så återkommer vi. Uppge gärna företag och telefonnummer.</p><ul class="checklist" style="margin-top:8px"><li class="chk"><a href="tel:{CO['tel']}">{CO['phone']}</a></li><li class="chk"><a href="mailto:{CO['email']}">{CO['email']}</a></li><li class="chk">{CO['street']}, {CO['zip']} {CO['city']}</li></ul></div>
<form class="form" id="kontaktform" data-to="{CO['email']}" novalidate><div class="two"><label for="f-namn">Namn<input id="f-namn" name="namn" autocomplete="name" required></label><label for="f-foretag"><span>Företag <span class="opt">(valfritt)</span></span><input id="f-foretag" name="foretag" autocomplete="organization"></label></div><div class="two"><label for="f-epost">E-post<input id="f-epost" name="epost" type="email" autocomplete="email"></label><label for="f-tel">Telefon<input id="f-tel" name="telefon" type="tel" autocomplete="tel"></label></div><label for="f-arende">Ärende<select id="f-arende" name="arende">{options}</select></label><label for="f-medd">Meddelande<textarea id="f-medd" name="meddelande" required></textarea></label><button class="btn btn-red" type="submit">Skicka</button><p class="note">Ditt e-postprogram öppnas med meddelandet ifyllt till {CO['email']}.</p><p class="msg" role="status" aria-live="polite"></p></form></div></section>
"""
    body += split(p, BUILDING,
                  f'<span class="eyebrow">Kontor</span><h2 class="h2">{CO["street"]}, Göteborg</h2>'
                  f'<p>{escape(CO["name"])}<br>{CO["street"]}<br>{CO["zip"]} {CO["city"]}</p>'
                  f'<div class="btns"><a class="btn btn-line arrow" href="{MAPS}" target="_blank" rel="noopener">Öppna i Google Maps </a></div>',
                  rev=True, sec_id="karta")
    return (head(p, "kontakt", "Kontakta oss | Nyberg & Karlsons Elektriska AB, Göteborg",
                 "Kontakta Nyberg & Karlsons Elektriska AB på 031-80 13 50 eller mail@nykael.se. Norra Ågatan 10, Göteborg. Kontaktuppgifter till våra projektledare.",
                 "/kontakta-oss/", schema()) + nav(p, "kontakt") + body + foot(p))


# ------------------------------------------------------------------ 404
def page_404():
    # 404-sidan kan visas på vilken adress som helst, därför absoluta sökvägar
    p = "/"
    body = hero(p, BUILDING, "Sidan kunde inte hittas", "Adressen finns inte, eller så har sidan flyttats.", eyebrow="404")
    html = head(p, "404", "Sidan kunde inte hittas | Nyberg & Karlsons Elektriska AB", "Sidan kunde inte hittas.", "/404.html",
                '<meta name="robots" content="noindex">\n') + nav(p, "") + body + foot(p)
    return html.replace('href="/index.html', 'href="/')


def main():
    out = {
        "index.html": page_index(),
        "verksamhet/index.html": page_verksamhet(),
        "foretaget/index.html": page_foretaget(),
        "kontakta-oss/index.html": page_kontakt(),
        "404.html": page_404(),
    }
    for rel, html in out.items():
        f = ROOT / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(html, encoding="utf-8")
        print("skrev", rel)
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    urls = "".join(f"  <url><loc>{SITE_URL}{u}</loc></url>\n" for u in ["/", "/verksamhet/", "/foretaget/", "/kontakta-oss/"])
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")


if __name__ == "__main__":
    main()
