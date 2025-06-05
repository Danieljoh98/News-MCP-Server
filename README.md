# 📰 News MCP Server

En MCP (Model Context Protocol) server som integrerer nyhetsdata med AI-analyse for å gi omfattende nyhetsanalyse og innsikt.

## 🌟 Funksjoner

Denne MCP-serveren tilbyr tre hovedverktøy:

- **📰 get_news**: Henter og analyserer nyhetsartikler med AI-genererte sammendrag
- **⚖️ generate_pros_cons**: Lager fordeler/ulemper-analyse basert på nyhetsartikler
- **📅 build_timeline**: Bygger tidslinjer over hendelser fra nyhetskilder

## 🛠️ Installasjon

### Forutsetninger

- Python 3.13 eller nyere
- UV package manager (anbefalt) eller pip
- **API-nøkler** (se konfigurasjon nedenfor)

### 1. Klone prosjektet

```bash
git clone https://github.com/ditt-brukernavn/news.git
cd news
```

### 2. Installer avhengigheter

Med UV:
```bash
uv sync
```

Med pip:
```bash
pip install httpx "mcp[cli]" python-dotenv
```

### 3. Konfigurer API-nøkler (PÅKREVD)

⚠️ **VIKTIG**: Dette prosjektet krever API-nøkler som du må skaffe selv.

#### 3.1 Skaff API-nøkler

Du trenger følgende API-nøkler:

