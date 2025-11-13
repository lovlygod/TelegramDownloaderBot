import logging
import time
import os
import asyncio
from typing import Final
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from pytube import YouTube
import tweepy
from instaloader import Instaloader, Profile
from pyrogram import Client as PyrogramClient
from pyromod import listen
from config import Config
from utils import download_insta, upload, acc_type, yes_or_no
import subprocess
from tt_video import yt_dlp as tt_yt_dlp
import re

# Настройка логирования
logging.basicConfig(level=logging.INFO)

import os
from dotenv import load_dotenv
load_dotenv()

# Объединенный токен для бота (замените на ваш токен)
TOKEN : Final = os.environ.get("BOT_TOKEN", "your_api_token_here")

# API токены и настройки для различных платформ
TIKTOK_API_TOKEN = os.environ.get("TIKTOK_API_TOKEN", "")
INSTAGRAM_BOT_TOKEN = os.environ.get("INSTAGRAM_BOT_TOKEN", "")
YOUTUBE_API_TOKEN = os.environ.get("YOUTUBE_API_TOKEN", "")
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET", "")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", "")

# Языковые настройки
languages = {
    "ru": {
        "help": "Скачать видео или картинки с тиктока легко😉\nОтправь мне ссылку на видео или картинки.\nЕсли вы заметили ошибки отпишите @phones_parts",
        "invalid_link": "Неверная ссылка, пришлите правильную ссылку. Пример:\nhttps://vm.tiktok.com/abcdefg/",
        "wait": "Пожалуйста, подождите!\nВаше видео загружается...\nПока загружается видео вы можете подписатся наш канал @XLRSHOP",
        "likes": "Лайков",
        "comments": "Коментариев",
        "share": "Репостов",
        "views": "Просмотров",
        "nickname": "Ник",
        "large_for_tg": "Вес видео слишком большой для телеграмма(20 МБ лимит), но вы можете скачать видео по ссылке",
    },
    "en": {
        "help": "Download video or images from tiktok easy\nSend me a link of video.\nIf you see bugs message me @phones_parts",
        "invalid_link": "Invalid link, please send the correct link. Example:\nhttps://vm.tiktok.com/XLR_TT_BOT/",
        "wait": "Please wait!\nYour video is on the way...",
        "likes": "likes",
        "comments": "comments",
        "share": "share",
        "views": "views",
        "nickname": "nickname",
        "large_for_tg": "video is too large for telegram(20 MB limit), but you can download video by link",
    }
}

