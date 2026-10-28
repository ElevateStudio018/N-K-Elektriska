#!/usr/bin/env python3
"""Genererar alla sidor för nya nykael.se: python3 site/build.py

Sidorna ligger på samma adresser som på den gamla webbplatsen (/, /foretaget/, /kontakta-oss/)
så att befintliga länkar och sökresultat fortsätter att fungera.
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

# ------------------------------------------------------------------ ikoner (egna, enkla linjeikoner)
ICON = {
    "service": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3.6 17.2a1.6 1.6 0 0 0 2.3 2.3l5.7-5.7a4 4 0 0 0 5.2-5.4l-2.5 2.5-2.2-.4-.4-2.2z"/>',
    "industri": '<path d="M3 21V10l5 3V10l5 3V10l5 3V4h3v17z"/><path d="M7 17h2M12 17h2M17 17h1"/>',
    "fastighet": '<path d="M4 21V5a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v16"/><path d="M14 10h5a1 1 0 0 1 1 1v10"/><path d="M8 8h2M8 12h2M8 16h2M17 14h0M17 17h0"/><path d="M2 21h20"/>',
    "butik": '<path d="M4 9h16l-1-5H5z"/><path d="M5 9v11h14V9"/><path d="M10 20v-6h4v6"/><path d="M4 9a2.7 2.7 0 0 0 5.3 0 2.7 2.7 0 0 0 5.4 0 2.7 2.7 0 0 0 5.3 0"/>',
    "nyproduktion": '<path d="M3 21h18"/><path d="M6 21V8l6-4 6 4v13"/><path d="M10 21v-5h4v5"/><path d="M10 11h4"/>',
    "ombyggnad": '<path d="M20 11a8 8 0 0 0-14.3-4.9L4 8"/><path d="M4 4v4h4"/><path d="M4 13a8 8 0 0 0 14.3 4.9L20 16"/><path d="M20 20v-4h-4"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "people": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.2A5 5 0 0 1 21 19"/>',
    "form": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13.5 6.5l4 4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg>'


# Verksamhetsområden enligt nykael.se: i huvudsak servicearbeten åt industri, fastighetsförvaltning
# och butiker, men även en del nyproduktion och ombyggnader.
AREAS = [
    ("service", "Servicearbeten", "Huvuddelen av verksamheten. Elservice, felsökning och åtgärder åt en stor kundkrets."),
    ("industri", "Industri", "Elinstallationer och service i industrins lokaler och anläggningar."),
    ("fastighet", "Fastighetsförvaltning", "Elarbeten åt fastighetsförvaltare, i allt från enskilda lokaler till hela fastigheter."),
    ("butik", "Butiker", "Elinstallationer och service i butiker och handelslokaler."),
    ("nyproduktion", "Nyproduktion", "Elinstallationer i nya byggnader och lokaler."),
    ("ombyggnad", "Ombyggnader", "Elarbeten när lokaler och fastigheter byggs om eller får en ny användning."),
]


# ------------------------------------------------------------------ gemensamma delar
def head(p, title, desc, path, extra=""):
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="{p}assets/style.css">
<script>document.documentElement.classList.add('js')</script>
{extra}</head>
"""


