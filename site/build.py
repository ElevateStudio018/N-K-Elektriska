#!/usr/bin/env python3
"""Genererar alla sidor för nya nykael.se: python3 site/build.py

Gamla adresser (/, /foretaget/, /kontakta-oss/) finns kvar så att befintliga länkar fungerar.
All fakta kommer från nykael.se (startsida, Företaget, Kontakta oss och mediabiblioteket).
"""
import json
import os
from html import escape
from pathlib import Path

# Elevate Studio's credit under every footer: the mark and the name, the whole of it one link to elevatestudio.nu.
ELEVATE_CREDIT = '''<!-- elevate-credit -->
<style>.elevate-credit{max-width:1240px;margin:24px auto 0;padding:20px 16px 0;border-top:1px solid rgba(128,128,128,.25);display:flex;justify-content:center;box-sizing:border-box}.elevate-credit a{display:inline-flex;align-items:center;gap:8px;padding:8px 0;font:inherit;font-size:13px;line-height:1;color:inherit;opacity:.55;text-decoration:none;transition:opacity .2s}.elevate-credit a:hover,.elevate-credit a:focus-visible{opacity:1}.elevate-credit svg{width:16px;height:16px;flex:none;display:block}@media(min-width:1024px){.elevate-credit a{font-size:14px}}</style>
<div class="elevate-credit"><a href="https://elevatestudio.nu" target="_blank" rel="noopener"><svg viewBox="0 0 1884.3 1353.9" aria-hidden="true"><path d="M0.0 1353.9 L1218.7 0.0 L1218.7 329.1 L479.7 1136.4 L786.7 1132.4 L1215.5 687.4 L1884.3 1349.9 L1590.1 1349.9 L1218.6 994.7 L865.4 1349.9Z" fill="currentColor"/></svg>Byggd av Elevate Studio</a></div>
'''


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
    items = [("index", "Start", f"{p}index.html"), ("verksamhet", "Verksamhet", f"{p}verksamhet/"),
             ("foretaget", "Företaget", f"{p}foretaget/"), ("kontakt", "Kontakt", f"{p}kontakta-oss/")]
    cur = ' aria-current="page"'
    lis = "".join(f'<li><a href="{href}"{cur if key == current else ""}>{label}</a></li>' for key, label, href in items)
    return f"""<a class="skip" href="#innehall">Hoppa till innehållet</a>
<header class="nav"><div class="wrap">
<a class="logo" href="{p}index.html"><img src="{p}img/logo-nyberg-karlsons.png" width="640" height="176" alt="Nyberg &amp; Karlsons Elektriska AB, sedan 1910"></a>
<div class="nav-right">
<button class="burger" type="button" aria-expanded="false" aria-controls="meny"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>Meny</button>
<nav aria-label="Huvudmeny"><ul class="menu" id="meny">{lis}</ul></nav>
<a class="nav-tel" href="tel:{CO['tel']}" aria-label="Ring {CO['phone']}">{icon('phone')}<span>{CO['phone']}</span></a>
<a class="btn btn-navy" href="{p}kontakta-oss/#formular">Kontakta oss</a>
</div>
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
</div>{ELEVATE_CREDIT}</footer>
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


def ring(cls="btn-line"):
    return f'<a class="btn {cls}" href="tel:{CO["tel"]}">{icon("phone")}Ring {CO["phone"]}</a>'


def kontakt_btn(p, cls="btn-navy"):
    return f'<a class="btn {cls} arrow" href="{p}kontakta-oss/#formular">Kontakta oss </a>'


def svc_card(p, n, a, wide=False):
    cls = "svc wide" if wide else "svc"
    return (f'<article class="{cls}" id="{a["id"]}"><div class="img">{picture(p, a["img"], a["alt"], 960, 640)}</div>'
            f'<div class="in"><i>{n:02d}</i><h3>{a["title"]}</h3><p>{a["text"]}</p></div></article>')


def person_card(x):
    return f"""<article class="person"><div class="av" aria-hidden="true">{x['initials']}</div><div>
<h3>{x['name']}</h3><p class="role">Projektledare</p>
<ul><li><a href="tel:{x['tel']}">{icon('phone')}{x['mobile']}</a></li><li><a href="mailto:{x['email']}">{icon('mail')}{x['email']}</a></li></ul>
</div></article>"""


def contact_list():
    return f"""<ul class="contact-list">
