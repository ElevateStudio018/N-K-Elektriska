# Nya nykael.se – Nyberg & Karlsons Elektriska AB

Statisk webbplats med samma tekniska upplägg och kvalitetsnivå som nya Bloms El & Data, men med en egen
formgivning utgången från Nyberg & Karlsons logotyp: vit navbar med logotypen i färg, telefonnummer och
kontaktknapp, marinblå duotonhero med årtalet 1910, numrerade verksamhetskort och logotypens tre linjer
(ljusblå, vinröd, marinblå) som återkommande motiv.

All fakta kommer från nykael.se: startsidan, *Företaget*, *Kontakta oss* och WordPress-mediabiblioteket.

## Struktur

- `site/build.py` genererar alla sidor: `python3 site/build.py`
- `site/assets/style.css` designsystemet, `site/assets/main.js` mobilmeny, kontaktformulär och inglidning
- `site/img/` logotyp och bilder hämtade från nykael.se

Sidorna ligger på samma adresser som tidigare, så gamla länkar fungerar: `/`, `/foretaget/`, `/kontakta-oss/`.
Nytt är `/verksamhet/` med alla verksamhetsområden.
Dessutom `404.html`, `robots.txt` och `sitemap.xml`. Publicera innehållet i `site/` som webbplatsens rot.

## Bilder och logotyp

| Fil | Källa |
| --- | --- |
| `logo-nyberg-karlsons.png`, `logo-nyberg-karlsons-vit.png` | `cropped-nykael-logga.jpg`, frilagd till transparent PNG (färg och vit) |
| `logo-original.jpg` | originalfilen, sparad som referens |
| `foretaget-lokaler-servicebilar.*` | `start.jpg` (byggnad med skylt, servicebilar och personal), uppskalad 2× |
| `servicebil-dekal.*` | `Nok-nya-logga-bil20.jpg` (logotypen på en servicebil), uppskalad 2× |
| `favicon.png`, `apple-touch-icon.png`, `og-bild.jpg` | gjorda av logotypen och `start.jpg` |

### Illustrationsbilder (CC0, ingen attribution krävs)

Nykael.se har bara två foton, så verksamhetsområdena illustreras med fria bilder. De visar **inte** företagets
egna arbeten eller anställda och bör bytas mot egna foton när sådana finns.

| Fil | Källa |
| --- | --- |
| `bild-elservice.*` | Michal Jarmoluk, StockSnap (CC0) https://stocksnap.io/photo/electrician-electricity-QJ55PI34SY |
| `bild-industri-elcentral.*` | Michal Jarmoluk, StockSnap (CC0) https://stocksnap.io/photo/electrician-electricity-3A5FXM89OG |
| `bild-fastighet-kontorshus.*` | Open Grid Scheduler, Flickr (CC0) https://www.flickr.com/photos/29155878@N03/26930332206 |
| `bild-butik-interior.*` | Artem Beliaikin, Flickr (CC0) https://www.flickr.com/photos/157635012@N07/49390481077 |
| `bild-nyproduktion-kabelstegar.*` | Darryl, WordPress Photos (CC0) https://wordpress.org/photos/photo/63761f0310/ |
| `bild-ombyggnad-belysning.*` | YellowstoneNPS, Flickr (Public Domain) https://www.flickr.com/photos/80223459@N05/52653265115 |
| `bild-elcentral-plintar.*` | rawpixel (CC0) https://www.rawpixel.com/image/5904900 |

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
