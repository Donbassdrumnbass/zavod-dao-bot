"""
ЗАВОД DAO — Telegram Aggregator Bot
"""

from telethon import TelegramClient, events
import asyncio

# ============================================================
# ДАННЫЕ
# ============================================================
API_ID = 33739613
API_HASH = "9cff7d08655717927a7f5e4ed64cae2b"
BOT_TOKEN = "8772294114:AAHExInjuEa_Z_droP06DDs6ZY6mW58i_9g"
TARGET_CHANNEL = "@zavod_dao"
ADMIN_ID = 1873762723

# ============================================================
# СПИСОК КАНАЛОВ-ИСТОЧНИКОВ
# ============================================================
SOURCE_CHANNELS = [
    "natykcryptooo",
    "Slavik_investor_updates",
    "mykytaio",
    "speculator_guy",
    "CryptoTravelsWithDmytro",
    "Defiscamcheck",
    "danokhlopkov",
    "skhema_crypto",
    "eligible4",
    "maisonuranus",
    "TeddyinCrypto",
    "AI_Handler",
    "KriptoUkraine",
    "Crypt0Hermes",
    "idoresearch",
    "GentleChron",
    "digitalbios",
    "Yung_HoDler",
    "TeddyDrops",
    "autofina",
    "afina_io",
    "OOO_ZavodDAO",
    "forklog",
    "bits_media",
    "coinmarketcap_ru",
    "binance_russian",
    "bybit_russian",
    "prostocoin",
    "whalesinside",
    "beincrypto_russian",
    "incrypted",
    "cryptokrot",
    "tcanalysis",
    "ru_btc",
]

# ============================================================
# ЧЁРНЫЙ СПИСОК — посты с этими словами НЕ публикуются
# ============================================================
BLACKLIST = [
    "реклама", "на правах рекламы", "партнёрский материал",
    "промо", "спонсор", "совместно с", "при поддержке",
    "#реклама", "#промо", "#ad", "#sponsored", "#partner",
    "купить сейчас", "успей купить", "ограниченное предложение",
    "только сегодня", "промокод", "реферальная ссылка",
    "пригласи друга", "пассивный доход",
    "гарантированная прибыль",
    "подпишись на", "подписывайся на",
    "перейди по ссылке", "жми сюда",
    "наш партнёр", "читай здесь",
    "раздача токенов", "бесплатные монеты", "удвоение",
    "вип группа", "закрытый клуб", "слив сигналов",
    "розыгрыш", "разыгрываем", "участвуй в розыгрыше",
]

# ============================================================
# БЕЛЫЙ СПИСОК — эти посты публикуются ВСЕГДА
# ============================================================
WHITELIST = [
    "bitcoin", "btc", "ethereum", "eth", "sec",
    "etf", "халвинг", "halving", "blackrock",
    "binance", "coinbase", "регулирование",
    "крах", "обвал", "рост", "ath", "рекорд",
]

# ============================================================
# ТЕКСТЫ МЕНЮ
# ============================================================
WELCOME_TEXT = """
👋 Привет! Это бот канала <b>Завод DAO</b>

📡 Мы агрегируем лучшие крипто-посты без рекламы и спама.

Выбери раздел 👇
"""

COOPERATION_TEXT = """
🤝 <b>Сотрудничество с Завод DAO</b>

📌 <b>Добавление в агрегатор</b>
Ваш канал попадает в список источников — лучшие посты будут репоститься к нам.
Требования: тематика крипта, минимум рекламы, живая аудитория.

📢 <b>Рекламная интеграция</b>
Размещение поста о вашем канале или проекте.

📊 <b>Совместные активности</b>
Коллаборации, кросс-промо.

✉️ <b>Для связи пишите:</b> @Donbassdrumnbass

Ответим в течение 24 часов.
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
# КОД БОТА
# ============================================================

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

reader = TelegramClient("zavod_dao_session", API_ID, API_HASH)


def is_blacklisted(text: str) -> bool:
    text_lower = text.lower()
    for word in WHITELIST:
        if word.lower() in text_lower:
            return False
    for word in BLACKLIST:
        if word.lower() in text_lower:
            return True
    return False


async def forward_post(event):
    try:
        message = event.message
        if not message:
            return
        text = message.text or ""
        if is_blacklisted(text):
            print(f"BLOCKED: {text[:50]}")
            return
        await reader.forward_messages(TARGET_CHANNEL, message)
        print(f"POSTED from {event.chat.username}")
    except Exception as e:
        print(f"ERROR: {e}")


async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("📢 Наш канал", url="https://t.me/zavod_dao")],
        [InlineKeyboardButton("🤝 Сотрудничество", callback_data="cooperation")],
        [InlineKeyboardButton("ℹ️ О нас", callback_data="about")],
    ]
    await update.message.reply_html(WELCOME_TEXT, reply_markup=InlineKeyboardMarkup(keyboard))


async def button_handler(update, context):
    query = update.callback_query
    await query.answer()
    back = [[InlineKeyboardButton("◀️ Назад", callback_data="back")]]
    if query.data == "cooperation":
        await query.edit_message_text(COOPERATION_TEXT, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(back))
    elif query.data == "about":
        await query.edit_message_text(ABOUT_TEXT, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(back))
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("📢 Наш канал", url="https://t.me/zavod_dao")],
            [InlineKeyboardButton("🤝 Сотрудничество", callback_data="cooperation")],
            [InlineKeyboardButton("ℹ️ О нас", callback_data="about")],
        ]
        await query.edit_message_text(WELCOME_TEXT, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))


async def run_reader():
    await reader.start()
    print("Reader started")

    @reader.on(events.NewMessage(chats=SOURCE_CHANNELS))
    async def handler(event):
        await forward_post(event)

    await reader.run_until_disconnected()


async def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    print("Bot started")
    await asyncio.Event().wait()


async def main():
    print("Zavod DAO starting...")
    await asyncio.gather(run_reader(), run_bot())


if __name__ == "__main__":
    asyncio.run(main())
