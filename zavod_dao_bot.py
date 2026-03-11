"""
ЗАВОД DAO — Telegram Aggregator Bot
=====================================
Установка: pip install telethon python-telegram-bot
Запуск: python zavod_dao_bot.py
"""

from telethon import TelegramClient, events
from telethon.tl.types import MessageEntityUrl, MessageEntityTextUrl
import asyncio
import re

# ============================================================
# 🔑 ТВОИ ДАННЫЕ — ВСТАВЬ СЮДА
# ============================================================
API_ID = 33739613               # твой api_id с my.telegram.org
API_HASH = "9cff7d08655717927a7f5e4ed64cae2b"      # твой api_hash с my.telegram.org
BOT_TOKEN = "8772294114:AAHExInjuEa_Z_droP06DDs6ZY6mW58i_9g
"   # токен от @BotFather
TARGET_CHANNEL = "@zavod_dao"   # твой канал куда публикуем
ADMIN_ID = 1873762723            # твой Telegram ID (узнай у @userinfobot)

# ============================================================
# 📋 СПИСОК КАНАЛОВ-ИСТОЧНИКОВ — добавляй и убирай каналы
# ============================================================
SOURCE_CHANNELS = [
    # Твои каналы
    "@natykcryptooo",
    "@Slavik_investor_updates",
    "@mykytaio",
    "@speculator_guy",
    "@CryptoTravelsWithDmytro",
    "@Defiscamcheck",
    "@danokhlopkov",
    "@skhema_crypto",
    "@eligible4",
    "@maisonuranus",
    "@TeddyinCrypto",
    "@AI_Handler",
    "@KriptoUkraine",
    "@Crypt0Hermes",
    "@idoresearch",
    "@GentleChron",
    "@digitalbios",
    "@Yung_HoDler",
    "@TeddyDrops",
    "@autofina",
    "@afina_io",
    "@OOO_ZavodDAO",
    # Русскоязычные топ-каналы
    "@forklog",
    "@bits_media",
    "@cryptonewsru",
    "@coinmarketcap_ru",
    "@binance_russian",
    "@bybit_russian",
    "@crypto_godfather",
    "@prostocoin",
    "@cryptoalert_ru",
    "@whalesinside",
    "@cryptoportal",
    "@beincrypto_russian",
    "@incrypted",
    "@cryptokrot",
    "@mmgp_bitcoin",
    "@cryptoinsider_ru",
    "@tcanalysis",
    "@ru_btc",
    "@cryptorussia",
    "@cryptoportal",
]

# ============================================================
# 🚫 ЧЁРНЫЙ СПИСОК — посты с этими словами НЕ публикуются
# ============================================================
BLACKLIST = [
    # Прямая реклама
    "реклама", "на правах рекламы", "партнёрский материал",
    "промо", "спонсор", "совместно с", "при поддержке",
    "#реклама", "#промо", "#ad", "#sponsored", "#partner",
    # Продажи
    "купить сейчас", "успей купить", "ограниченное предложение",
    "только сегодня", "промокод", "реферальная ссылка",
    "пригласи друга", "пассивный доход",
    "гарантированная прибыль", "сигналы на",
    # Накрутка
    "подпишись на", "подписывайся на", "наш канал",
    "перейди по ссылке", "жми сюда", "переходи",
    "наш партнёр", "читай здесь",
    # Скам
    "раздача токенов", "бесплатные монеты", "удвоение",
    "x100 прибыли", "x1000", "инсайд слив",
    "вип группа", "закрытый клуб", "слив сигналов",
    # Розыгрыши
    "розыгрыш", "розыгрыша", "разыгрываем", "победитель получит",
    "участвуй в розыгрыше",
]

# ============================================================
# ✅ БЕЛЫЙ СПИСОК — посты с этими словами публикуются ВСЕГДА
# ============================================================
WHITELIST = [
    "bitcoin", "btc", "ethereum", "eth", "sec",
    "etf", "халвинг", "halving", "blackrock",
    "binance", "coinbase", "регулирование",
    "крах", "обвал", "рост", "ath", "рекорд",
]

