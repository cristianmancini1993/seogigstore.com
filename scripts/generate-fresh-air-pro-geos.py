#!/usr/bin/env python3
"""Generate Fresh Air Pro landing + thank-you pages for all geos."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES_DIR = ROOT / "scripts" / "fresh-air-pro-locales"
FORMS_PATH = ROOT / "scripts" / "fresh-air-pro-forms.json"
UI_PATH = ROOT / "scripts" / "fresh-air-pro-ui.json"
TEMPLATE_LANDING = ROOT / "scripts" / "templates" / "fresh-air-pro-landing.html"
TEMPLATE_TY = ROOT / "it" / "hypertrimmer" / "thank-you.html"

ADRICE_UID = "018e3961-c73a-7965-8fc1-b1d91c869a42"
ADRICE_ACTION = "https://offers.adricenetwork.com/forms/html/"
ADRICE_WEBHOOK = "https://hook.eu2.make.com/6w6627fflahnsa4qpoqggy993yac0ubz"

GOOGLE_ADS_ID = "AW-18192990064"
GOOGLE_ADS_CONVERSION_SEND_TO = "AW-18192990064/1U2ICLnWpMwcEPD-i-ND"

# Network CPA (EUR) per offer ID — usato come value nella conversione Google Ads
OFFER_CPA = {
    "3990": 14,
    "764": 18,
    "4067": 18,
    "765": 18,
    "1244": 16,
    "1275": 17,
    "2288": 17,
    "1673": 15,
    "1739": 15,
    "2287": 13,
    "1851": 17,
    "2283": 15,
    "2285": 16,
    "2286": 19,
    "2289": 18,
    "2920": 18,
    "3426": 17,
}

# Every network offer ID → geo folder (price/currency from locale landing.json)
OFFERS = [
    {"id": "3990", "geo": "it"},
    {"id": "764", "geo": "sk"},
    {"id": "4067", "geo": "sk"},
    {"id": "765", "geo": "si"},
    {"id": "1244", "geo": "ro"},
    {"id": "1275", "geo": "hu"},
    {"id": "2288", "geo": "hu"},
    {"id": "1673", "geo": "pt"},
    {"id": "1739", "geo": "pl"},
    {"id": "2287", "geo": "pl"},
    {"id": "1851", "geo": "hr"},
    {"id": "2283", "geo": "es"},
    {"id": "2285", "geo": "de"},
    {"id": "2286", "geo": "lt"},
    {"id": "2289", "geo": "cz"},
    {"id": "2920", "geo": "cz"},
    {"id": "3426", "geo": "lv"},
]

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

def conversion_snippet_html(cpa: float) -> str:
    return f"""<!-- Event snippet for Purchase (1) conversion page -->
<script>
  (function () {{
    var p = new URLSearchParams(window.location.search);

    function stored(name) {{
      try {{ return window.localStorage.getItem('df_' + name) || ''; }}
      catch (e) {{ return ''; }}
    }}

    var campaignId = p.get('campaign_id') || p.get('utm_campaign') || p.get('campaignid') || p.get('subid') || stored('campaign_id') || stored('utm_campaign') || stored('subid') || '';
    var subid = p.get('subid') || campaignId || stored('subid') || '';
    var transactionId = p.get('order_id') || p.get('transaction_id') || p.get('tid') || subid || '';

    gtag('event', 'conversion', {{
      'send_to': '{GOOGLE_ADS_CONVERSION_SEND_TO}',
      'value': {cpa},
      'currency': 'EUR',
      'transaction_id': transactionId,
      'campaign_id': campaignId,
      'subid': subid,
      'utm_campaign': p.get('utm_campaign') || campaignId,
      'utm_source': p.get('utm_source') || stored('utm_source') || '',
      'utm_medium': p.get('utm_medium') || stored('utm_medium') || '',
      'utm_term': p.get('utm_term') || stored('utm_term') || '',
      'utm_content': p.get('utm_content') || stored('utm_content') || ''
    }});
  }})();