<li><span class="ic">{icon('phone')}</span><div><b>Telefon</b><a href="tel:{CO['tel']}">{CO['phone']}</a></div></li>
<li><span class="ic">{icon('mail')}</span><div><b>E-post</b><a href="mailto:{CO['email']}">{CO['email']}</a></div></li>
<li><span class="ic">{icon('pin')}</span><div><b>Adress</b><a href="{MAPS}" target="_blank" rel="noopener">{CO['street']}, {CO['zip']} {CO['city']}</a></div></li>
</ul>"""


def hero(p, img, h1, lead, eyebrow="", listing="", img_style="", year=True):
    eb = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ""
    cls = "hero" if listing else "hero no-cards"
    lst = f'<nav class="hero-list" aria-label="Verksamhetsområden">{listing}</nav>' if listing else ""
    yr = '<div class="year" aria-hidden="true">1910</div>' if year else ""
    return f"""<section class="{cls}"><div class="hero-bg">{picture(p, img[0], '', img[2], img[3], eager=True, style=img_style)}</div>{yr}<div class="wrap">
<div class="hero-text">{eb}<h1>{h1}</h1><p class="lead">{lead}</p>
<div class="btns">{kontakt_btn(p, 'btn-blue')}{ring('btn-ghost')}</div></div>
{lst}</div></section>
"""


def facts():
    return """<section class="sec dark"><div class="wrap">
<div class="sec-head"><div class="prose"><span class="eyebrow">Varför Nyberg &amp; Karlsons</span><h2 class="h2">Ett etablerat elföretag i Göteborg</h2></div></div>
<div class="facts">
<div class="fact"><div class="num">1910</div><h3>Lång erfarenhet</h3><p>Företaget har utfört elinstallationer i Göteborgsområdet sedan starten 1910.</p></div>
<div class="fact"><div class="num word">Service</div><h3>Service i fokus</h3><p>Huvuddelen av verksamheten består av servicearbeten åt en stor kundkrets.</p></div>
<div class="fact"><div class="num word">Industri, fastighet &amp; butik</div><h3>En bred kundkrets</h3><p>Vi arbetar åt kunder inom industri, fastighetsförvaltning och butiker.</p></div>
</div></div></section>
"""


def cta(p):
    return f"""<section class="sec gray"><div class="wrap split">
<div class="prose"><span class="eyebrow">Kontakt</span><h2 class="h2">Behöver ni hjälp med el?</h2>
<p>Berätta vad som ska göras så återkommer vi. Ni kan också vända er direkt till någon av våra projektledare.</p>
<div class="btns">{kontakt_btn(p)}<a class="btn btn-line arrow" href="{p}kontakta-oss/#projektledare">Våra projektledare </a></div></div>
{contact_list()}
</div></section>
"""


# ------------------------------------------------------------------ Start
def page_index():
    p = ""
    listing = "".join(f'<a href="verksamhet/#{k}"><i>{i:02d}</i><b>{t}</b><small>{s}</small></a>' for i, (k, t, s) in enumerate([
        ("service", "Servicearbeten", "Vår huvudsakliga verksamhet"),
        ("industri", "Industri", "Installation och service"),
        ("fastighet", "Fastighetsförvaltning", "El i förvaltade fastigheter"),
        ("butik", "Butiker", "El i handelslokaler"),
    ], 1))
    body = hero(p, BUILDING, "Elinstallationer i Göteborgsområdet sedan 1910",
                "Nyberg &amp; Karlsons Elektriska AB utför främst servicearbeten åt kunder inom industri, fastighetsförvaltning och butiker, men även nyproduktion och ombyggnader.",
                eyebrow="Elinstallationer · Göteborg", listing=listing, img_style="object-position:center 40%")
    body += f"""<section class="sec" id="om"><div class="wrap split">
<div class="prose"><span class="eyebrow">Om företaget</span><h2 class="h2">Mer än hundra år av elarbeten i Göteborg</h2>
<p>Nyberg &amp; Karlsons Elektriska AB startades 1910 och har sedan dess utfört elinstallationer i Göteborgsområdet.</p>
<p>Verksamheten består i huvudsak av servicearbeten åt en stor kundkrets inom industri, fastighetsförvaltning och butiker, men även en del nyproduktion och ombyggnader.</p>
<div class="btns"><a class="btn btn-line arrow" href="foretaget/">Läs mer om företaget </a></div></div>
<figure class="media left">{picture(p, *VAN)}<div class="badge"><small>Sedan</small><b>1910</b></div></figure>
</div></section>
"""
    cards = "".join(svc_card(p, i, a) for i, a in enumerate(AREAS, 1)).replace(' id="', ' data-id="')
    body += f"""<section class="sec gray" id="verksamhet"><div class="wrap">