# ============================================================
# 📝 ТЕКСТ ДЛЯ МЕНЮ БОТА
# ============================================================
WELCOME_TEXT = """
👋 Привет! Это бот канала <b>Завод DAO</b>

📡 Мы агрегируем лучшие крипто-посты без рекламы и спама.

Выбери раздел 👇
"""

COOPERATION_TEXT = """
🤝 <b>Сотрудничество с Завод DAO</b>

Мы рассматриваем следующие форматы:

📌 <b>Добавление в агрегатор</b>
Ваш канал попадает в список источников — лучшие посты будут репоститься к нам.
Требования: тематика крипта, минимум рекламы, живая аудитория.

📢 <b>Рекламная интеграция</b>
Размещение поста о вашем канале или проекте в нашем агрегаторе.

📊 <b>Совместные активности</b>
Коллаборации, совместные публикации, кросс-промо.

✉️ <b>Для связи пишите:</b> @manager_rekt

Мы ответим в течение 24 часов.
"""

ABOUT_TEXT = """
📡 <b>Завод DAO Агрегатор</b>

Собираем лучшее из крипто-каналов в одном месте.

✅ Без рекламы
✅ Без спама  
✅ Только полезный контент

📢 Канал: @zavod_dao
"""

# ============================================================
# КОД БОТА — ничего ниже менять не нужно
# ============================================================

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Клиент для чтения каналов
reader = TelegramClient('zavod_dao_session', API_ID, API_HASH)

def is_blacklisted(text: str) -> bool:
    """Проверяем есть ли в посте запрещённые слова"""
    text_lower = text.lower()
    # Сначала проверяем белый список — если есть важное слово, пропускаем
    for word in WHITELIST:
        if word.lower() in text_lower:
            return False
    # Проверяем чёрный список
    for word in BLACKLIST:
        if word.lower() in text_lower:
            return True
    return False

async def forward_post(event):
    """Пересылаем пост в наш канал"""
    try:
        message = event.message
        if not message or not message.text and not message.media:
            return
        text = message.text or ""
        # Проверяем чёрный список
        if is_blacklisted(text):
            print(f"🚫 Пост заблокирован (чёрный список): {text[:50]}...")
            return
        # Пересылаем пост
        await reader.forward_messages(TARGET_CHANNEL, message)
        print(f"✅ Пост опубликован из {event.chat.username}")
    except Exception as e:
        print(f"❌ Ошибка при пересылке: {e}")

# Меню бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Наш канал", url=f"https://t.me/zavod_dao")],
        [InlineKeyboardButton("🤝 Сотрудничество", callback_data="cooperation")],
        [InlineKeyboardButton("ℹ️ О нас", callback_data="about")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_html(WELCOME_TEXT, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "cooperation":
        keyboard = [[InlineKeyboardButton("◀️ Назад", callback_data="back")]]
        await query.edit_message_text(
            COOPERATION_TEXT,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "about":
        keyboard = [[InlineKeyboardButton("◀️ Назад", callback_data="back")]]
        await query.edit_message_text(
            ABOUT_TEXT,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("📢 Наш канал", url="https://t.me/zavod_dao")],
            [InlineKeyboardButton("🤝 Сотрудничество", callback_data="cooperation")],
            [InlineKeyboardButton("ℹ️ О нас", callback_data="about")],
        ]
        await query.edit_message_text(
            WELCOME_TEXT,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def run_reader():
    """Запускаем чтение каналов"""
    await reader.start()
    print("✅ Читатель каналов запущен")

    @reader.on(events.NewMessage(chats=SOURCE_CHANNELS))
    async def handler(event):
        await forward_post(event)

    await reader.run_until_disconnected()

async def run_bot():
    """Запускаем бота с меню"""
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    print("✅ Бот с меню запущен")
    await asyncio.Event().wait()

async def main():
    """Запускаем всё вместе"""
    print("🚀 Завод DAO Агрегатор запускается...")
    await asyncio.gather(
        run_reader(),
        run_bot(),
    )

if __name__ == "__main__":
    asyncio.run(main())
