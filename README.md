# TikTok Downloader Bot

Telegram-бот для скачивания контента с различных платформ: TikTok, Instagram, YouTube, Twitter.

## Функциональность

- Скачивание видео и фото с TikTok
- Скачивание медиа с Instagram (фото и видео)
- Скачивание видео и аудио с YouTube (без API)
- Скачивание медиа с Twitter (фото, видео и GIF)

## Установка

1. Установите Python 3.8 или выше
2. Клонируйте репозиторий
3. Установите зависимости:

```bash
pip install -r requirements.txt
```

## Настройка

1. Создайте бота в [@BotFather](https://t.me/BotFather) и получите токен
2. Заполните файл `.env` своими данными:

```env
# Telegram Bot Token
BOT_TOKEN=ваш_токен_бота

# API Configuration for Instagram
API_ID=ваш_api_id
API_HASH=ваш_api_hash

# Instagram Username
INSTAGRAM_USERNAME=ваш_инстаграм_юзернейм

# Owner ID
OWNER_ID=ваш_айди

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

### Где получить переменные:

- `BOT_TOKEN` — получить у [@BotFather](https://t.me/BotFather) в Telegram (бесплатно)
- `API_ID`, `API_HASH` — получить на [my.telegram.org](https://my.telegram.org) (бесплатно, требуется аккаунт Telegram)
- `INSTAGRAM_USERNAME` — ваш логин в Instagram (бесплатно)
- `OWNER_ID` — ваш ID в Telegram (можно получить у [@userinfobot](https://t.me/userinfobot)) (бесплатно)

**Опциональные переменные:**

- `INSTA_SESSIONFILE_ID` — ID файла сессии Instagram (бесплатно, создается автоматически при первом использовании)
- `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET` — получить на [Twitter Developer Portal](https://developer.twitter.com/) (требуется аккаунт разработчика)

**Важно:** Для работы с Twitter необходимо получить API-ключи на Twitter Developer Portal и заполнить соответствующие переменные. Без этих ключей функция скачивания Twitter-контента работать не будет.

**Примечание:** Большинство из этих сервисов бесплатны, но могут иметь ограничения по количеству запросов в день.

### Назначение Instagram переменных:

- `INSTAGRAM_USERNAME` — используется для аутентификации в Instagram через библиотеку Instaloader
- `INSTA_SESSIONFILE_ID` — ID файла сессии Instagram, который позволяет сохранять сессию и не проходить аутентификацию каждый раз
- `INSTAGRAM_BOT_TOKEN` — токен для дополнительного Instagram бота (не используется в текущей реализации, но предусмотрен в коде)

**Важно:** Функция скачивания Instagram-контента теперь полностью реализована. Для полноценной работы с Instagram рекомендуется заполнить переменные `INSTAGRAM_USERNAME` и при необходимости использовать сессию Instagram.

При запуске бота с вашей сессией Instagram, другие пользователи смогут скачивать контент с Instagram через вашего бота. Важно понимать, что все запросы к Instagram будут выполняться от вашего имени, и приватные аккаунты будут доступны только если вы подписаны на них.

## Запуск

### В командной строке Windows:
```cmd
start.bat
```

### В PowerShell:
```powershell
.\start.ps1
```

### Вручную через Python (если предыдущие способы не работают):
1. Убедитесь, что у вас установлены все зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите бота:
```bash
python bot.py
```

**Важно:** Перед запуском убедитесь, что вы заполнили все необходимые переменные в файле `.env`, особенно `BOT_TOKEN`, который обязателен для работы бота.

## Использование

После запуска бота вы можете использовать следующие команды:

- `/start` - начать работу с ботом
- `/help` - получить справку
- `/tiktok` - скачать с TikTok
- `/instagram` - скачать с Instagram
- `/youtube` - скачать с YouTube
- `/twitter` - скачать с Twitter

Просто отправьте боту ссылку на видео/пост, и он автоматически определит платформу и скачает контент.

**Особенности бота:**
- Автоматическая проверка размера файлов перед отправкой в Telegram (ограничение 20 МБ)
- Улучшенная обработка перенаправлений TikTok-ссылок
- Поддержка различных форматов TikTok-ссылок

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности смотрите в файле [LICENSE](./LICENSE).

**Состояние бота:** В данный момент бот успешно запущен и работает. Он может скачивать контент с TikTok, Instagram, YouTube и Twitter (при наличии соответствующих API-ключей).

Также доступна альтернативная лицензия GNU General Public License v3.0 (GPL-3.0). Подробности смотрите в файле [GPL-LICENSE](./GPL-LICENSE).