<div class="sec-head"><div class="prose"><span class="eyebrow">Verksamhet</span><h2 class="h2">Det här arbetar vi med</h2>
<p>Service är kärnan i verksamheten. Vid sidan av den åtar vi oss nyproduktion och ombyggnader.</p></div>
<a class="btn btn-line arrow" href="verksamhet/">Hela verksamheten </a></div>
<div class="grid g3">{cards}</div></div></section>
"""
    body += facts()
    people = "".join(person_card(x) for x in PEOPLE)
    body += f"""<section class="sec" id="projektledare"><div class="wrap">
<div class="sec-head"><div class="prose"><span class="eyebrow">Personal</span><h2 class="h2">Kontakta våra projektledare</h2>
<p>Ring eller mejla direkt till någon av våra projektledare, eller kontakta växeln på <a href="tel:{CO['tel']}">{CO['phone']}</a>.</p></div></div>
<div class="grid g2">{people}</div></div></section>
"""
    body += cta(p)
    return (head(p, "index", "Elinstallationer i Göteborg sedan 1910 | Nyberg & Karlsons Elektriska AB",
                 "Nyberg & Karlsons Elektriska AB utför elinstallationer i Göteborgsområdet sedan 1910. Främst servicearbeten åt industri, fastighetsförvaltning och butiker.",
                 "/", schema()) + nav(p, "index") + body + foot(p))


# ------------------------------------------------------------------ Verksamhet
def page_verksamhet():
    p = "../"
    body = hero(p, ("bild-elcentral-plintar", "", 1024, 576), "Vår verksamhet",
                "Främst servicearbeten åt kunder inom industri, fastighetsförvaltning och butiker, men även en del nyproduktion och ombyggnader i Göteborgsområdet.",
                eyebrow="Verksamhet", year=False)
    cards = "".join(svc_card(p, i, a, wide=True) for i, a in enumerate(AREAS, 1))
    body += f"""<section class="sec"><div class="wrap">
<div class="sec-head"><div class="prose"><span class="eyebrow">Verksamhetsområden</span><h2 class="h2">Service först, nyproduktion och ombyggnader därtill</h2></div></div>
<div class="grid g2">{cards}</div></div></section>
"""
    body += cta(p)
    return (head(p, "verksamhet", "Verksamhet – elservice för industri, fastighet och butik | Nyberg & Karlsons Elektriska AB",
                 "Servicearbeten och elinstallationer för industri, fastighetsförvaltning och butiker samt nyproduktion och ombyggnader i Göteborgsområdet.",
                 "/verksamhet/") + nav(p, "verksamhet") + body + foot(p))


# ------------------------------------------------------------------ Företaget
def page_foretaget():
    p = "../"
    body = hero(p, BUILDING, "Om Nyberg &amp; Karlsons Elektriska AB",
                "Ett elföretag i Göteborg som har utfört elinstallationer i Göteborgsområdet sedan 1910.", eyebrow="Företaget",
                img_style="object-position:center 40%")
    body += f"""<section class="sec"><div class="wrap split">
<div class="prose"><span class="eyebrow">Sedan 1910</span><h2 class="h2">Elinstallationer i Göteborgsområdet i mer än hundra år</h2>
<p>Nyberg &amp; Karlsons Elektriska AB startades 1910 och har sedan dess utfört elinstallationer i Göteborgsområdet.</p>
<p>Verksamheten består i huvudsak av servicearbeten åt en stor kundkrets inom industri, fastighetsförvaltning och butiker, men även en del nyproduktion och ombyggnader.</p></div>
<figure class="media">{picture(p, *BUILDING)}<figcaption>Företagets lokaler och servicebilar.</figcaption></figure>
</div></section>
"""
    checks = "".join(f'<li class="chk">{a["title"]}</li>' for a in AREAS)
    body += f"""<section class="sec gray"><div class="wrap split top">
