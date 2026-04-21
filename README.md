# DTM Bot

Telegram bot for registering users in the Registan Abituriyent channel.

## Features

- Channel subscription verification
- User registration form (name, phone numbers)
- Lead collection to group chat

## Requirements

- Python 3.12+
- aiogram 3.27.0+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dtm-bot.git
cd dtm-bot
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your actual values
```

5. Run the bot:
```bash
python dtm.py
```

## Configuration

Create a `.env` file with the following variables:
- `API_TOKEN`: Your Telegram bot token
- `CHANNEL_USERNAME`: Channel username (e.g., @registan_abituriyent)
- `GROUP_ID`: Group ID where leads are sent

## License

MIT
