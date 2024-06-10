# Manganime Discord Bot

A comprehensive Discord bot designed to track manga releases, manage user subscriptions, and notify communities of new chapters automatically.

> **Archival Note:** This project was originally developed in **2022**. It is archived here to demonstrate backend development skills, asynchronous programming, and database management.

## Key Features

* **Asynchronous Architecture:** Built with `discord.py` and `aiohttp` to handle concurrent API requests without blocking the event loop.
* **RSS Feed Parsing:** Automates chapter tracking by parsing RSS feeds from major aggregators (MangaUpdates, FanFox) using `feedparser`.
* **SQLite Database:** Implements a relational database (`aiosqlite`) to store guild configurations, user follow lists, and update logs.
* **External API Integration:** Interfaces with the **MangaDex API** to fetch metadata, cover art, and chapter links dynamically.
* **Slash Commands:** utilized `discord-py-slash-command` (pre-2.0 standard) for modern user interactions.

## Tech Stack

* **Language:** Python 3.8+
* **Core Libs:** `discord.py` (v1.7.3), `aiohttp`, `feedparser`, `aiosqlite`
* **Data Storage:** SQLite3
* **Environment:** Docker / Conda

## Project Structure

```plaintext
Manganime-discord-bot/
├── main.py              # Entry point (Bot initialization & Slash commands)
├── mdexapi.py           # Async wrapper for MangaDex API
├── db/                  # Database logic (Schema & CRUD operations)
├── rss/                 # RSS Feed parsers (FanFox, MangaUpdates)
└── requirements.txt     # Dependencies
```

## Setup & Usage

1. **Clone the repository**

```bash
git clone [https://github.com/YOUR_USERNAME/Manganime-discord-bot.git]
cd Manganime-discord-bot
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Configuration Create a .env file in the root directory:**
```bash
TOKEN=your_discord_bot_token_here
```

4. **Run the Bot**

```bash
python main.py
```

## License
This project is open-source and available under the MIT License.