def nav(p, current):
    items = [("start", "Start", f"{p}index.html"), ("verksamhet", "Verksamhet", f"{p}index.html#verksamhet"),
             ("foretaget", "Företaget", f"{p}foretaget/"), ("personal", "Projektledare", f"{p}kontakta-oss/#projektledare"),
             ("kontakt", "Kontakta oss", f"{p}kontakta-oss/")]
    cur = ' aria-current="page"'
    lis = "".join(f'<li><a href="{href}"{cur if key == current else ""}>{label}</a></li>' for key, label, href in items)
    return f"""<body>
<a class="skip" href="#innehall">Hoppa till innehållet</a>
<header class="nav"><div class="wrap">
<a class="logo" href="{p}index.html"><img src="{p}img/logo-nyberg-karlsons-vit.png" width="640" height="176" alt="Nyberg &amp; Karlsons Elektriska AB, sedan 1910 – till startsidan"></a>
<div class="nav-right">
<button class="burger" type="button" aria-expanded="false" aria-controls="meny">{'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'}Meny</button>
<nav aria-label="Huvudmeny"><ul class="menu" id="meny">{lis}</ul></nav>
<a class="nav-tel" href="tel:{CO['tel']}" aria-label="Ring oss på {CO['phone']}">{icon('phone')}<span>{CO['phone']}</span></a>
<a class="btn btn-blue" href="{p}kontakta-oss/#formular">Kontakta oss</a>
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
<div><h2>Kontakt</h2><ul><li><a href="tel:{CO['tel']}">{CO['phone']}</a></li><li><a href="mailto:{CO['email']}">{CO['email']}</a></li><li><a href="{MAPS}" target="_blank" rel="noopener">{CO['street']}<br>{CO['zip']} {CO['city']}</a></li></ul></div>
<div><h2>Projektledare</h2><ul>{people}</ul></div>
<div><h2>Sidor</h2><ul><li><a href="{p}index.html">Start</a></li><li><a href="{p}index.html#verksamhet">Verksamhet</a></li><li><a href="{p}foretaget/">Företaget</a></li><li><a href="{p}kontakta-oss/">Kontakta oss</a></li></ul></div>
</div>
<div class="foot-bottom"><span>© 2026 {escape(CO['name'])}</span><span>{CO['street']}, {CO['zip']} {CO['city']}</span></div>
</div></footer>
<script src="{p}assets/main.js" defer></script>
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


def area_card(key, title, text, href=None, small=False):
    tag, attr = ("a", f' href="{href}"') if href else ("div", "")
    if small:
        return f'<{tag} class="card icon"{attr}><div class="ic">{icon(key)}</div><div class="row">{title}<small>{text}</small></div></{tag}>'
    return f'<{tag} class="card icon top-accent"{attr}><div class="ic">{icon(key)}</div><div class="row">{title}</div><div class="body"><p>{text}</p></div></{tag}>'


def person_card(x):
    return f"""<article class="person"><div class="av" aria-hidden="true">{x['initials']}</div><div>
<h3>{x['name']}</h3><p class="role">Projektledare</p>
<ul><li><a href="tel:{x['tel']}">{icon('phone')}{x['mobile']}</a></li><li><a href="mailto:{x['email']}">{icon('mail')}{x['email']}</a></li></ul>
</div></article>"""


def contact_list(dark=False):
    return f"""<ul class="contact-list">
<li><span class="ic">{icon('phone')}</span><div><b>Telefon</b><a href="tel:{CO['tel']}">{CO['phone']}</a></div></li>
<li><span class="ic">{icon('mail')}</span><div><b>E-post</b><a href="mailto:{CO['email']}">{CO['email']}</a></div></li>
<li><span class="ic">{icon('pin')}</span><div><b>Adress</b><a href="{MAPS}" target="_blank" rel="noopener">{CO['street']}, {CO['zip']} {CO['city']}</a></div></li>
</ul>"""


def picture(name, alt, w, h, cls="", eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source srcset="{{p}}img/{name}.webp" type="image/webp">'
            f'<img{c} src="{{p}}img/{name}.jpg" alt="{alt}" width="{w}" height="{h}" {load} decoding="async"></picture>')


BUILDING_ALT = "Nyberg &amp; Karlsons Elektriska AB:s kontorsbyggnad med företagsskylt, med personal och fem servicebilar uppställda framför"
VAN_ALT = "Servicebil med Nyberg &amp; Karlsons logotyp, www.nykael.se, 031-801350 och texten Sedan 1910"


# ------------------------------------------------------------------ startsidan
def page_index():
    p = ""
    hero_cards = "".join(area_card(k, t, s, "#verksamhet", small=True) for k, t, s in [
        ("service", "Servicearbeten", "Vår huvudsakliga verksamhet"),
        ("industri", "Industri", "Installation och service"),
        ("fastighet", "Fastighetsförvaltning", "El i förvaltade fastigheter"),
        ("butik", "Butiker", "El i handelslokaler"),
    ])
    areas = "".join(area_card(k, t, s) for k, t, s in AREAS)
    people = "".join(person_card(x) for x in PEOPLE)
    body = f"""<section class="hero">
<div class="hero-bg">{picture('foretaget-lokaler-servicebilar', '', 800, 452, eager=True)}</div>
<div class="since" aria-hidden="true"><small>Sedan</small>1910</div>
<div class="wrap">
<div class="hero-text">
<span class="eyebrow">Elinstallationer · Göteborg · Sedan 1910</span>
<h1>Elinstallationer i Göteborgsområdet sedan 1910</h1>
<p class="lead">Nyberg &amp; Karlsons Elektriska AB utför främst servicearbeten åt kunder inom industri, fastighetsförvaltning och butiker, men även nyproduktion och ombyggnader.</p>
<div class="btns"><a class="btn btn-white" href="kontakta-oss/#formular">Kontakta oss</a><a class="btn btn-ghost arrow" href="#verksamhet">Vår verksamhet </a></div>
</div>
<div class="hero-cards">{hero_cards}</div>
</div>
</section>

