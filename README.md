# Meow-discord-bot

A high energy Discord economy and fun bot featuring gambling games, Roblox discovery, and Chiikawa-themed GIFs.


## ✨ Features

* **💰 Economy**: Earn 'Meowency' and compete on server-wide leaderboards.
* **🃏 Casino Games**: Play Blackjack, Slots, and Dice Roll with real-time balance updates.
* **🎮 Roblox Discovery**: Browse top-trending games by genre (Horror, FPS, Adventure, etc.) with direct play links.
* **🌈 Character GIFs**: Instant access to Chiikawa, Deltarune, and cute animal GIFs.
* **📩 DM Logging**: Advanced logging system for staff to track and reply to bot DMs.

## 🚀 Setup Instructions

1.  **Install Dependencies**:
    ```bash
    pip install discord.py requests python-dotenv certifi
    ```

2.  **Configuration**:
    * Create a `.env` file in the root directory.
    * Add your credentials:
        ```env
        DISCORD_TOKEN=your_bot_token_here
        GIPHY_API_KEY=your_giphy_key_here
        ```

3.  **Run the Bot**:
    ```bash
    python bot.py
    ```

## 🛠 Commands

| Command | Description |
| :--- | :--- |
| `?coms` | View the full list of all available commands |
| `?bal` | Check your current Meowency balance |
| `?daily` | Claim your daily allowance |
| `?bj [bet]` | Play a round of Blackjack against the dealer |
| `?slots [bet]` | Spin the cat-themed slot machine |
| `?top` | View the server's top Meowency holders |
| `?rblx genres` | List all available Roblox game categories |

## 🔒 Security

This bot uses a `.env` system to keep your Discord Token and API keys private. Never share your `.env` file or upload it to GitHub.

---
