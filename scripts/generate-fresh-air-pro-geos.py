#!/usr/bin/env python3
"""Generate Fresh Air Pro landing + thank-you pages for all geos."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES_DIR = ROOT / "scripts" / "fresh-air-pro-locales"
TEMPLATE_LANDING = ROOT / "it" / "fresh-air-pro" / "landing.html"
TEMPLATE_TY = ROOT / "it" / "hypertrimmer" / "thank-you.html"

POPUP_IMAGES = [
    "/assets/img/reviews/fresh-air-pro/popup-3.webp",
    "/assets/img/reviews/fresh-air-pro/popup-4.webp",
    "/assets/img/reviews/fresh-air-pro/popup-1.webp",
    "/assets/img/reviews/fresh-air-pro/popup-2.webp",
    "/assets/img/reviews/fresh-air-pro/popup-3.webp",
    "/assets/img/reviews/fresh-air-pro/popup-4.webp",
    "/assets/img/reviews/fresh-air-pro/popup-1.webp",
    "/assets/img/reviews/fresh-air-pro/popup-2.webp",
]

THANK_YOU = {
    "it": {
        "title": "Ordine ricevuto — Attendi la chiamata di conferma | Fresh Air Pro",
        "description": "Il tuo ordine Fresh Air Pro è stato registrato. Manca solo un ultimo passaggio: rispondi alla chiamata di conferma.",
        "headline": "Il tuo ordine è stato registrato con successo!",
        "subhead": "Perfetto — il tuo ordine è in elaborazione. Manca solo <strong>un ultimo passaggio</strong> per completarlo e far partire la spedizione.",
        "action_eyebrow": "👇 Cosa devi fare adesso",
        "action_title": "📞 Rispondi alla chiamata di conferma",
        "action_body": "Un nostro operatore ti contatterà <strong>nelle prossime ore</strong> per confermare il tuo ordine.",
        "action_warning": "Se non rispondi alla chiamata, l'ordine verrà automaticamente annullato.",
        "hours_heading": "🕒 Orari di contatto",
        "hours_line": "<strong>Lunedì – Sabato</strong> · 9:00 – 18:00",
        "steps_heading": "📋 Cosa succede dopo",
        "steps": [
            "Rispondi alla chiamata e <strong>conferma i tuoi dati</strong>",
            "Il tuo ordine verrà spedito entro <strong>24–48 ore</strong>",
            "Consegna a domicilio e <strong>pagamento alla consegna</strong>",
        ],
        "badges": ["🔒 Pagamento alla consegna", "🛡️ Garanzia 24 mesi", "🔐 Protezione SSL"],
    },
    "de": {
        "title": "Bestellung erhalten — Warten Sie auf den Bestätigungsanruf | Fresh Air Pro",
        "description": "Ihre Fresh Air Pro Bestellung wurde registriert. Ein letzter Schritt: Nehmen Sie den Bestätigungsanruf entgegen.",
        "headline": "Ihre Bestellung wurde erfolgreich registriert!",
        "subhead": "Perfekt — Ihre Bestellung wird bearbeitet. Es fehlt nur noch <strong>ein letzter Schritt</strong>, um sie abzuschließen und den Versand zu starten.",
        "action_eyebrow": "👇 Was Sie jetzt tun müssen",
        "action_title": "📞 Nehmen Sie den Bestätigungsanruf entgegen",
        "action_body": "Ein Mitarbeiter wird Sie <strong>in den nächsten Stunden</strong> kontaktieren, um Ihre Bestellung zu bestätigen.",
        "action_warning": "Wenn Sie den Anruf nicht annehmen, wird die Bestellung automatisch storniert.",
        "hours_heading": "🕒 Kontaktzeiten",
        "hours_line": "<strong>Montag – Samstag</strong> · 9:00 – 18:00",
        "steps_heading": "📋 Was als Nächstes passiert",
        "steps": [
            "Nehmen Sie den Anruf an und <strong>bestätigen Sie Ihre Daten</strong>",
            "Ihre Bestellung wird innerhalb von <strong>24–48 Stunden</strong> versendet",
            "Lieferung nach Hause und <strong>Zahlung bei Lieferung</strong>",
        ],
        "badges": ["🔒 Zahlung bei Lieferung", "🛡️ 24 Monate Garantie", "🔐 SSL-Schutz"],
    },
    "es": {
        "title": "Pedido recibido — Espera la llamada de confirmación | Fresh Air Pro",
        "description": "Tu pedido de Fresh Air Pro ha sido registrado. Falta un último paso: responde a la llamada de confirmación.",
        "headline": "¡Tu pedido se ha registrado correctamente!",
        "subhead": "Perfecto — tu pedido está en proceso. Solo falta <strong>un último paso</strong> para completarlo y enviarlo.",
        "action_eyebrow": "👇 Qué debes hacer ahora",
        "action_title": "📞 Responde a la llamada de confirmación",
        "action_body": "Un operador te contactará <strong>en las próximas horas</strong> para confirmar tu pedido.",
        "action_warning": "Si no respondes a la llamada, el pedido se cancelará automáticamente.",
        "hours_heading": "🕒 Horario de contacto",
        "hours_line": "<strong>Lunes – Sábado</strong> · 9:00 – 18:00",
        "steps_heading": "📋 Qué ocurre después",
        "steps": [
            "Responde a la llamada y <strong>confirma tus datos</strong>",
            "Tu pedido se enviará en <strong>24–48 horas</strong>",
            "Entrega a domicilio y <strong>pago contra reembolso</strong>",
        ],
        "badges": ["🔒 Pago contra reembolso", "🛡️ Garantía 24 meses", "🔐 Protección SSL"],
    },
    "pt": {
        "title": "Encomenda recebida — Aguarde a chamada de confirmação | Fresh Air Pro",
        "description": "A sua encomenda Fresh Air Pro foi registada. Falta um último passo: atenda à chamada de confirmação.",
        "headline": "A sua encomenda foi registada com sucesso!",
        "subhead": "Perfeito — a sua encomenda está a ser processada. Falta apenas <strong>um último passo</strong> para a concluir e iniciar o envio.",
        "action_eyebrow": "👇 O que deve fazer agora",
        "action_title": "📞 Atenda à chamada de confirmação",
        "action_body": "Um operador irá contactá-lo <strong>nas próximas horas</strong> para confirmar a encomenda.",
        "action_warning": "Se não atender à chamada, a encomenda será cancelada automaticamente.",
        "hours_heading": "🕒 Horário de contacto",
        "hours_line": "<strong>Segunda – Sábado</strong> · 9:00 – 18:00",
        "steps_heading": "📋 O que acontece a seguir",
        "steps": [
            "Atenda à chamada e <strong>confirme os seus dados</strong>",
            "A encomenda será enviada em <strong>24–48 horas</strong>",
            "Entrega ao domicílio e <strong>pagamento na entrega</strong>",
        ],
        "badges": ["🔒 Pagamento na entrega", "🛡️ Garantia 24 meses", "🔐 Proteção SSL"],
    },
    "pl": {
        "title": "Zamówienie przyjęte — Oczekuj na telefon potwierdzający | Fresh Air Pro",
        "description": "Twoje zamówienie Fresh Air Pro zostało zarejestrowane. Brakuje ostatniego kroku: odbierz telefon potwierdzający.",
        "headline": "Twoje zamówienie zostało pomyślnie zarejestrowane!",
        "subhead": "Świetnie — zamówienie jest w realizacji. Brakuje tylko <strong>ostatniego kroku</strong>, aby je sfinalizować i wysłać przesyłkę.",
        "action_eyebrow": "👇 Co musisz teraz zrobić",
        "action_title": "📞 Odbierz telefon potwierdzający",
        "action_body": "Nasz konsultant skontaktuje się z Tobą <strong>w ciągu najbliższych godzin</strong>, aby potwierdzić zamówienie.",
        "action_warning": "Jeśli nie odbierzesz telefonu, zamówienie zostanie automatycznie anulowane.",
        "hours_heading": "🕒 Godziny kontaktu",
        "hours_line": "<strong>Poniedziałek – Sobota</strong> · 9:00 – 18:00",
        "steps_heading": "📋 Co dzieje się dalej",
        "steps": [
            "Odbierz telefon i <strong>potwierdź swoje dane</strong>",
            "Zamówienie zostanie wysłane w ciągu <strong>24–48 godzin</strong>",
            "Dostawa do domu i <strong>płatność przy odbiorze</strong>",
        ],
        "badges": ["🔒 Płatność przy odbiorze", "🛡️ Garantia 24 miesiące", "🔐 Ochrona SSL"],
    },
    "hu": {
        "title": "Rendelés fogadva — Várja a megerősítő hívást | Fresh Air Pro",
        "description": "Fresh Air Pro rendelését rögzítettük. Még egy lépés: vegye fel a megerősítő hívást.",
        "headline": "Rendelését sikeresen rögzítettük!",
        "subhead": "Remek — rendelése feldolgozás alatt van. Már csak <strong>egy utolsó lépés</strong> van hátra a befejezéshez és a szállításhoz.",
        "action_eyebrow": "👇 Mit kell most tennie",
        "action_title": "📞 Vegye fel a megerősítő hívást",
        "action_body": "Munkatársunk <strong>a következő órákban</strong> felhívja a rendelés megerősítéséhez.",
        "action_warning": "Ha nem veszi fel a hívást, a rendelés automatikusan törlődik.",
        "hours_heading": "🕒 Elérhetőség",
        "hours_line": "<strong>Hétfő – Szombat</strong> · 9:00 – 18:00",
        "steps_heading": "📋 Mi történik ezután",
        "steps": [
            "Vegye fel a hívást és <strong>erősítse meg adatait</strong>",
            "Rendelését <strong>24–48 órán</strong> belül feladjuk",
            "Házhozszállítás és <strong>utánvét</strong>",
        ],
        "badges": ["🔒 Utánvét", "🛡️ 24 hónap garancia", "🔐 SSL védelem"],
    },
    "ro": {
        "title": "Comandă primită — Așteptați apelul de confirmare | Fresh Air Pro",
        "description": "Comanda Fresh Air Pro a fost înregistrată. Mai lipsește un pas: răspundeți la apelul de confirmare.",
        "headline": "Comanda dvs. a fost înregistrată cu succes!",
        "subhead": "Perfect — comanda este în procesare. Mai lipsește doar <strong>un ultim pas</strong> pentru a o finaliza și a trimite livrarea.",
        "action_eyebrow": "👇 Ce trebuie să faceți acum",
        "action_title": "📞 Răspundeți la apelul de confirmare",
        "action_body": "Un operator vă va contacta <strong>în următoarele ore</strong> pentru a confirma comanda.",
        "action_warning": "Dacă nu răspundeți la apel, comanda va fi anulată automat.",
        "hours_heading": "🕒 Program de contact",
        "hours_line": "<strong>Luni – Sâmbătă</strong> · 9:00 – 18:00",
        "steps_heading": "📋 Ce urmează",
        "steps": [
            "Răspundeți la apel și <strong>confirmați datele</strong>",
            "Comanda va fi expediată în <strong>24–48 de ore</strong>",
            "Livrare la domiciliu și <strong>plată la livrare</strong>",
        ],
        "badges": ["🔒 Plată la livrare", "🛡️ Garanție 24 luni", "🔐 Protecție SSL"],
    },
    "hr": {
        "title": "Narudžba primljena — Pričekajte poziv za potvrdu | Fresh Air Pro",
        "description": "Vaša narudžba Fresh Air Pro je registrirana. Još jedan korak: odgovorite na poziv za potvrdu.",
        "headline": "Vaša narudžba je uspješno registrirana!",
        "subhead": "Odlično — narudžba je u obradi. Ostao je samo <strong>posljednji korak</strong> za dovršetak i slanje.",
        "action_eyebrow": "👇 Što trebate učiniti sada",
        "action_title": "📞 Odgovorite na poziv za potvrdu",
        "action_body": "Naš operater će vas kontaktirati <strong>u sljedećim satima</strong> radi potvrde narudžbe.",
        "action_warning": "Ako ne odgovorite na poziv, narudžba će se automatski otkazati.",
        "hours_heading": "🕒 Radno vrijeme",
        "hours_line": "<strong>Ponedjeljak – Subota</strong> · 9:00 – 18:00",
        "steps_heading": "📋 Što slijedi",
        "steps": [
            "Odgovorite na poziv i <strong>potvrdite svoje podatke</strong>",
            "Narudžba će biti poslana u roku od <strong>24–48 sati</strong>",
            "Dostava na kućnu adresu i <strong>plaćanje pouzećem</strong>",
        ],
        "badges": ["🔒 Plaćanje pouzećem", "🛡️ Jamstvo 24 mjeseca", "🔐 SSL zaštita"],
    },
    "sk": {
        "title": "Objednávka prijatá — Čakajte na potvrdzovací hovor | Fresh Air Pro",
        "description": "Vaša objednávka Fresh Air Pro bola zaregistrovaná. Chýba posledný krok: zdvihnite potvrdzovací hovor.",
        "headline": "Vaša objednávka bola úspešne zaregistrovaná!",
        "subhead": "Výborne — objednávka sa spracováva. Zostáva už len <strong>posledný krok</strong> na dokončenie a odoslanie.",
        "action_eyebrow": "👇 Čo musíte urobiť teraz",
        "action_title": "📞 Zdvihnite potvrdzovací hovor",
        "action_body": "Náš operátor vás bude kontaktovať <strong>v najbližších hodinách</strong> na potvrdenie objednávky.",
        "action_warning": "Ak nezdvihnete hovor, objednávka sa automaticky zruší.",
        "hours_heading": "🕒 Kontaktné hodiny",
        "hours_line": "<strong>Pondelok – Sobota</strong> · 9:00 – 18:00",
        "steps_heading": "📋 Čo bude nasledovať",
        "steps": [
            "Zdvihnite hovor a <strong>potvrďte svoje údaje</strong>",
            "Objednávka bude odoslaná do <strong>24–48 hodín</strong>",
            "Doručenie domov a <strong>platba na dobierku</strong>",
        ],
        "badges": ["🔒 Platba na dobierku", "🛡️ Záruka 24 mesiacov", "🔐 SSL ochrana"],
    },
    "si": {
        "title": "Naročilo prejeto — Počakajte na potrditveni klic | Fresh Air Pro",
        "description": "Vaše naročilo Fresh Air Pro je registrirano. Manjka še zadnji korak: sprejmite potrditveni klic.",
        "headline": "Vaše naročilo je bilo uspešno registrirano!",
        "subhead": "Odlično — naročilo je v obdelavi. Manjka le še <strong>zadnji korak</strong> za dokončanje in odpošiljanje.",
        "action_eyebrow": "👇 Kaj morate storiti zdaj",
        "action_title": "📞 Sprejmite potrditveni klic",
        "action_body": "Naš operater vas bo kontaktiral <strong>v naslednjih urah</strong> za potrditev naročila.",
        "action_warning": "Če ne sprejmete klica, bo naročilo samodejno preklicano.",
        "hours_heading": "🕒 Kontaktni čas",
        "hours_line": "<strong>Ponedeljek – Sobota</strong> · 9:00 – 18:00",
        "steps_heading": "📋 Kaj sledi",
        "steps": [
            "Sprejmite klic in <strong>potrdite svoje podatke</strong>",
            "Naročilo bo odposlano v <strong>24–48 urah</strong>",
            "Dostava na dom in <strong>plačilo ob prevzemu</strong>",
        ],
        "badges": ["🔒 Plačilo ob prevzemu", "🛡️ Garancija 24 mesecev", "🔐 SSL zaščita"],
    },
    "cz": {
        "title": "Objednávka přijata — Vyčkejte na potvrzovací hovor | Fresh Air Pro",
        "description": "Vaše objednávka Fresh Air Pro byla zaregistrována. Chybí poslední krok: zvedněte potvrzovací hovor.",
        "headline": "Vaše objednávka byla úspěšně zaregistrována!",
        "subhead": "Skvělé — objednávka se zpracovává. Zbývá už jen <strong>poslední krok</strong> k dokončení a odeslání.",
        "action_eyebrow": "👇 Co musíte udělat nyní",
        "action_title": "📞 Zvedněte potvrzovací hovor",
        "action_body": "Náš operátor vás bude kontaktovat <strong>v následujících hodinách</strong> kvůli potvrzení objednávky.",
        "action_warning": "Pokud hovor nezvednete, objednávka bude automaticky zrušena.",
        "hours_heading": "🕒 Kontaktní hodiny",
        "hours_line": "<strong>Pondělí – Sobota</strong> · 9:00 – 18:00",
        "steps_heading": "📋 Co bude následovat",
        "steps": [
            "Zvedněte hovor a <strong>potvrďte své údaje</strong>",
            "Objednávka bude odeslána do <strong>24–48 hodin</strong>",
            "Doručení domů a <strong>platba na dobírku</strong>",
        ],
        "badges": ["🔒 Platba na dobírku", "🛡️ Záruka 24 měsíců", "🔐 SSL ochrana"],
    },
    "lt": {
        "title": "Užsakymas gautas — Laukite patvirtinimo skambučio | Fresh Air Pro",
        "description": "Jūsų Fresh Air Pro užsakymas užregistruotas. Liko paskutinis žingsnis: atsiliepkite į patvirtinimo skambutį.",
        "headline": "Jūsų užsakymas sėkmingai užregistruotas!",
        "subhead": "Puiku — užsakymas tvarkomas. Liko tik <strong>paskutinis žingsnis</strong>, kad jį užbaigtumėte ir pradėtume siuntimą.",
        "action_eyebrow": "👇 Ką daryti dabar",
        "action_title": "📞 Atsiliepkite į patvirtinimo skambutį",
        "action_body": "Mūsų operatorius susisieks su jumis <strong>artimiausiomis valandomis</strong>, kad patvirtintų užsakymą.",
        "action_warning": "Jei neatsiliepsite į skambutį, užsakymas bus automatiškai atšauktas.",
        "hours_heading": "🕒 Kontaktų laikas",
        "hours_line": "<strong>Pirmadienis – Šeštadienis</strong> · 9:00 – 18:00",
        "steps_heading": "📋 Kas bus toliau",
        "steps": [
            "Atsiliepkite į skambutį ir <strong>patvirtinkite savo duomenis</strong>",
            "Užsakymas bus išsiųstas per <strong>24–48 valandas</strong>",
            "Pristatymas į namus ir <strong>mokėjimas pristatymo metu</strong>",
        ],
        "badges": ["🔒 Mokėjimas pristatymo metu", "🛡️ 24 mėn. garantija", "🔐 SSL apsauga"],
    },
    "lv": {
        "title": "Pasūtījums saņemts — Gaidiet apstiprinājuma zvanu | Fresh Air Pro",
        "description": "Jūsu Fresh Air Pro pasūtījums ir reģistrēts. Atlicis pēdējais solis: atbildiet uz apstiprinājuma zvanu.",
        "headline": "Jūsu pasūtījums ir veiksmīgi reģistrēts!",
        "subhead": "Lieliski — pasūtījums tiek apstrādāts. Atlicis tikai <strong>pēdējais solis</strong>, lai to pabeigtu un sāktu piegādi.",
        "action_eyebrow": "👇 Ko darīt tagad",
        "action_title": "📞 Atbildiet uz apstiprinājuma zvanu",
        "action_body": "Mūsu operators sazināsies ar jums <strong>tuvākajās stundās</strong>, lai apstiprinātu pasūtījumu.",
        "action_warning": "Ja neatbildēsiet uz zvanu, pasūtījums tiks automātiski atcelts.",
        "hours_heading": "🕒 Kontakta laiks",
        "hours_line": "<strong>Pirmdiena – Sestdiena</strong> · 9:00 – 18:00",
        "steps_heading": "📋 Kas notiks tālāk",
        "steps": [
            "Atbildiet uz zvanu un <strong>apstipriniet savus datus</strong>",
            "Pasūtījums tiks nosūtīts <strong>24–48 stundu</strong> laikā",
            "Piegāde uz mājām un <strong>apmaksa piegādes brīdī</strong>",
        ],
        "badges": ["🔒 Apmaksa piegādes brīdī", "🛡️ 24 mēnešu garantija", "🔐 SSL aizsardzība"],
    },
}


def popup_json(locale: dict) -> str:
    items = []
    for i, p in enumerate(locale["popup_purchases"]):
        img = POPUP_IMAGES[i % len(POPUP_IMAGES)]
        items.append(
            f'  {{ "initial": "{p["initial"]}", "name": "{p["name"]}", '
            f'"image": "{img}", "message": "{p["message"]}", "time": "{p["time"]}" }}'
        )
    return "[\n" + ",\n".join(items) + "\n]"


def site_config_block(geo: str, locale: dict, landing: dict) -> str:
    price = float(landing["meta"]["price"])
    currency = landing["meta"]["currency"]
    suffix = locale["offer_name_suffix"]
    offer_id = locale["offer_id"]
    cookie = locale["cookie"]
    return f"""window.SITE_CONFIG = {{
  GEO: '{geo}',
  PRODUCT_SLUG: 'fresh-air-pro',
  CURRENCY: '{currency}',
  PRICE: {price},
  OFFER_ID: '{offer_id}',
  OFFER_NAME: 'Fresh Air Pro {suffix}',
  LP_ID: '{geo}-fresh-air-pro-v1',
  META_PIXEL_ID: '',
  GOOGLE_TAG_ID: '',
  GOOGLE_ADS_CONVERSION_ID: '',
  GOOGLE_ADS_CONVERSION_LABEL: '',
  TY_CONVERSION_LABEL: '',
  NETWORK_PIXEL_URL: '',
  FORM_ENDPOINT: 'https://TODO-network-endpoint.com/api/lead',
  SUBMITTING_LABEL: '{landing["form"]["submitting_label"]}',
  COOKIE_TEXT: '{cookie["text"].replace("'", "\\'")}',
  COOKIE_ACCEPT: '{cookie["accept"]}',
  COOKIE_LEARN: '{cookie["learn"]}'
}};"""


def price_display(landing: dict) -> dict:
    p = landing["price"]
    cur = p.get("currency", "€")
    anchor = p["anchor"]
    final = p["final"]
    return {
        "old": f"{anchor} {cur}".strip(),
        "new": f"{final} {cur}".strip(),
        "amount": final.split(",")[0] if "," in final else final.split()[0],
        "cta": landing["form"]["cta_button"],
        "discount_line": landing.get("incentive_2", {}).get("text", ""),
        "limited_old": f"{anchor} {cur}".strip(),
        "limited_discount": landing.get("banner_urgency", {}).get("main", ""),
    }


def generate_landing_html(geo: str, locale: dict) -> str:
    landing = locale["landing"]
    prices = price_display(landing)
    offer_id = locale["offer_id"]
    base = f"https://seogigstore.com/{geo}/fresh-air-pro/landing.html?offer_id={offer_id}"
    html = TEMPLATE_LANDING.read_text(encoding="utf-8")

    html = html.replace('lang="it"', f'lang="{locale["html_lang"]}"')
    html = html.replace(
        'data-lp-json="/content/it/products/fresh-air-pro/landing.json"',
        f'data-lp-json="/content/{geo}/products/fresh-air-pro/landing.json"',
    )
    html = re.sub(r"<title>.*?</title>", f"<title>{landing['meta']['title']}</title>", html, count=1)
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{landing["meta"]["description"]}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<link rel="canonical" href="[^"]*">',
        f'<link rel="canonical" href="{base}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">',
        f'<link rel="alternate" hreflang="{geo}" href="{base}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{landing["meta"]["title"][:120]}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{landing["meta"]["description"]}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:url" content="[^"]*">',
        f'<meta property="og:url" content="{base}">',
        html,
        count=1,
    )
    html = html.replace("/it/", f"/{geo}/")
    html = re.sub(
        r'"url": "https://seogigstore\.com/[^"]*fresh-air-pro/landing\.html[^"]*"',
        f'"url": "{base}"',
        html,
        count=1,
    )

    # ld+json
    html = re.sub(
        r'"price": "[^"]*"',
        f'"price": "{landing["meta"]["price"]}"',
        html,
        count=1,
    )
    html = re.sub(
        r'"priceCurrency": "[^"]*"',
        f'"priceCurrency": "{landing["meta"]["currency"]}"',
        html,
        count=1,
    )
    desc_escaped = landing["meta"]["description"].replace('"', '\\"')
    html = re.sub(
        r'"description": "[^"]*"',
        f'"description": "{desc_escaped}"',
        html,
        count=1,
    )

    # SITE_CONFIG + POPUP
    html = re.sub(
        r"window\.SITE_CONFIG = \{[\s\S]*?\};",
        site_config_block(geo, locale, landing),
        html,
        count=1,
    )
    html = re.sub(
        r"window\.POPUP_PURCHASES = \[[\s\S]*?\];",
        f"window.POPUP_PURCHASES = {popup_json(locale)};",
        html,
        count=1,
    )

    if 'package-content__list--inline-icons' not in html:
        html = html.replace(
            '<ul class="package-content__list">',
            '<ul class="package-content__list package-content__list--inline-icons">',
        )

    # footer labels
    ft = locale["footer"]
    html = html.replace("Informazioni", ft["info_heading"])
    html = html.replace("Contatti", ft["contact_heading"])
    html = html.replace("Chi siamo", ft["about"])
    html = html.replace("Contattaci", ft["contact"])
    html = html.replace("Privacy Policy", ft["privacy"])
    html = html.replace("Termini e Condizioni", ft["terms"])
    html = html.replace("Cookie Policy", ft["cookies"])
    html = html.replace("Politica di Spedizione", ft["shipping"])
    html = html.replace("Politica di Rimborso", ft["refund"])
    html = html.replace("Tutti i diritti riservati.", ft["rights"])

    if landing.get("footer", {}).get("tagline"):
        html = re.sub(
            r'<p style="margin-top:1rem;max-width:340px">[^<]*</p>',
            f'<p style="margin-top:1rem;max-width:340px">{landing["footer"]["tagline"]}</p>',
            html,
            count=1,
        )

    return html


def generate_thank_you_html(geo: str, locale: dict) -> str:
    landing = locale["landing"]
    ty = THANK_YOU.get(geo, THANK_YOU["it"])
    ft = locale["footer"]
    price = float(landing["meta"]["price"])
    currency = landing["meta"]["currency"]
    html = TEMPLATE_TY.read_text(encoding="utf-8")

    html = html.replace('lang="it"', f'lang="{locale["html_lang"]}"')
    html = re.sub(r"<title>.*?</title>", f"<title>{ty['title']}</title>", html, count=1)
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{ty["description"]}">',
        html,
        count=1,
    )
    html = html.replace("HyperTrimmer™ 3000", "Fresh Air Pro")
    html = html.replace("hypertrimmer", "fresh-air-pro")
    html = html.replace("/it/", f"/{geo}/")

    html = re.sub(
        r"window\.SITE_CONFIG = \{[\s\S]*?\};",
        f"""window.SITE_CONFIG = {{
  GEO: '{geo}',
  PRODUCT_SLUG: 'fresh-air-pro',
  CURRENCY: '{currency}',
  PRICE: {price},
  META_PIXEL_ID: '',
  GOOGLE_TAG_ID: '',
  GOOGLE_ADS_CONVERSION_ID: '',
  TY_CONVERSION_LABEL: '',
  COOKIE_TEXT: '{locale["cookie"]["text"].replace("'", "\\'")}',
  COOKIE_ACCEPT: '{locale["cookie"]["accept"]}',
  COOKIE_LEARN: '{locale["cookie"]["learn"]}'
}};""",
        html,
        count=1,
    )

    html = html.replace(
        "if (window.trackPurchase) window.trackPurchase(79.90, 'EUR');",
        f"if (window.trackPurchase) window.trackPurchase({price}, '{currency}');",
    )

    html = html.replace(
        '<h1 class="ty-headline">Il tuo ordine è stato registrato con successo!</h1>',
        f'<h1 class="ty-headline">{ty["headline"]}</h1>',
    )
    html = re.sub(
        r'<p class="ty-subhead">.*?</p>',
        f'<p class="ty-subhead">{ty["subhead"]}</p>',
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = html.replace(
        '<div class="ty-action__eyebrow">👇 Cosa devi fare adesso</div>',
        f'<div class="ty-action__eyebrow">{ty["action_eyebrow"]}</div>',
    )
    html = html.replace(
        '<h2 class="ty-action__title">📞 Rispondi alla chiamata di conferma</h2>',
        f'<h2 class="ty-action__title">{ty["action_title"]}</h2>',
    )
    html = re.sub(
        r'<p class="ty-action__body">.*?</p>',
        f'<p class="ty-action__body">{ty["action_body"]}</p>',
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = html.replace(
        '<p class="ty-action__warning">Se non rispondi alla chiamata, l\'ordine verrà automaticamente annullato.</p>',
        f'<p class="ty-action__warning">{ty["action_warning"]}</p>',
    )
    html = html.replace(
        '<div class="ty-box__header">🕒 Orari di contatto</div>',
        f'<div class="ty-box__header">{ty["hours_heading"]}</div>',
    )
    html = html.replace(
        '<div class="ty-hours-line"><strong>Lunedì – Sabato</strong> · 9:00 – 18:00</div>',
        f'<div class="ty-hours-line">{ty["hours_line"]}</div>',
    )
    html = html.replace(
        '<div class="ty-box__header">📋 Cosa succede dopo</div>',
        f'<div class="ty-box__header">{ty["steps_heading"]}</div>',
    )

    steps_html = "\n".join(f"        <li>{s}</li>" for s in ty["steps"])
    html = re.sub(
        r"<ol class=\"ty-steps-list\">[\s\S]*?</ol>",
        f"<ol class=\"ty-steps-list\">\n{steps_html}\n      </ol>",
        html,
        count=1,
    )

    badges_html = "\n".join(
        f'    <span class="ty-trust__badge">{b}</span>' for b in ty["badges"]
    )
    html = re.sub(
        r'<div class="ty-trust">[\s\S]*?</div>',
        f'<div class="ty-trust">\n{badges_html}\n  </div>',
        html,
        count=1,
    )

    html = html.replace("Informazioni", ft["info_heading"])
    html = html.replace("Contatti", ft["contact_heading"])
    html = html.replace("Chi siamo", ft["about"])
    html = html.replace("Contattaci", ft["contact"])
    html = html.replace("Privacy Policy", ft["privacy"])
    html = html.replace("Termini e Condizioni", ft["terms"])
    html = html.replace("Cookie Policy", ft["cookies"])
    html = html.replace("Politica di Spedizione", ft["shipping"])
    html = html.replace("Politica di Rimborso", ft["refund"])
    html = html.replace("Tutti i diritti riservati.", ft["rights"])

    return html


def generate_thank_you_json(geo: str, locale: dict) -> dict:
    landing = locale["landing"]
    ty = THANK_YOU.get(geo, THANK_YOU["it"])
    return {
        "meta": {
            "title": ty["title"],
            "description": ty["description"],
            "currency": landing["meta"]["currency"],
            "price": landing["meta"]["price"],
        },
        "headline_warning": {
            "loader_percent": "90%",
            "title": ty["headline"],
            "text": ty["subhead"].replace("<strong>", "").replace("</strong>", ""),
        },
        "next_steps": {
            "title": ty["steps_heading"],
            "subtitle": landing["form"]["title"],
            "steps": [
                {"title": ty["steps"][0], "text": ""},
                {"title": ty["steps"][1], "text": ""},
                {"title": ty["steps"][2], "text": ""},
            ],
        },
        "stock_warning": {
            "icon": "🚨",
            "title": ty["action_title"],
            "text": ty["action_warning"],
        },
        "call_hours": {
            "icon": "🕒",
            "title": ty["hours_heading"],
            "hours": [ty["hours_line"].replace("<strong>", "").replace("</strong>", "")],
            "promise_title": ty["badges"][0],
            "promise_text": landing["form"]["secure_note"],
        },
        "product_recall": {
            "image_alt": "Fresh Air Pro",
            "title": landing["headline"]["title"],
            "text": landing["headline"]["subtitle"],
            "whatsapp_button": "",
            "whatsapp_link": "",
        },
    }


def main() -> None:
    locales = sorted(LOCALES_DIR.glob("*.json"))
    print(f"Generating {len(locales)} geos...")
    for path in locales:
        geo = path.stem
        locale = json.loads(path.read_text(encoding="utf-8"))
        landing = locale["landing"]

        content_dir = ROOT / "content" / geo / "products" / "fresh-air-pro"
        page_dir = ROOT / geo / "fresh-air-pro"
        content_dir.mkdir(parents=True, exist_ok=True)
        page_dir.mkdir(parents=True, exist_ok=True)

        (content_dir / "landing.json").write_text(
            json.dumps(landing, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (content_dir / "thank-you.json").write_text(
            json.dumps(generate_thank_you_json(geo, locale), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (page_dir / "landing.html").write_text(
            generate_landing_html(geo, locale), encoding="utf-8"
        )
        (page_dir / "thank-you.html").write_text(
            generate_thank_you_html(geo, locale), encoding="utf-8"
        )
        print(f"  ✓ {geo} (offer_id={locale['offer_id']})")

    print("Done.")


if __name__ == "__main__":
    main()