</script>"""


def load_ui() -> dict[str, dict]:
    return json.loads(UI_PATH.read_text(encoding="utf-8"))


def merge_landing_content(landing: dict, geo: str) -> dict:
    merged = dict(landing)
    ui = load_ui().get(geo, {})
    for key, value in ui.items():
        merged[key] = value
    return merged


def price_display_parts(price: dict) -> tuple[str, str, str]:
    cur = price.get("currency", "€")
    anchor = price.get("anchor", "")
    final = price.get("final", "")
    old = f"{anchor} {cur}".strip()
    new = f"{final} {cur}".strip()
    return old, final, new


def replace_one(html: str, pattern: str, repl: str, count: int = 1) -> str:
    def _sub(match: re.Match[str]) -> str:
        if match.lastindex and match.lastindex >= 2:
            return f"{match.group(1)}{repl}{match.group(2)}"
        return repl

    return re.sub(pattern, _sub, html, count=count, flags=re.DOTALL)


def apply_landing_content(html: str, landing: dict) -> str:
    price = landing.get("price", {})
    cur = price.get("currency", "€")
    old_price, final_amount, new_price = price_display_parts(price)
    lo = landing.get("limited_offer", {})
    lo_discount = lo.get("discount", "{final} {currency}").format(
        final=price.get("final", ""), currency=cur
    )

    if landing.get("banner_urgency", {}).get("main"):
        html = replace_one(
            html,
            r'(<div class="banner-urgency__main">)[^<]*(</div>)',
            landing['banner_urgency']['main'],
        )

    hl = landing.get("headline", {})
    if hl.get("rating_label"):
        html = replace_one(
            html,
            r'(<div class="hero-headline__rating">\s*<span class="stars"[^>]*>★★★★★</span>\s*<span>)[^<]*(</span>)',
            hl['rating_label'],
        )
    if hl.get("title"):
        html = replace_one(html, r'(<h1 class="hero-headline__title">)[^<]*(</h1>)', hl['title'])
    if hl.get("subtitle"):
        html = replace_one(
            html, r'(<p class="hero-headline__subtitle">)[\s\S]*?(</p>)', hl['subtitle']
        )
    if hl.get("image_alt"):
        html = replace_one(
            html,
            r'(<div class="hero-headline__image">[\s\S]*?<img[^>]*alt=")[^"]*(")',
            hl["image_alt"],
        )
        html = replace_one(
            html,
            r'(<div class="hero-headline__image">[\s\S]*?<img[^>]*title=")[^"]*(")',
            hl["image_alt"],
        )

    if price.get("label"):
        html = replace_one(html, r'(<span class="price-discount__label">)[^<]*(</span>)', price['label'])
    html = replace_one(html, r'(<section class="price-discount">[\s\S]*?<span class="price-anchor__old">)[^<]*(</span>)', old_price)
    html = replace_one(html, r'(<section class="price-discount">[\s\S]*?<span class="price-anchor__new">)[^<]*(</span>)', new_price, count=1)
    if price.get("discount"):
        html = replace_one(
            html,
            r'(<section class="price-discount">[\s\S]*?<span class="price-anchor__discount">)[^<]*(</span>)',
            price['discount'],
        )

    bullets = landing.get("bullets", [])
    bullet_items = re.findall(r"<li>[\s\S]*?</li>", re.search(r'<ul class="bullet-list-checkmark">([\s\S]*?)</ul>', html).group(1))
    for i, item in enumerate(bullet_items):
        if i < len(bullets) and bullets[i].get("text"):
            html = html.replace(item, f"<li>{bullets[i]['text']}</li>", 1)

    form = landing.get("form", {})
    if form.get("title"):
        html = replace_one(
            html,
            r'(<section class="form-1"[\s\S]*?<h2 class="cod-form__title">)[^<]*(</h2>)',
            form['title'],
        )
    if form.get("subtitle"):
        html = replace_one(
            html,
            r'(<section class="form-1"[\s\S]*?<p class="cod-form__subtitle">)[^<]*(</p>)',
            form['subtitle'],
        )
    sp = landing.get("social_proof", {})
    if sp.get("viewing"):
        html = replace_one(
            html,
            r'(<section class="form-1"[\s\S]*?<li class="cod-form__social-proof-item--neutral">[\s\S]*?<span>)[^<]*(?:<[^>]+>[^<]*</[^>]+>)*[^<]*(</span>)',
            sp['viewing'],
        )
    if sp.get("orders"):
        html = replace_one(
            html,
            r'(<section class="form-1"[\s\S]*?<li class="cod-form__social-proof-item--urgent">[\s\S]*?<span>)[^<]*(?:<[^>]+>[^<]*</[^>]+>)*[^<]*(</span>)',
            sp['orders'],
        )
    if landing.get("form_rating"):
        html = replace_one(
            html,
            r'(<span class="cod-form__rating-text">)[^<]*(?:<[^>]+>[^<]*</[^>]+>)*[^<]*(</span>)',
            landing['form_rating'],
        )
    if form.get("secure_note"):
        html = replace_one(
            html, r'(<p class="cod-form__trust"[^>]*>)[^<]*(</p>)', form['secure_note']
        )

    mr = landing.get("macro_review", {})
    if mr.get("quote"):
        html = replace_one(html, r'(<p class="macro-review__quote">)[\s\S]*?(</p>)', mr['quote'])
    if mr.get("author"):
        html = replace_one(html, r'(<div class="macro-review__author">)[^<]*(</div>)', mr['author'])
    if mr.get("credentials"):
        html = replace_one(html, r'(<div class="macro-review__credentials">)[^<]*(</div>)', mr['credentials'])
    if mr.get("photo_alt"):
        html = replace_one(
            html,
            r'(<img class="macro-review__photo"[^>]*alt=")[^"]*(")',
            mr["photo_alt"],
        )
        cred = mr.get("credentials", "")
        html = replace_one(
            html,
            r'(<img class="macro-review__photo"[^>]*title=")[^"]*(")',
            cred,
        )
    if landing.get("section_cta"):
        html = html.replace(
            ">⚡ Ordina ora — Ricevilo entro 48 ore</a>",
            f">{landing['section_cta']}</a>",
        )

    cd = landing.get("competitor_destruction", {})
    if cd.get("title"):
        html = replace_one(
            html, r'(<section class="competitor-destruction">[\s\S]*?<h2 class="section__title">)[^<]*(</h2>)', cd['title']
        )
    if cd.get("subtitle"):
        html = replace_one(
            html,
            r'(<section class="competitor-destruction">[\s\S]*?<p class="section__subtitle">)[^<]*(</p>)',
            cd['subtitle'],
        )
    headers = cd.get("headers", [])
    if len(headers) >= 2:
        html = replace_one(html, r'(<thead>[\s\S]*?<th>)[^<]*(</th>)', headers[0])
        html = replace_one(html, r'(<thead>[\s\S]*?<th class="is-winner">)[^<]*(</th>)', headers[1])
    for i, row in enumerate(cd.get("rows", [])):
        html = re.sub(
            r"(<tbody>[\s\S]*?<tr><td class=\"is-bad\">)[^<]*(</td><td class=\"is-good\">)[^<]*(</td></tr>)",
            lambda m, row=row: f"{m.group(1)}{row['bad']}{m.group(2)}{row['good']}{m.group(3)}",
            html,
            count=1,
            flags=re.DOTALL,
        )

    if lo.get("pill"):
        html = replace_one(html, r'(<span class="limited-offer__pill">)[^<]*(</span>)', lo['pill'])
    html = replace_one(html, r'(<span class="limited-offer__price-old">)[^<]*(</span>)', old_price)
    html = replace_one(html, r'(<span class="limited-offer__price-amount">)[^<]*(</span>)', final_amount)
    html = replace_one(html, r'(<span class="limited-offer__price-currency">)[^<]*(</span>)', cur)
    if lo_discount:
        html = replace_one(html, r'(<p class="limited-offer__discount">)[^<]*(</p>)', lo_discount)
    if lo.get("cta"):
        html = replace_one(
            html, r'(<a href="#form-2" class="cta-button cta-button--orange limited-offer__cta">)[^<]*(</a>)', lo['cta']
        )
    if lo.get("stock_title"):
        html = replace_one(
            html, r'(<p class="limited-offer__stock-title">)[\s\S]*?(</p>)', lo['stock_title']
        )
    if lo.get("stock_note"):
        html = replace_one(html, r'(<p class="limited-offer__stock-note">)[^<]*(</p>)', lo['stock_note'])
    if lo.get("aria_label"):
        html = replace_one(
            html, r'(<aside class="limited-offer__stock" aria-label=")[^"]*(")', lo['aria_label']
        )

    rs = landing.get("reviews_section", {})
    if rs.get("title"):
        html = replace_one(
            html, r'(<section class="reviews-grid">[\s\S]*?<h2 class="section__title">)[^<]*(</h2>)', rs['title']
        )
    if rs.get("subtitle"):
        html = replace_one(
            html,
            r'(<section class="reviews-grid">[\s\S]*?<p class="section__subtitle">)[^<]*(</p>)',
            rs['subtitle'],
        )
    verified = rs.get("verified", "✓")
    for i, review in enumerate(landing.get("reviews", [])):
        cards = list(re.finditer(r'<article class="review-card">[\s\S]*?</article>', html))
        if i >= len(cards):
            break
        card = cards[i].group(0)
        new_card = card
        if review.get("name"):
            new_card = re.sub(r'<div class="review-card__name">[^<]*</div>', f'<div class="review-card__name">{review["name"]}</div>', new_card)
        if review.get("location"):
            new_card = re.sub(
                r'<div class="review-card__location">[^<]*</div>',
                f'<div class="review-card__location">{review["location"]}</div>',
                new_card,
            )
        if review.get("stars"):
            new_card = re.sub(r'<div class="review-card__stars">[^<]*</div>', f'<div class="review-card__stars">{review["stars"]}</div>', new_card)
        if review.get("title"):
            new_card = re.sub(r'<h3 class="review-card__title">[^<]*</h3>', f'<h3 class="review-card__title">{review["title"]}</h3>', new_card)
        if review.get("text"):
            new_card = re.sub(r'<p class="review-card__text">[\s\S]*?</p>', f'<p class="review-card__text">{review["text"]}</p>', new_card)
        if review.get("photo_alt"):
            new_card = re.sub(r'alt="[^"]*"', f'alt="{review["photo_alt"]}"', new_card, count=1)
            new_card = re.sub(r'title="[^"]*"', f'title="{review["photo_alt"]}"', new_card, count=1)
        new_card = re.sub(r'<span class="review-card__verified">[^<]*</span>', f'<span class="review-card__verified">{verified}</span>', new_card)
        html = html.replace(card, new_card, 1)

    pc = landing.get("package_content", {})
    if pc.get("title"):
        html = replace_one(
            html, r'(<section class="package-content">[\s\S]*?<h2 class="section__title">)[^<]*(</h2>)', pc['title']
        )
    if pc.get("image_alt"):
        html = replace_one(
            html,
            r'(<section class="package-content">[\s\S]*?<img[^>]*alt=")[^"]*(")',
            pc["image_alt"],
        )
        html = replace_one(
            html,
            r'(<section class="package-content">[\s\S]*?<img[^>]*title=")[^"]*(")',
            pc.get("title", pc["image_alt"]),
        )
    pkg_items = re.findall(r'<li[^>]*>[\s\S]*?</li>', re.search(r'<ul class="package-content__list[^"]*">([\s\S]*?)</ul>', html).group(1))
    for i, item in enumerate(pkg_items):
        pc_item = pc.get("items", [])
        if i < len(pc_item) and pc_item[i].get("text"):
            cls = ' class="is-bonus"' if 'is-bonus' in item else ""
            html = html.replace(item, f"<li{cls}>{pc_item[i]['text']}</li>", 1)
    html = replace_one(
        html,
        r'(<div class="package-content__price">[\s\S]*?<span class="price-anchor__old">)[^<]*(</span>)',
        old_price,
    )
    html = replace_one(
        html,
        r'(<div class="package-content__price">[\s\S]*?<span class="price-anchor__new">)[^<]*(</span>)',
        new_price,
    )

    f2 = landing.get("form_2", {})
    if f2.get("title"):
        html = replace_one(
            html,
            r'(<section class="form-2"[\s\S]*?<h2 class="cod-form__title">)[^<]*(</h2>)',
            f2['title'],
        )
    if f2.get("subtitle"):
        html = replace_one(
            html,
            r'(<section class="form-2"[\s\S]*?<p class="cod-form__subtitle">)[^<]*(</p>)',
            f2['subtitle'],
        )

    inc = landing.get("incentive_2", {})
    if inc.get("title"):
        html = replace_one(html, r'(<section class="incentive-badges-2">[\s\S]*?<h2>)[^<]*(</h2>)', inc['title'])
    if inc.get("text"):
        html = replace_one(html, r'(<section class="incentive-badges-2">[\s\S]*?<p>)[\s\S]*?(</p>)', inc['text'])

    badges = landing.get("trust_badges", [])
    badge_items = re.findall(
        r'<div class="guarantee-badges__item">[\s\S]*?</div>',
        re.search(r'<section class="guarantee-badges-2">([\s\S]*?)</section>', html).group(1),
    )
    for i, item in enumerate(badge_items):
        if i >= len(badges):
            break
        b = badges[i]
        new_item = re.sub(r'<span class="guarantee-badges__title">[^<]*</span>', f'<span class="guarantee-badges__title">{b["title"]}</span>', item)
        new_item = re.sub(r'<span class="guarantee-badges__sub">[^<]*</span>', f'<span class="guarantee-badges__sub">{b["sub"]}</span>', new_item)
        html = html.replace(item, new_item, 1)

    faq = landing.get("faq", {})
    if faq.get("title"):
        html = replace_one(
            html,
            r'(<section class="faq" id="faq">[\s\S]*?<h2 class="section__title">)[^<]*(</h2>)',
            faq["title"],
        )
    for i, item in enumerate(faq.get("items", [])):
        details = list(re.finditer(r"<details>[\s\S]*?</details>", html))
        if i >= len(details):
            break
        block = details[i].group(0)
        new_block = block
        if item.get("q"):
            new_block = re.sub(r"<summary>[^<]*</summary>", f"<summary>{item['q']}</summary>", new_block)
        if item.get("a"):
            new_block = re.sub(
                r'<div class="faq-accordion__body">[\s\S]*?</div>',
                f'<div class="faq-accordion__body">{item["a"]}</div>',
                new_block,
            )
        html = html.replace(block, new_block, 1)

    footer = landing.get("footer", {})
    company_lines = footer.get("company_info", [])
    if len(company_lines) >= 3:
        html = html.replace("08011 Barcelona, Spagna", company_lines[2].replace("<strong>", "").replace("</strong>", ""))
        html = replace_one(
            html,
            r"(<div>\s*<h4 class=\"site-footer__heading\">[^<]*</h4>\s*<ul class=\"site-footer__list\">\s*<li>)[^<]*(?:<[^>]+>[^<]*</[^>]+>)*[^<]*(</li>)",
            company_lines[0],
        )
        html = replace_one(
            html,
            r"(<div>\s*<h4 class=\"site-footer__heading\">[^<]*</h4>\s*<ul class=\"site-footer__list\">[\s\S]*?<li>[^<]*</li>\s*<li>)[^<]*(</li>)",
            company_lines[1],
        )

    return html


def load_forms() -> dict[str, dict]:
    return json.loads(FORMS_PATH.read_text(encoding="utf-8"))


def render_tm_order_form(offer_id: str, geo: str, suffix: str = "") -> str:
    forms = load_forms()
    cfg = forms[str(offer_id)]
    thank_you = f"https://seogigstore.com/{geo}/fresh-air-pro/thank-you-{offer_id}.html"
    lines = [
        f'<form class="tm-order-form" action="{ADRICE_ACTION}" method="post">',
    ]
    for field in cfg["fields"]:
        fid = field["id"] + suffix if suffix else field["id"]
        req = " required" if field.get("required", True) else ""
        lines.append(f'<label for="{fid}">{field["label"]}</label>')
        lines.append(
            f'<input id="{fid}" type="{field["type"]}" name="{field["name"]}" '
            f'autocomplete="{field["autocomplete"]}" placeholder="{field["placeholder"]}"{req}><br>'
        )
    lines.extend(
        [
            f'<input name="uid" type="hidden" value="{ADRICE_UID}" />',
            f'<input name="offer" type="hidden" value="{offer_id}" />',
            f'<input name="lp" type="hidden" value="{cfg["lp"]}" />',
            f'<input name="thankyoupage" type="hidden" value="{thank_you}"/>',
            f'<input name="webhook" type="hidden" value="{ADRICE_WEBHOOK}"/>',
            f'<input name="_key" type="hidden" value="{cfg["key"]}" />',
            '<div style="margin-top: 10px; text-align: center">',
            f'    <button name="submit" type="submit">{cfg["submit"]}</button>',
            "</div>",
            "</form>",
        ]
    )
    return "\n".join(lines)


def inject_order_forms(html: str, offer_id: str, geo: str) -> str:
    html = html.replace("%%TM_ORDER_FORM_1%%", render_tm_order_form(offer_id, geo))
    html = html.replace("%%TM_ORDER_FORM_2%%", render_tm_order_form(offer_id, geo, suffix="2"))
    return html


def popup_json(locale: dict) -> str:
    items = []
    for i, p in enumerate(locale["popup_purchases"]):
        img = POPUP_IMAGES[i % len(POPUP_IMAGES)]
        items.append(
            f'  {{ "initial": "{p["initial"]}", "name": "{p["name"]}", '
            f'"image": "{img}", "message": "{p["message"]}", "time": "{p["time"]}" }}'
        )
    return "[\n" + ",\n".join(items) + "\n]"


def site_config_block(geo: str, locale: dict, landing: dict, offer_id: str, lp_id: str) -> str:
    price = float(landing["meta"]["price"])
    currency = landing["meta"]["currency"]
    suffix = locale["offer_name_suffix"]
    offer_id = str(offer_id)
    cookie = locale["cookie"]
    return f"""window.SITE_CONFIG = {{
  GEO: '{geo}',
  PRODUCT_SLUG: 'fresh-air-pro',
  CURRENCY: '{currency}',
  PRICE: {price},
  OFFER_ID: '{offer_id}',
  OFFER_NAME: 'Fresh Air Pro {suffix}',
  LP_ID: '{lp_id}',
  META_PIXEL_ID: '',
  GOOGLE_TAG_ID: '{GOOGLE_ADS_ID}',
  GOOGLE_ADS_CONVERSION_ID: '{GOOGLE_ADS_ID}',
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


def generate_landing_html(geo: str, locale: dict, offer_id: str, landing_file: str = "landing.html") -> str:
    landing = merge_landing_content(locale["landing"], geo)
    offer_id = str(offer_id)
    forms = load_forms()
    lp_id = forms[offer_id]["lp"]
    base = f"https://seogigstore.com/{geo}/fresh-air-pro/{landing_file}?offer_id={offer_id}"
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
        site_config_block(geo, locale, landing, offer_id, lp_id),
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
    html = html.replace("Tutti i diritti riservati seogigstore.com", f"{ft['rights']} seogigstore.com")

    if landing.get("footer", {}).get("tagline"):
        html = re.sub(
            r'<p style="margin-top:1rem;max-width:340px">[^<]*</p>',
            f'<p style="margin-top:1rem;max-width:340px">{landing["footer"]["tagline"]}</p>',
            html,
            count=1,
        )

    html = inject_order_forms(html, offer_id, geo)
    html = apply_landing_content(html, landing)
    html = html.replace("AW-17528466836", GOOGLE_ADS_ID)
    return html


def generate_thank_you_html(geo: str, locale: dict, offer_id: str) -> str:
    landing = locale["landing"]
    ty = THANK_YOU.get(geo, THANK_YOU["it"])
    ft = locale["footer"]
    price = float(landing["meta"]["price"])
    currency = landing["meta"]["currency"]
    cpa = OFFER_CPA[str(offer_id)]
    html = TEMPLATE_TY.read_text(encoding="utf-8")

    html = html.replace("AW-17528466836", GOOGLE_ADS_ID)

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
  OFFER_ID: '{offer_id}',
  OFFER_NAME: 'Fresh Air Pro {locale["offer_name_suffix"]}',
  LP_ID: '{geo}-fresh-air-pro-{offer_id}',
  META_PIXEL_ID: '',
  GOOGLE_TAG_ID: '{GOOGLE_ADS_ID}',
  GOOGLE_ADS_CONVERSION_ID: '{GOOGLE_ADS_ID}',
  TY_CONVERSION_LABEL: '1U2ICLnWpMwcEPD-i-ND',
  CONVERSION_VALUE: {cpa},
  CONVERSION_CURRENCY: 'EUR',
  COOKIE_TEXT: '{locale["cookie"]["text"].replace("'", "\\'")}',
  COOKIE_ACCEPT: '{locale["cookie"]["accept"]}',
  COOKIE_LEARN: '{locale["cookie"]["learn"]}'
}};""",
        html,
        count=1,
    )

    html = re.sub(
        r"if \(window\.trackPurchase\) window\.trackPurchase\([^)]+\);",
        f"if (window.trackPurchase) window.trackPurchase({cpa}, 'EUR');",
        html,
        count=1,
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
    html = html.replace("Tutti i diritti riservati seogigstore.com", f"{ft['rights']} seogigstore.com")

    html = re.sub(
        r"<!-- (?:CPA:|Event snippet)[\s\S]*?<script>[\s\S]*?gtag\('event', 'conversion'[\s\S]*?</script>",
        conversion_snippet_html(cpa),
        html,
        count=1,
    )

    return html


def generate_thank_you_json(geo: str, locale: dict, offer_id: str) -> dict:
    landing = locale["landing"]
    ty = THANK_YOU.get(geo, THANK_YOU["it"])
    data = {
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
        "offer_id": offer_id,
    }
    return data


def load_locales() -> dict[str, dict]:
    locales: dict[str, dict] = {}
    for path in LOCALES_DIR.glob("*.json"):
        locales[path.stem] = json.loads(path.read_text(encoding="utf-8"))
    return locales


def main() -> None:
    locales = load_locales()
    forms = load_forms()

    print(f"Generating {len(locales)} geo content JSON files...")
    for geo, locale in sorted(locales.items()):
        landing = locale["landing"]
        content_dir = ROOT / "content" / geo / "products" / "fresh-air-pro"
        content_dir.mkdir(parents=True, exist_ok=True)
        (content_dir / "landing.json").write_text(
            json.dumps(landing, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(f"Generating {len(OFFERS)} offer-specific landings...")
    primary_by_geo: dict[str, str] = {}
    for offer in OFFERS:
        offer_id = str(offer["id"])
        geo = offer["geo"]
        if geo not in primary_by_geo:
            primary_by_geo[geo] = offer_id
        locale = locales[geo]
        page_dir = ROOT / geo / "fresh-air-pro"
        page_dir.mkdir(parents=True, exist_ok=True)
        landing_name = f"landing-{offer_id}.html"
        landing_html = generate_landing_html(geo, locale, offer_id, landing_name)
        (page_dir / landing_name).write_text(landing_html, encoding="utf-8")
        if offer_id == primary_by_geo[geo]:
            primary_html = generate_landing_html(geo, locale, offer_id, "landing.html")
            (page_dir / "landing.html").write_text(primary_html, encoding="utf-8")
        print(f"  ✓ {geo} {landing_name} (offer={offer_id}, lp={forms[offer_id]['lp']})")

    print(f"Generating {len(OFFERS)} offer-specific thank-you pages...")
    for offer in OFFERS:
        offer_id = offer["id"]
        geo = offer["geo"]
        locale = locales[geo]
        content_dir = ROOT / "content" / geo / "products" / "fresh-air-pro"
        page_dir = ROOT / geo / "fresh-air-pro"
        ty_name = f"thank-you-{offer_id}.html"
        ty_json_name = f"thank-you-{offer_id}.json"

        (content_dir / ty_json_name).write_text(
            json.dumps(
                generate_thank_you_json(geo, locale, offer_id),
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (page_dir / ty_name).write_text(
            generate_thank_you_html(geo, locale, offer_id), encoding="utf-8"
        )
        print(f"  ✓ {geo} {ty_name}")

    # Remove legacy generic thank-you pages (replaced by offer-specific files)
    for geo in locales:
        legacy = ROOT / geo / "fresh-air-pro" / "thank-you.html"
        legacy_json = ROOT / "content" / geo / "products" / "fresh-air-pro" / "thank-you.json"
        if legacy.exists():
            legacy.unlink()
        if legacy_json.exists():
            legacy_json.unlink()

    print("Done.")


if __name__ == "__main__":
    main()
