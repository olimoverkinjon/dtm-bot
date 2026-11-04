# DTM Bot

Telegram bot that collects applicant registrations for the **Registan Abituriyent** channel.

> 🇺🇿 Registan Abituriyent kanali uchun abituriyentlarni ro'yxatga oluvchi Telegram bot.

## What it does

- Checks that the user is subscribed to the channel before registration
- Step-by-step form: full name → phone (contact share) → extra phone
- Sends every new lead to a private group chat and stores it in `leads.json`
- `/admin` panel for admins: statistics and the list of leads
- Forwards photos, videos and documents from users to the admin group

## Tech stack

- **Python version:** Python 3.12, [aiogram 3](https://docs.aiogram.dev/), aiohttp (`bot.py`, `main.py`)
- **PHP version:** webhook-based, runs on Apache (`index.php`, `webhook.php`, `config.php`, `Dockerfile`)

## Quick start (Python)

```bash
git clone https://github.com/olimoverkinjon/dtm-bot.git
cd dtm-bot
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # then fill in your values
python main.py
```

## Configuration

All secrets are read from environment variables (or a local `.env` file, which is git-ignored). Never commit a real token.

| Variable | Description |
|---|---|
| `API_TOKEN` | Bot token from [@BotFather](https://t.me/BotFather) |
| `CHANNEL_USERNAME` | Channel users must join, e.g. `@registan_abituriyent` |
| `GROUP_ID` | Chat ID of the group that receives leads |
| `ADMIN_ID`, `ADMIN_ID_2` | Telegram user IDs allowed to use `/admin` |
| `BOT_MODE` | `polling` (default) or `webhook` |
| `WEBHOOK_URL` | Required only in webhook mode |

## Project structure

```
bot.py              # main bot logic (Python)
main.py             # entry point
config.py           # configuration loader
setup_webhook.py    # registers the webhook URL
status.py           # status dashboard
index.php, webhook.php, config.php, status.php   # PHP version
Dockerfile, docker-compose.yml                   # PHP container
docs/               # deployment guides and migration notes
```

## Docs

- [Getting started](docs/GETTING_STARTED.md)
- [Deployment guide](docs/DEPLOYMENT_GUIDE.md)
- [Python version details](docs/README_PYTHON.md) · [PHP version details](docs/README_PHP.md)

## License

MIT
