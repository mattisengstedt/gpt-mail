# 📬 EmailGPT

**EmailGPT** är ett Python-baserat verktyg som:
- Hämtar olästa e-postmeddelanden från Gmail
- Kategoriserar dem med hjälp av OpenAI GPT
- Skickar en sammanfattning och eventuella svarsförslag till Slack


---

## ⚙️ Funktioner

- 🔍 Kategorisering av e-post i t.ex. `Jobbrelaterat`, `Prioriterat`, `Nyhetsbrev` m.fl.
- 🧠 GPT-genererade sammanfattningar av viktiga mejl
- ✉️ Identifiering av mejl som kräver svar + svarsförslag
- 🔔 Slack-notifiering i din DM eller annan valfri kanal

---

## 🚀 Kom igång

### 1. Klona repo

```bash
git clone https://github.com/ditt-namn/email-gpt.git
cd email-gpt
```

### 2. Skapa virtuell miljö (valfritt men rekommenderat)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installera beroenden

```bash
pip install -r requirements.txt
```

### 4. Lägg till `user_settings.py`

Ändra filen i projektroten som heter `user_settings.py` med följande innehåll:

```python
# user_settings.py
ACCOUNT = "din e-postadress (gmail)"
APP_PASSWORD = "ditt app-lösenord för Gmail"
OPENAI_API_KEY = "din OpenAI-nyckel"
SLACK_BOT_TOKEN = "din Slack bot token"
```

**OBS!** Dela aldrig den här filen offentligt.

---

## ▶️ Kör scriptet

```bash
source venv/bin/activate
python main.py
```