**NewsAPI (Gratis):**
1. Gå til [newsapi.org](https://newsapi.org)
2. Klikk "Get API Key"
3. Registrer deg med e-post
4. Kopier din API-nøkkel

**Claude API (Betalt):**
1. Gå til [console.anthropic.com](https://console.anthropic.com)
2. Opprett en konto
3. Gå til "API Keys" i dashboardet
4. Klikk "Create Key"
5. Kopier din API-nøkkel

#### 3.2 Opprett .env-fil

Opprett en `.env`-fil i rotmappen av prosjektet:

```bash
touch .env  # Linux/Mac
# eller opprett filen manuelt i Windows
```

Legg til dine API-nøkler i `.env`-filen:

```env
NEWS_API_KEY=din_faktiske_newsapi_nøkkel_her
CLAUDE_API_KEY=din_faktiske_claude_api_nøkkel_her
```

**Eksempel:**
```env
NEWS_API_KEY=a1b2c3d4e5f6789012345abcdef67890
CLAUDE_API_KEY=sk-ant-api03-AbCdEf1234567890...
```

🔒 **Sikkerhetsnote**: `.env`-filen er allerede lagt til i `.gitignore` og vil ikke bli lastet opp til GitHub.


## 🚀 Bruk

### Test at alt fungerer

Før du starter serveren, test at API-nøklene fungerer:

```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('NewsAPI Key:', 'OK' if os.getenv('NEWS_API_KEY') else 'MANGLER')
print('Claude Key:', 'OK' if os.getenv('CLAUDE_API_KEY') else 'MANGLER')
"
```

### Som MCP Server (anbefalt)

1. Start serveren:
```bash
python news.py
```

2. Koble til Claude Desktop ved å legge til følgende i din `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "news": {
      "command": "python",
      "args": ["C:/full/sti/til/news/news.py"],
      "env": {
        "NEWS_API_KEY": "din_faktiske_newsapi_nøkkel",
        "CLAUDE_API_KEY": "din_faktiske_claude_nøkkel"
      }
    }
  }
}
```

**Alternativt (anbefalt):** Bruk .env-filen ved å peke til prosjektmappen:
```json
{
  "mcpServers": {
    "news": {
      "command": "python",
      "args": ["news.py"],
      "cwd": "C:/full/sti/til/news/"
    }
  }
}
```

### Tilgjengelige verktøy i Claude

#### 📰 get_news(topic)
Henter nyhetsartikler om et spesifikt tema og genererer AI-sammendrag.

**Eksempel:**
```
Bruk get_news-verktøyet for å finne artikler om "klimaendringer"
```

#### ⚖️ generate_pros_cons(topic)
Analyserer nyhetsartikler og lager en strukturert fordeler/ulemper-liste.

**Eksempel:**
```
Bruk generate_pros_cons-verktøyet for "elbiler" for å se argumenter på begge sider
```


#### 📅 build_timeline(topic)
Bygger en kronologisk tidslinje basert på nyhetshendeser.

**Eksempel:**
```
Bruk build_timeline-verktøyet for "ukraina-krig" for å se hendelsesforløp
```

## 📁 Prosjektstruktur

```
news/
├── .env                 # API-nøkler (MÅ OPPRETTES AV DEG)
├── .gitignore          # Git-ignorerte filer
├── .python-version     # Python versjonsspesifikasjon
├── pyproject.toml      # Prosjektkonfigurasjon og avhengigheter
├── uv.lock            # UV låsefil for reproduserbare builds
├── news.py            # Hovedserverfil
├── news copy.py       # Backup/alternativ implementasjon
├── news_news_detailed_comments.py  # Detaljert kommentert versjon
└── README.md          # Denne filen
```

## 🔧 Teknisk oversikt

### Avhengigheter

- **httpx**: Asynkron HTTP-klient for API-forespørsler
- **mcp[cli]**: Model Context Protocol implementasjon
- **python-dotenv**: For miljøvariabel-håndtering

### API-integrasjoner

- **NewsAPI v2**: Henter nyhetsartikler fra tusenvis av kilder
- **Claude 3 Haiku**: AI-analyse og sammendrag av innhold

### Sikkerhet

- API-nøkler lagres i `.env`-fil (ikke versjonskontrollert)
- HTTPS-forespørsler til alle eksterne API-er
- Timeout-håndtering for alle nettverksforespørsler

## 💰 Kostnader

- **NewsAPI**: Gratis tier gir 1000 forespørsler per måned
- **Claude API**: Betales per token - Haiku er rimeligste modell (~$0.25/1M tokens)

Estimert kostnad for moderat bruk: $5-15 per måned avhengig av aktivitet.


## 🐛 Feilsøking

### Vanlige problemer

1. **"Fant ingen artikler"**
   - ✅ Sjekk at `NEWS_API_KEY` er korrekt satt i `.env`
   - ✅ Verifiser at API-nøkkelen er gyldig på [newsapi.org](https://newsapi.org)

2. **"Klarte ikke analysere med Claude"**
   - ✅ Sjekk at `CLAUDE_API_KEY` er korrekt satt i `.env`
   - ✅ Verifiser at du har kreditt på Anthropic-kontoen din
   - ✅ Test nettverkstilgang til api.anthropic.com

3. **"Server starter ikke"**
   - ✅ Kontroller at alle avhengigheter er installert: `uv sync`
   - ✅ Sjekk at Python 3.13+ er installert: `python --version`
   - ✅ Verifiser at `.env`-filen eksisterer og inneholder begge nøklene

4. **"ModuleNotFoundError"**
   - ✅ Aktiver virtual environment: `.venv\Scripts\activate` (Windows) eller `source .venv/bin/activate` (Linux/Mac)
   - ✅ Installer avhengigheter på nytt

### Testing av API-nøkler

Test NewsAPI:
```bash
curl -H "Authorization: Bearer DIN_NEWSAPI_NØKKEL" \
  "https://newsapi.org/v2/everything?q=test&pageSize=1"
```

Test Claude API:
```bash
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: DIN_CLAUDE_NØKKEL" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-3-haiku-20240307","max_tokens":10,"messages":[{"role":"user","content":"test"}]}'
```

### Logging

For detaljert debugging:
```bash
python news.py --verbose
```

## 📝 Lisens

Dette prosjektet er utviklet for personlig/utdanningsbruk. Se respektive API-leverandørers vilkår for kommersielle restriksjoner.

## 🤝 Bidrag

Forbedringsforslag og pull requests er velkommen! Vennligst:

1. Fork prosjektet
2. Opprett en feature branch
3. Commit dine endringer  
4. Push til branchen
5. Opprett en Pull Request

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/ditt-brukernavn/news/issues)
- 📖 **NewsAPI Docs**: [newsapi.org/docs](https://newsapi.org/docs)
- 🤖 **Claude API Docs**: [docs.anthropic.com](https://docs.anthropic.com)

---

**⚠️ Husk**: Du må skaffe dine egne API-nøkler for at dette prosjektet skal fungere!
