# Nya nykael.se – Nyberg & Karlsons Elektriska AB

Statisk webbplats byggd i samma stil som nya Bloms El & Data (fotohero med överlappande kort, färgad navbar,
Poppins, växlande vita/ljusgrå sektioner och färgad sidfot), men med Nyberg & Karlsons egna färger ur logotypen:
marinblått, ljusblått och vinrött.

All fakta kommer från nykael.se: startsidan, *Företaget*, *Kontakta oss* och WordPress-mediabiblioteket.

## Struktur

- `site/build.py` genererar alla sidor: `python3 site/build.py`
- `site/assets/style.css` designsystemet, `site/assets/main.js` mobilmeny, kontaktformulär och inglidning
- `site/img/` logotyp och bilder hämtade från nykael.se

Sidorna ligger på samma adresser som tidigare, så gamla länkar fungerar: `/`, `/foretaget/`, `/kontakta-oss/`.
Dessutom `404.html`, `robots.txt` och `sitemap.xml`. Publicera innehållet i `site/` som webbplatsens rot.

## Bilder och logotyp

| Fil | Källa |
| --- | --- |
| `logo-nyberg-karlsons.png`, `logo-nyberg-karlsons-vit.png` | `cropped-nykael-logga.jpg`, frilagd till transparent PNG (färg och vit) |
| `logo-original.jpg` | originalfilen, sparad som referens |
| `foretaget-lokaler-servicebilar.*` | `start.jpg` (byggnad med skylt, servicebilar och personal), uppskalad 2× |
| `servicebil-dekal.*` | `Nok-nya-logga-bil20.jpg` (logotypen på en servicebil), uppskalad 2× |
| `favicon.png`, `apple-touch-icon.png`, `og-bild.jpg` | gjorda av logotypen och `start.jpg` |

Originalbilderna är små (ca 400 px breda). Skicka gärna större foton på personal, bilar och arbeten så blir sajten skarpare.

## Kontaktformuläret

Utan backend öppnar formuläret ett ifyllt mejl till mail@nykael.se, och det står tydligt på sidan.
Vill ni ta emot förfrågningar direkt: lägg till `data-endpoint="https://formspree.io/f/…"` (eller motsvarande
tjänst) på `<form id="kontaktform">` i `build.py`, så skickas formuläret med `fetch` i stället.

## Att kontrollera och komplettera

- **Reine Ekstorm** stavas så på nuvarande sajt. Kontrollera om det ska vara *Ekström*.
- På gamla sajten hade mejllänken till Mikael Nyberg ett mellanslag (`mailto:%20mikael…`), vilket är rättat här.
- I mediabiblioteket finns logotyper för Installatörsföretagen (medlem, 2018), EIO och ID06, men de visas inte på
  nuvarande sajt. De är inte med eftersom medlemskapen inte går att bekräfta därifrån. Lägg till dem om de gäller.
- Det finns inga publicerade projekt eller referenser, därför har sajten ingen projektsektion. Den kan läggas till
  när det finns verkligt material.
- Org.nr och eventuella sociala kanaler fanns inte på sajten och är inte med.