<div class="prose"><span class="eyebrow">Verksamhet</span><h2 class="h2">Service i första hand</h2>
<p>Det mesta vi gör är servicearbeten åt en stor kundkrets. Vid sidan av servicen utför vi även en del nyproduktion och ombyggnader.</p>
<ul class="checklist cols">{checks}</ul>
<div class="btns"><a class="btn btn-line arrow" href="../verksamhet/">Läs mer om verksamheten </a></div></div>
<figure class="media left">{picture(p, *VAN)}<div class="badge"><small>Sedan</small><b>1910</b></div></figure>
</div></section>
"""
    body += facts()
    body += cta(p)
    return (head(p, "foretaget", "Företaget – elföretag i Göteborg sedan 1910 | Nyberg & Karlsons Elektriska AB",
                 "Nyberg & Karlsons Elektriska AB startades 1910 och utför elinstallationer i Göteborgsområdet, främst servicearbeten åt industri, fastighetsförvaltning och butiker.",
                 "/foretaget/") + nav(p, "foretaget") + body + foot(p))


# ------------------------------------------------------------------ Kontakt
def page_kontakt():
    p = "../"
    people = "".join(person_card(x) for x in PEOPLE)
    options = "".join(f"<option>{o}</option>" for o in ["Service / felsökning", "Industri", "Fastighetsförvaltning", "Butik", "Nyproduktion", "Ombyggnad", "Annat"])
    body = hero(p, VAN, "Kontakta oss",
                "Ring växeln, mejla eller vänd er direkt till någon av våra projektledare. Ni kan också skicka en förfrågan via formuläret.",
                eyebrow=escape(CO["name"]), year=False, img_style="object-position:0 50%")
    body += f"""<section class="sec" id="formular"><div class="wrap split top">
<div class="prose"><span class="eyebrow">Växel och e-post</span><h2 class="h2">Så når ni oss</h2>
<p>Beskriv gärna kort vad som ska göras och var, så återkommer vi.</p>
{contact_list()}</div>
<form class="form" id="kontaktform" data-to="{CO['email']}" novalidate>
<h3>Skicka en förfrågan</h3>
<div class="two"><label for="f-namn">Namn<input id="f-namn" name="namn" autocomplete="name" required></label>
<label for="f-foretag"><span>Företag <span class="opt">(valfritt)</span></span><input id="f-foretag" name="foretag" autocomplete="organization"></label></div>
<div class="two"><label for="f-epost">E-post<input id="f-epost" name="epost" type="email" autocomplete="email"></label>
<label for="f-tel">Telefon<input id="f-tel" name="telefon" type="tel" autocomplete="tel"></label></div>
<label for="f-arende">Ärende<select id="f-arende" name="arende">{options}</select></label>
<label for="f-medd">Meddelande<textarea id="f-medd" name="meddelande" required></textarea></label>
<button class="btn btn-navy" type="submit">Skicka förfrågan</button>
<p class="note">När du skickar öppnas ditt e-postprogram med meddelandet ifyllt till {CO['email']}. Du kan också ringa oss på {CO['phone']}.</p>
<p class="msg" role="status" aria-live="polite"></p>
</form></div></section>
"""
    body += f"""<section class="sec gray" id="projektledare"><div class="wrap">
<div class="sec-head"><div class="prose"><span class="eyebrow">Personal</span><h2 class="h2">Våra projektledare</h2>
<p>Kontakta våra projektledare direkt på mobil eller e-post.</p></div></div>
<div class="grid g2">{people}</div></div></section>
"""
    body += f"""<section class="sec" id="karta"><div class="wrap split">
<div class="prose"><span class="eyebrow">Adress</span><h2 class="h2">{CO['street']}, Göteborg</h2>
<p>{escape(CO['name'])}<br>{CO['street']}<br>{CO['zip']} {CO['city']}</p>
<div class="btns"><a class="btn btn-line arrow" href="{MAPS}" target="_blank" rel="noopener">Öppna i Google Maps </a></div></div>
<figure class="media">{picture(p, *BUILDING)}</figure>
</div></section>
"""
    return (head(p, "kontakt", "Kontakta oss | Nyberg & Karlsons Elektriska AB, Göteborg",
                 "Kontakta Nyberg & Karlsons Elektriska AB på 031-80 13 50 eller mail@nykael.se. Norra Ågatan 10, Göteborg. Kontaktuppgifter till våra projektledare.",
                 "/kontakta-oss/", schema()) + nav(p, "kontakt") + body + foot(p))

# ------------------------------------------------------------------ 404
def page_404():
    # 404-sidan kan visas på vilken adress som helst, därför absoluta sökvägar.
    # SITE_BASE sätts när sajten ligger i en undermapp, t.ex. /N-K-Elektriska/ på GitHub Pages.
    p = os.environ.get("SITE_BASE", "/")
    body = hero(p, BUILDING, "Sidan kunde inte hittas", "Adressen finns inte, eller så har sidan flyttats.", eyebrow="404", year=False)
    html = head(p, "404", "Sidan kunde inte hittas | Nyberg & Karlsons Elektriska AB", "Sidan kunde inte hittas.", "/404.html",
                '<meta name="robots" content="noindex">\n') + nav(p, "") + body + foot(p)
    return html.replace(f'href="{p}index.html', f'href="{p}')


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
