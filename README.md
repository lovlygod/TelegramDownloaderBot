<div align="center">
  <h1 style="margin-top: 24px;">💎 Telegram Downloader Bot by @lovlydev</h1>

  <p style="font-size: 18px; margin-bottom: 24px;">
    <b>Telegram bot for downloading content from various platforms: TikTok, Instagram, YouTube, Twitter</b>
  </p>

[Report Bug](https://github.com/lovlygod/TelegramDownloaderBot/issues) · [Request Feature](https://github.com/lovlygod/TelegramDownloaderBot/issues)

</div>

---

## ✨ Features

- 🎥 **TikTok Content Download** - Download videos and photos from TikTok
- 📸 **Instagram Media Download** - Download photos and videos from Instagram 
- 🎵 **YouTube Video/Audio Download** - Download videos and audio from YouTube (without API)
- 🐦 **Twitter Media Download** - Download photos, videos and GIFs from Twitter

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/lovlygod/TelegramDownloaderBot.git
cd TelegramDownloaderBot
pip install -r requirements.txt
```

### 2. Configuration

Create `.env` file with your credentials:

```env
# Telegram Bot Token
BOT_TOKEN=your_bot_token

# API Configuration for Instagram
API_ID=your_api_id
API_HASH=your_api_hash

# Instagram Username
INSTAGRAM_USERNAME=your_instagram_username

# Owner ID
OWNER_ID=your_id

# Session File ID for Instagram
INSTA_SESSIONFILE_ID=

# API tokens for various platforms
TIKTOK_API_TOKEN=
INSTAGRAM_BOT_TOKEN=
YOUTUBE_API_TOKEN=
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
```

### 3. Getting Required Data

#### 🤖 Telegram Bot Token
1. Message [@BotFather](https://t.me/BotFather) in Telegram
2. Create a new bot using `/newbot` command
3. Copy the token and paste to `BOT_TOKEN` in your `.env` file

#### 🔐 Telegram API Credentials
1. Visit [my.telegram.org](https://my.telegram.org)
2. Login with your Telegram account
3. Create a new application
4. Copy `API_ID` and `API_HASH` → paste to your `.env` file

#### 👤 Instagram Username
1. Your Instagram login username
2. Paste to `INSTAGRAM_USERNAME` in your `.env` file

#### 🆔 Telegram User ID
1. Message [@userinfobot](https://t.me/userinfobot) in Telegram
2. Copy your ID → paste to `OWNER_ID` in your `.env` file

**Optional credentials:**
- Twitter API keys: Get from [Twitter Developer Portal](https://developer.twitter.com/)

### 4. Usage

Run the bot using one of these methods:

#### Windows Command Line:
```cmd
start.bat
```

#### PowerShell:
```powershell
.\start.ps1
```

#### Manual Python execution:
```bash
python bot.py
```

## Commands

After starting the bot, you can use these commands:

| Command | Description |
|---------|-------------|
| `/start` | Start working with the bot |
| `/help` | Get help information |
| `/tiktok` | Download from TikTok |
| `/instagram` | Download from Instagram |
| `/youtube` | Download from YouTube |
| `/twitter` | Download from Twitter |

Just send the bot a link to a video/post, and it will automatically detect the platform and download the content.

## Requirements

- Python >= 3.8
- Libraries: python-telegram-bot, instaloader, pytube, etc. (see requirements.txt)

## License
[MIT](LICENSE)

<div align="center">

### Made with ❤️ by [@lovly](https://t.me/lovlyswag)

**Star ⭐ this repo if you found it useful!**

</div>