<section class="sec" id="om"><div class="wrap split">
<figure class="media reveal" style="margin:0">{picture('servicebil-dekal', VAN_ALT, 806, 456)}<div class="badge"><small>Sedan</small><b>1910</b></div></figure>
<div class="prose reveal">
<span class="eyebrow">Om företaget</span>
<h2 class="h2">Mer än hundra år av elarbeten i Göteborg</h2>
<p>Nyberg &amp; Karlsons Elektriska AB startades 1910 och har sedan dess utfört elinstallationer i Göteborgsområdet.</p>
<p>Verksamheten består i huvudsak av servicearbeten åt en stor kundkrets inom industri, fastighetsförvaltning och butiker, men även en del nyproduktion och ombyggnader.</p>
<div class="btns"><a class="btn btn-line arrow" href="foretaget/">Läs mer om företaget </a></div>
</div>
</div></section>

<section class="sec gray" id="verksamhet"><div class="wrap">
<div class="sec-head"><div class="prose"><span class="eyebrow">Verksamhet</span><h2 class="h2">Det här arbetar vi med</h2>
<p>Service är kärnan i verksamheten. Vid sidan av den åtar vi oss nyproduktion och ombyggnader.</p></div>
<a class="btn btn-navy" href="kontakta-oss/#formular">Skicka en förfrågan</a></div>
<div class="grid g3 reveal">{areas}</div>
</div></section>

<section class="sec dark" id="varfor"><div class="wrap">
<div class="sec-head"><div class="prose"><span class="eyebrow">Varför Nyberg &amp; Karlsons</span><h2 class="h2">Ett etablerat elföretag i Göteborg</h2></div></div>
<div class="facts reveal">
<div class="fact"><div class="num">1910</div><h3>Lång erfarenhet</h3><p>Företaget har utfört elinstallationer i Göteborgsområdet sedan starten 1910.</p></div>
<div class="fact"><div class="num word">Service</div><h3>Service i fokus</h3><p>Huvuddelen av verksamheten består av servicearbeten åt en stor kundkrets.</p></div>
<div class="fact"><div class="num word">Industri, fastighet &amp; butik</div><h3>En bred kundkrets</h3><p>Vi arbetar åt kunder inom industri, fastighetsförvaltning och butiker.</p></div>
</div>
</div></section>

<section class="sec" id="projektledare"><div class="wrap">
<div class="sec-head"><div class="prose"><span class="eyebrow">Personal</span><h2 class="h2">Kontakta våra projektledare</h2>
<p>Ring eller mejla direkt till någon av våra projektledare, eller kontakta växeln på <a href="tel:{CO['tel']}">{CO['phone']}</a>.</p></div></div>
<div class="grid g2 reveal">{people}</div>
</div></section>

<section class="band">{picture('foretaget-lokaler-servicebilar', '', 800, 452)}<div class="wrap split">
<div class="prose"><span class="eyebrow">Kontakt</span><h2 class="h2">Behöver ni hjälp med el?</h2>
<p>Berätta vad som ska göras så återkommer vi. Ni når oss enklast på telefon eller e-post.</p>
<div class="btns"><a class="btn btn-white" href="tel:{CO['tel']}">Ring {CO['phone']}</a><a class="btn btn-ghost arrow" href="kontakta-oss/#formular">Skicka en förfrågan </a></div></div>
</div></section>
"""
    return (head(p, "Elinstallationer i Göteborg sedan 1910 | Nyberg & Karlsons Elektriska AB",
                 "Nyberg & Karlsons Elektriska AB utför elinstallationer i Göteborgsområdet sedan 1910. Främst servicearbeten åt industri, fastighetsförvaltning och butiker.",
                 "/", schema()) + nav(p, "start") + body.replace("{p}", p) + foot(p))


# ------------------------------------------------------------------ Företaget
def page_foretaget():
    p = "../"
    checks = "".join(f'<li class="chk">{t}</li>' for _, t, _ in AREAS)
    body = f"""<section class="hero no-cards">
