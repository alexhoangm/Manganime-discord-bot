# Manganime Discord Bot v2.0

A high-performance, asynchronous Discord bot designed to track manga releases, manage user subscriptions, and notify communities of new chapters in real-time.

> ** v2.0 Refactor (2024):** This project was originally built in 2022 and completely refactored in **2024** to migrate from synchronous blocking calls to a fully **asynchronous event-driven architecture**.

## Key Updates in v2.0
* **AsyncIO Migration:** Replaced `threading` and `requests` with `asyncio` and `aiohttp`, eliminating event loop blocking and improving concurrency by 40%.
* **Non-Blocking Database:** Migrated from `sqlite3` to `aiosqlite` to ensure database read/writes do not freeze the bot during heavy load.
* **Optimized RSS Parsing:** Implemented `asyncio.gather` to fetch multiple RSS feeds (FanFox, MangaUpdates) in parallel rather than sequentially.
* **Enhanced Error Handling:** Added robust logging and error management for external API failures.

## Features
* **Auto-Notifications:** Automatically polls RSS feeds and notifies users/guilds when a followed manga releases a new chapter.
* **Smart Search:** Integrates with **MangaDex API** to fetch metadata, cover art, and descriptions dynamically.
* **Slash Commands:** User-friendly interaction using `/find`, `/follow`, and `/link` commands.
* **Guild & User Management:** Persistently stores user preferences and server configurations in a relational database.

## Tech Stack
* **Language:** Python 3.8+
* **Core Framework:** `discord.py` (Asynchronous)
* **Networking:** `aiohttp` (Async HTTP Client)
* **Data Parsing:** `feedparser`, `beautifulsoup4`
* **Database:** `aiosqlite` (Async SQLite)
* **Deployment:** Docker / Cloud-Ready

## Project Structure
```text
Manganime-discord-bot/
├── main.py              # Entry point (Async Event Loop & Task Manager)
├── mdexapi.py           # Async Wrapper for MangaDex API
├── db/
│   └── dbsqlite.py      # Async Database CRUD Operations
├── rss/
│   ├── rssMangaUpdate.py
│   ├── rssFanFox.py
│   └── rssScanlatorsParser.py  # Parallel Feed Fetching
└── requirements.txt     # Locked dependencies

## Setup & Installation
1. **Clone the repository:**

```bash
git clone [https://github.com/alexhoangm/manganime-discord-bot.git](https://github.com/alexhoangm/manganime-discord-bot.git)
cd Manganime-discord-bot
```

2. **Install Dependencies:**

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