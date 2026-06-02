# ⬡ ChirpStack Gateway Monitor

Een lichtgewicht Flask webapplicatie die gateways ophaalt uit een ChirpStack LoRaWAN netwerk server en weergeeft met een live online/offline status indicator.

Gebouwd voor gebruik met **lora.surfiot.nl** (ChirpStack v4).

---

## Schermafbeelding

```
⬡ Gateway Monitor          ChirpStack · lora.surfiot.nl       ⚙ configuratie

[ Filter op postcode+huisnr  (bijv. 8917DD10)  📌 ]   ↻ Vernieuwen

● 3 online   ● 1 offline   4 gateways getoond · 14:32:01

┌─────────────────────────┐  ┌─────────────────────────┐
│ ● IoTnet-8917DD10       │  │ ● IoTnet-8917DD25       │
│   a84041ffff...         │  │   a84041ffff...         │
│   2m geleden     online │  │   5m geleden     online │
└─────────────────────────┘  └─────────────────────────┘
```

---

## Functionaliteit

- **Live status** — groene pulserende bolletjes (online) en rode bolletjes (offline)
- **Filteren** op postcode + huisnummer uit de gateway naam (bijv. `8917DD10` matcht `IoTnet-8917DD10`)
- **Filter vastzetten** met het 📌 icoon — wordt opgeslagen in de browser (`localStorage`)
- **Auto-refresh** elke 30 seconden
- **Configuratiepagina** (`/config`) voor het instellen van de API token — opgeslagen in `config.json`
- Paginering wordt automatisch afgehandeld (100 gateways per request)

---

## Vereisten

- Python 3.10+
- ChirpStack v4 instantie met gRPC bereikbaar op poort 443
- Een ChirpStack **Network API Key**

---

## Installatie

```bash
# 1. Clone de repository
git clone https://github.com/JOUWUSERNAME/chirpstack-gateways.git
cd chirpstack-gateways

# 2. Maak een virtual environment aan
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Installeer dependencies
pip install flask grpcio chirpstack-api
```

---

## Gebruik

```bash
# Start de applicatie
python app.py
```

Open dan `http://localhost:5000` in je browser.

Bij de eerste keer opstarten word je automatisch doorgestuurd naar de configuratiepagina (`/config`). Vul hier je ChirpStack API token in.

---

## Configuratie

| Instelling | Locatie | Omschrijving |
|---|---|---|
| API Token | `/config` pagina → `config.json` | ChirpStack Network API Key |
| Server | `chirpstack_client.py` | Standaard: `lora.surfiot.nl:443` |
| Tenant ID | `chirpstack_client.py` | UUID van je ChirpStack tenant |

> ⚠️ `config.json` staat in `.gitignore` en bevat je API token — commit dit bestand nooit.

### API Token aanmaken in ChirpStack

1. Log in op je ChirpStack instantie
2. Ga naar **API Keys** → **Add API key**
3. Geef het een naam en sla de token op
4. Plak de token in de configuratiepagina van de monitor

---

## Projectstructuur

```
chirpstack-gateways/
├── app.py                  # Flask routes
├── chirpstack_client.py    # gRPC client + config lezen/schrijven
├── config.json             # API token opslag (niet in git)
├── templates/
│   ├── index.html          # Gateway overzicht
│   └── config.html         # Configuratiepagina
├── .gitignore
└── README.md
```

---

## Filter logica

De filtertekst wordt vergeleken met het gedeelte **na het laatste koppelteken** in de gateway naam:

```
IoTnet-8917DD10  →  suffix: 8917DD10
```

Invullen van `8917DD10`, `8917DD` of `DD10` geeft allemaal een match. De filter is hoofdletterongevoelig.

---

## Licentie

MIT