<div class="hero-bg">{picture('foretaget-lokaler-servicebilar', '', 800, 452, eager=True)}</div>
<div class="wrap"><div class="hero-text">
<span class="eyebrow">Företaget</span>
<h1>Om Nyberg &amp; Karlsons Elektriska AB</h1>
<p class="lead">Ett elföretag i Göteborg som har utfört elinstallationer i Göteborgsområdet sedan 1910.</p>
</div></div>
</section>

<section class="sec"><div class="wrap split">
<div class="prose reveal">
<span class="eyebrow">Sedan 1910</span>
<h2 class="h2">Elinstallationer i Göteborgsområdet i mer än hundra år</h2>
<p>Nyberg &amp; Karlsons Elektriska AB startades 1910 och har sedan dess utfört elinstallationer i Göteborgsområdet.</p>
<p>Verksamheten består i huvudsak av servicearbeten åt en stor kundkrets inom industri, fastighetsförvaltning och butiker, men även en del nyproduktion och ombyggnader.</p>
</div>
<figure class="media reveal" style="margin:0">{picture('foretaget-lokaler-servicebilar', BUILDING_ALT, 800, 452)}<figcaption>Företagets lokaler och servicebilar.</figcaption></figure>
</div></section>

<section class="sec gray"><div class="wrap split top">
<div class="prose reveal">
<span class="eyebrow">Verksamhet</span>
<h2 class="h2">Service i första hand</h2>
<p>Det mesta vi gör är servicearbeten åt en stor kundkrets. Vid sidan av servicen utför vi även en del nyproduktion och ombyggnader.</p>
<ul class="checklist cols" style="margin-top:8px">{checks}</ul>
</div>
<div class="prose reveal">
<span class="eyebrow">Kunder</span>
<h2 class="h2">Vilka vi arbetar åt</h2>
<div class="grid" style="gap:16px;margin-top:6px">
{area_card('industri', 'Industri', 'Elinstallationer och service i industrins lokaler och anläggningar.', small=True)}
{area_card('fastighet', 'Fastighetsförvaltning', 'Elarbeten åt fastighetsförvaltare och fastighetsägare.', small=True)}
{area_card('butik', 'Butiker', 'Elinstallationer och service i butiker och handelslokaler.', small=True)}
</div>
</div>
</div></section>

<section class="sec dark"><div class="wrap split">
<div class="prose reveal"><span class="eyebrow">Kontakt</span><h2 class="h2">Kom i kontakt med oss</h2>
<p>Ring växeln, mejla eller kontakta någon av våra projektledare direkt.</p>
<div class="btns"><a class="btn btn-white" href="../kontakta-oss/">Kontakta oss</a><a class="btn btn-ghost arrow" href="../kontakta-oss/#projektledare">Våra projektledare </a></div></div>
<div class="reveal">{contact_list(dark=True)}</div>
</div></section>
"""
    return (head(p, "Företaget – elföretag i Göteborg sedan 1910 | Nyberg & Karlsons Elektriska AB",
                 "Nyberg & Karlsons Elektriska AB startades 1910 och utför elinstallationer i Göteborgsområdet, främst servicearbeten åt industri, fastighetsförvaltning och butiker.",
                 "/foretaget/") + nav(p, "foretaget") + body.replace("{p}", p) + foot(p))


# ------------------------------------------------------------------ Kontakta oss
def page_kontakt():
    p = "../"
    people = "".join(person_card(x) for x in PEOPLE)
    hero_cards = f"""<a class="card icon" href="tel:{CO['tel']}"><div class="ic">{icon('phone')}</div><div class="row">Ring oss<small>{CO['phone']}</small></div></a>
<a class="card icon" href="mailto:{CO['email']}"><div class="ic">{icon('mail')}</div><div class="row">Mejla oss<small>{CO['email']}</small></div></a>
<a class="card icon" href="#adress"><div class="ic">{icon('pin')}</div><div class="row">Adress<small>{CO['street']}, {CO['city']}</small></div></a>
<a class="card icon" href="#projektledare"><div class="ic">{icon('people')}</div><div class="row">Projektledare<small>Kontakta dem direkt</small></div></a>"""
    options = "".join(f"<option>{o}</option>" for o in
                      ["Service / felsökning", "Industri", "Fastighetsförvaltning", "Butik", "Nyproduktion", "Ombyggnad", "Annat"])
    body = f"""<section class="hero">