# Инициализация ботов для разных платформ
class DownloaderBot:
    def __init__(self):
        self.telegram_app = Application.builder().token(TOKEN).build()
        self.tiktok_bot = None
        self.instagram_bot = None
        self.youtube_bot = None
        self.twitter_bot = None
        self.setup_handlers()
    
    def setup_handlers(self):
        # Команды для Telegram
        self.telegram_app.add_handler(CommandHandler('start', self.start_command))
        self.telegram_app.add_handler(CommandHandler('help', self.help_command))
        self.telegram_app.add_handler(CommandHandler('tiktok', self.tiktok_command))
        self.telegram_app.add_handler(CommandHandler('instagram', self.instagram_command))
        self.telegram_app.add_handler(CommandHandler('youtube', self.youtube_command))
        self.telegram_app.add_handler(CommandHandler('twitter', self.twitter_command))
        
        # Обработчик сообщений
        self.telegram_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Привет! Я универсальный бот для скачивания контента.\n"
            "Используйте следующие команды:\n"
            "/tiktok - скачать с TikTok\n"
            "/instagram - скачать с Instagram\n"
            "/youtube - скачать с YouTube\n"
            "/twitter - скачать с Twitter\n"
            "/help - помощь"
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Я могу скачивать контент с различных платформ:\n"
            "- TikTok: Отправьте ссылку на видео TikTok\n"
            "- Instagram: Отправьте ссылку на пост Instagram\n"
            "- YouTube: Отправьте ссылку на видео YouTube\n"
            "- Twitter: Отправьте ссылку на твит\n"
            "Или используйте соответствующие команды для каждой платформы."
        )
    
    async def tiktok_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Отправьте ссылку на TikTok видео для скачивания")
    
    async def instagram_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Отправьте ссылку на Instagram пост для скачивания")
    
    async def youtube_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Отправьте ссылку на YouTube видео для скачивания")
    
    async def twitter_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Отправьте ссылку на твит для скачивания")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message.text
        chat_id = update.message.chat.id
        
        # Определение типа ссылки и вызов соответствующего обработчика
        if 'tiktok.com' in message:
            await self.handle_tiktok_link(message, chat_id)
        elif 'instagram.com' in message:
            await self.handle_instagram_link(message, chat_id)
        elif 'youtube.com' in message or 'youtu.be' in message:
            await self.handle_youtube_link(message, chat_id)
        elif 'twitter.com' in message or 'x.com' in message:
            await self.handle_twitter_link(message, chat_id)
        else:
            await update.message.reply_text("Пожалуйста, отправьте ссылку на TikTok, Instagram, YouTube или Twitter")
    
    async def handle_tiktok_link(self, link, chat_id):
        await self.telegram_app.bot.send_message(chat_id=chat_id, text="Скачивание TikTok контента...")
        # Используем код из tt_video.py для обработки TikTok ссылок
        try:
            # Сначала пробуем использовать основную функцию
            response = await tt_yt_dlp(link)
            if response.endswith(".mp3"):
                await self.telegram_app.bot.send_audio(chat_id=chat_id, audio=open(response, 'rb'), caption='@DownloaderBot')
            else:
                await self.telegram_app.bot.send_video(chat_id=chat_id, video=open(response, 'rb'), caption='@DownloaderBot')
            os.remove(response)
        except Exception as e:
            # Если основная функция не сработала, пробуем использовать tt_videos_or_images
            try:
                from tt_video import tt_videos_or_images
                result = await tt_videos_or_images(link)
                if result and not isinstance(result, BaseException):
                    if result.get("is_video"):
                        # Это видео - пробуем скачать через yt-dlp
                        from yt_dlp import YoutubeDL
                        ydl_opts = {
                            'outtmpl': '%(title)s.%(ext)s',
                            'max_filesize': 50 * 1024 * 1024,  # 50MB лимит для Telegram
                        }
                        with YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(link, download=True)
                            filename = ydl.prepare_filename(info)
                            # Проверяем размер файла перед отправкой
                            file_size = os.path.getsize(filename)
                            if file_size > 20 * 1024 * 1024:  # 20MB - лимит Telegram
                                await self.telegram_app.bot.send_message(
                                    chat_id=chat_id,
                                    text=f"Видео слишком большое для отправки в Telegram ({file_size / (1024*1024):.1f}MB).\nСсылка на скачивание: {link}"
                                )
                                os.remove(filename)
                            else:
                                await self.telegram_app.bot.send_video(chat_id=chat_id, video=open(filename, 'rb'), caption='@DownloaderBot')
                                os.remove(filename)
                    else:
                        # Это изображение
                        images_urls = result.get("items", [])
                        for img_url in images_urls:
                            await self.telegram_app.bot.send_photo(chat_id=chat_id, photo=img_url)
                else:
                    await self.telegram_app.bot.send_message(chat_id=chat_id, text=f"Не удалось обработать TikTok ссылку: {e}")
            except Exception as e2:
                await self.telegram_app.bot.send_message(chat_id=chat_id, text=f"Ошибка при скачивании TikTok контента: {e2}")
    
    async def handle_instagram_link(self, link, chat_id):
        await self.telegram_app.bot.send_message(chat_id=chat_id, text="Скачивание Instagram контента...")
        try:
            # Используем instaloader для скачивания Instagram контента
            from instaloader import Instaloader, Post
            import tempfile
            
            # Создаем экземпляр Instaloader
            L = Instaloader()
            
            # Если есть сессия, загружаем её
            if Config.USER:
                session_file = f"session-{Config.USER}"
                if os.path.exists(session_file):
                    L.load_session_from_file(Config.USER, session_file)
            
            # Извлекаем URL поста из ссылки
            post_shortcode = self.extract_instagram_shortcode(link)
            if post_shortcode:
                post = Post.from_shortcode(L.context, post_shortcode)
                
                # Скачиваем медиафайл
                with tempfile.TemporaryDirectory() as temp_dir:
                    try:
                        L.download_post(post, target=temp_dir)
                        
                        # Находим скачанные файлы
                        files_sent = False
                        for root, dirs, files in os.walk(temp_dir):
                            for file in files:
                                if file.endswith(('.jpg', '.mp4', '.jpeg', '.png', '.mov')):
                                    file_path = os.path.join(root, file)
                                    
                                    # Проверяем размер файла перед отправкой
                                    file_size = os.path.getsize(file_path)
                                    if file_size > 20 * 1024 * 1024:  # 20MB - лимит Telegram
                                        await self.telegram_app.bot.send_message(
                                            chat_id=chat_id,
                                            text=f"Файл слишком большой для отправки в Telegram ({file_size / (1024*1024):.1f}MB).\nСсылка на скачивание: {link}"
                                        )
                                        continue  # Пропускаем отправку этого файла
                                    
                                    if file.endswith('.mp4'):
                                        await self.telegram_app.bot.send_video(chat_id=chat_id, video=open(file_path, 'rb'))
                                    elif file.endswith(('.jpg', '.jpeg', '.png')):
                                        await self.telegram_app.bot.send_photo(chat_id=chat_id, photo=open(file_path, 'rb'))
                                    else:
                                        await self.telegram_app.bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
                                    files_sent = True
                        
                        if not files_sent:
                            await self.telegram_app.bot.send_message(
                                chat_id=chat_id,
                                text=f"Не удалось скачать медиафайлы из Instagram поста. Попробуйте альтернативный метод: {link}"
                            )
                    except Exception as download_error:
                        # Если основной метод не работает, пробуем использовать веб-запрос
                        await self.telegram_app.bot.send_message(
                            chat_id=chat_id,
                            text=f"Не удалось скачать через Instaloader, пробуем альтернативный метод: {link}"
                        )
            else:
                await self.telegram_app.bot.send_message(chat_id=chat_id, text="Не удалось извлечь информацию из Instagram ссылки")
        except Exception as e:
            await self.telegram_app.bot.send_message(chat_id=chat_id, text=f"Ошибка при скачивании Instagram контента: {e}")

    def extract_instagram_shortcode(self, url):
        """Извлекает shortcode из Instagram URL"""
        import re
        regex = r"(?<=instagram\.com/p/)[a-zA-Z0-9_-]+|(?<=instagram\.com/reel/)[a-zA-Z0-9_-]+|(?<=instagr\.am/p/)[a-zA-Z0-9_-]+"
        match = re.search(regex, url)
        return match.group(0) if match else None
    async def handle_youtube_link(self, link, chat_id):
        await self.telegram_app.bot.send_message(chat_id=chat_id, text="Скачивание YouTube контента...")
        try:
            # Используем yt-dlp для скачивания YouTube видео
            from yt_dlp import YoutubeDL
            import tempfile
            
            # Сначала пробуем скачать видео (лучшее доступное качество)
            ydl_opts_video = {
                'outtmpl': os.path.join(tempfile.gettempdir(), '%(title)s.%(ext)s'),
                'max_filesize': 50 * 1024 * 1024,  # 50MB лимит для Telegram
                'format': 'best[height<=720][ext=mp4][filesize<50M]/best[ext=mp4][filesize<50M]/best[filesize<50M]',
            }
            
            with YoutubeDL(ydl_opts_video) as ydl:
                info = ydl.extract_info(link, download=True)
                filename = ydl.prepare_filename(info)
                
                # Проверяем размер файла перед отправкой
                file_size = os.path.getsize(filename)
                if file_size > 20 * 1024 * 1024:  # 20MB - лимит Telegram
                    await self.telegram_app.bot.send_message(
                        chat_id=chat_id,
                        text=f"Видео слишком большое для отправки в Telegram ({file_size / (1024*1024):.1f}MB).\nСсылка на скачивание: {link}"
                    )
                    os.remove(filename)
                    return
                
                # Проверяем, является ли файл видео
                if info.get('ext') in ['mp4', 'mov', 'avi', 'mkv', 'webm']:
                    # Это видео - пробуем отправить как видео
                    try:
                        await self.telegram_app.bot.send_video(chat_id=chat_id, video=open(filename, 'rb'))
                    except Exception:
                        # Если не удалось отправить как видео, пробуем как документ
                        await self.telegram_app.bot.send_document(chat_id=chat_id, document=open(filename, 'rb'))
                else:
                    # Это аудио - отправляем как аудио
                    await self.telegram_app.bot.send_audio(chat_id=chat_id, audio=open(filename, 'rb'))
                
                # Удаляем файл после отправки
                os.remove(filename)
        except Exception as e:
            # Если не удалось скачать как видео, пробуем скачать только аудио
            try:
                from yt_dlp import YoutubeDL
                import tempfile
                
                ydl_opts_audio = {
                    'outtmpl': os.path.join(tempfile.gettempdir(), '%(title)s.%(ext)s'),
                    'max_filesize': 50 * 1024 * 1024,
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                
                with YoutubeDL(ydl_opts_audio) as ydl:
                    info = ydl.extract_info(link, download=True)
                    filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
                    
                    # Проверяем размер файла перед отправкой
                    file_size = os.path.getsize(filename)
                    if file_size > 20 * 1024 * 1024:  # 20MB - лимит Telegram
                        await self.telegram_app.bot.send_message(
                            chat_id=chat_id,
                            text=f"Аудио слишком большое для отправки в Telegram ({file_size / (1024*1024):.1f}MB).\nСсылка на скачивание: {link}"
                        )
                        os.remove(filename)
                        return
                    
                    # Отправляем аудио
                    await self.telegram_app.bot.send_audio(chat_id=chat_id, audio=open(filename, 'rb'))
                    
                    # Удаляем файл после отправки
                    os.remove(filename)
            except Exception as e2:
                await self.telegram_app.bot.send_message(chat_id=chat_id, text=f"Ошибка при скачивании YouTube контента: {e2}")

    async def handle_twitter_link(self, link, chat_id):
        await self.telegram_app.bot.send_message(chat_id=chat_id, text="Скачивание Twitter контента...")
        try:
            # Используем tweepy для аутентификации
            auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
            auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)
            
            # Извлекаем ID твита из ссылки
            pattern = r'twitter\.com/.+?/status/(\d+)'
            match = re.search(pattern, link)
            if match:
                tweet_id = match.group(1)
                tweet = api.get_status(tweet_id, tweet_mode='extended')
                
                # Проверяем, есть ли медиа в твите
                if hasattr(tweet, 'extended_entities'):
                    media_list = tweet.extended_entities['media']
                    for media in media_list:
                        if media['type'] == 'photo':
                            # Отправляем фото
                            await self.telegram_app.bot.send_photo(chat_id=chat_id, photo=media['media_url'])
                        elif media['type'] in ['video', 'animated_gif']:
                            # Для видео и гифок используем yt-dlp
                            video_info = media['video_info']
                            if 'variants' in video_info:
                                # Находим лучший вариант видео
                                video_url = max(
                                    [v for v in video_info['variants'] if v.get('content_type') == 'video/mp4'],
                                    key=lambda x: x.get('bitrate', 0),
                                    default=None
                                )
                                
                                if video_url:
                                    # Используем yt-dlp для скачивания видео
                                    import tempfile
                                    
                                    with tempfile.TemporaryDirectory() as temp_dir:
                                        # Создаем временное имя файла
                                        temp_video_path = os.path.join(temp_dir, "twitter_video.mp4")
                                        
                                        # Скачиваем видео
                                        import requests
                                        response = requests.get(video_url['url'])
                                        with open(temp_video_path, 'wb') as f:
                                            f.write(response.content)
                                        
                                        # Проверяем размер файла перед отправкой
                                        file_size = os.path.getsize(temp_video_path)
                                        if file_size > 20 * 1024 * 1024:  # 20MB - лимит Telegram
                                            await self.telegram_app.bot.send_message(
                                                chat_id=chat_id,
                                                text=f"Видео слишком большое для отправки в Telegram ({file_size / (1024*1024):.1f}MB).\nСсылка на скачивание: {link}"
                                            )
                                        else:
                                            # Отправляем видео в Telegram
                                            await self.telegram_app.bot.send_video(chat_id=chat_id, video=open(temp_video_path, 'rb'))
                                else:
                                    await self.telegram_app.bot.send_message(chat_id=chat_id, text=f"Видео из твита: {link}")
                        else:
                            await self.telegram_app.bot.send_message(chat_id=chat_id, text=f"Неизвестный тип медиа в твите: {media['type']}")
                else:
                    # Просто текст твита
                    await self.telegram_app.bot.send_message(chat_id=chat_id, text=f"Текст твита: {tweet.full_text}")
            else:
                await self.telegram_app.bot.send_message(chat_id=chat_id, text="Не удалось распознать Twitter ссылку")
        except Exception as e:
            await self.telegram_app.bot.send_message(chat_id=chat_id, text=f"Ошибка при скачивании Twitter контента: {e}")

    def run(self):
        print('Запуск универсального бота...')
        try:
            self.telegram_app.run_polling(poll_interval=3, allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            print(f'Ошибка при запуске бота: {e}')
            # Перезапускаем бота через некоторое время
            import time
            time.sleep(5)
            self.telegram_app.run_polling(poll_interval=3, allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    bot = DownloaderBot()
    bot.run()