<div class="hero-bg">{picture('servicebil-dekal', '', 806, 456, eager=True)}</div>
<div class="wrap">
<div class="hero-text">
<span class="eyebrow">Kontakta oss</span>
<h1>Kontakta Nyberg &amp; Karlsons Elektriska</h1>
<p class="lead">Ring, mejla eller skicka en förfrågan. Ni kan också vända er direkt till någon av våra projektledare.</p>
</div>
<div class="hero-cards">{hero_cards}</div>
</div>
</section>

<section class="sec" id="projektledare"><div class="wrap">
<div class="sec-head"><div class="prose"><span class="eyebrow">Personal</span><h2 class="h2">Våra projektledare</h2>
<p>Kontakta våra projektledare direkt på mobil eller e-post.</p></div></div>
<div class="grid g2 reveal">{people}</div>
</div></section>

<section class="sec gray" id="formular"><div class="wrap split top">
<div class="prose reveal">
<span class="eyebrow">Förfrågan</span>
<h2 class="h2">Berätta vad ni behöver hjälp med</h2>
<p>Beskriv kort vad som ska göras och var. Uppge gärna företag och telefonnummer så att vi enkelt kan nå er.</p>
{contact_list()}
</div>
<form class="form reveal" id="kontaktform" data-to="{CO['email']}" novalidate>
<div class="two"><label for="f-namn">Namn<input id="f-namn" name="namn" autocomplete="name" required></label>
<label for="f-foretag"><span>Företag <span class="opt">(valfritt)</span></span><input id="f-foretag" name="foretag" autocomplete="organization"></label></div>
<div class="two"><label for="f-epost">E-post<input id="f-epost" name="epost" type="email" autocomplete="email"></label>
<label for="f-tel">Telefon<input id="f-tel" name="telefon" type="tel" autocomplete="tel"></label></div>
<label for="f-arende">Ärende<select id="f-arende" name="arende">{options}</select></label>
<label for="f-medd">Meddelande<textarea id="f-medd" name="meddelande" required></textarea></label>
<button class="btn btn-navy" type="submit">Skicka förfrågan</button>
<p class="note">När du skickar öppnas ditt e-postprogram med meddelandet ifyllt till {CO['email']}. Du kan också ringa oss på {CO['phone']}.</p>
<p class="msg" role="status" aria-live="polite"></p>
</form>
</div></section>

<section class="sec" id="adress"><div class="wrap split">
<div class="prose reveal"><span class="eyebrow">Adress</span><h2 class="h2">{CO['street']}, Göteborg</h2>
<p>{escape(CO['name'])}<br>{CO['street']}<br>{CO['zip']} {CO['city']}</p>
<div class="btns"><a class="btn btn-line arrow" href="{MAPS}" target="_blank" rel="noopener">Öppna i Google Maps </a></div></div>
<figure class="media reveal" style="margin:0">{picture('servicebil-dekal', VAN_ALT, 806, 456)}</figure>
</div></section>
"""
    return (head(p, "Kontakta oss | Nyberg & Karlsons Elektriska AB, Göteborg",
                 "Kontakta Nyberg & Karlsons Elektriska AB på 031-80 13 50 eller mail@nykael.se. Norra Ågatan 10, Göteborg. Kontaktuppgifter till våra projektledare.",
                 "/kontakta-oss/", schema()) + nav(p, "kontakt") + body.replace("{p}", p) + foot(p))


# ------------------------------------------------------------------ 404
def page_404():
    # 404-sidan kan visas på vilken adress som helst, därför absoluta sökvägar
    p = "/"
    body = f"""<section class="hero no-cards"><div class="hero-bg"></div><div class="wrap"><div class="hero-text">
<span class="eyebrow">404</span><h1>Sidan kunde inte hittas</h1>
<p class="lead">Adressen finns inte, eller så har sidan flyttats.</p>
<div class="btns"><a class="btn btn-white" href="/">Till startsidan</a><a class="btn btn-ghost arrow" href="/kontakta-oss/">Kontakta oss </a></div>
</div></div></section>"""
    html = head(p, "Sidan kunde inte hittas | Nyberg & Karlsons Elektriska AB", "Sidan kunde inte hittas.", "/404.html",
                '<meta name="robots" content="noindex">\n') + nav(p, "") + body + foot(p)
    return html.replace('href="/index.html', 'href="/')


def main():
    out = {
        "index.html": page_index(),
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
    urls = "".join(f"  <url><loc>{SITE_URL}{u}</loc></url>\n" for u in ["/", "/foretaget/", "/kontakta-oss/"])
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")


if __name__ == "__main__":
    main()
