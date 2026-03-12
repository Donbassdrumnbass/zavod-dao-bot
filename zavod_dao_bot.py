"""
ЗАВОД DAO — Telegram Aggregator Bot
"""

from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ============================================================
# 🔑 ДАННЫЕ
# ============================================================
API_ID = 33739613
API_HASH = "9cff7d08655717927a7f5e4ed64cae2b"
BOT_TOKEN = "8772294114:AAHExInjuEa_Z_droP06DDs6ZY6mW58i_9g"
TARGET_CHANNEL = "@zavod_dao"
ADMIN_ID = 1873762723
SESSION_STRING = "1ApWapzMBuwg43l7ZUrCuurEkZOZW-N2Pg5Fq07p-wnOgSyIv7f0u7dg5nwpnwgh9ldOkSupQqy5kiP_kCaFx6FaI8LCGVQcflPV0z1QAMLYx_yGIyeYP3rUpsKXUmrZF7DZiqV_DD3vZJD21cwrnKIPCpj1BRIe906lyNss4zMO5rdSHhMXFtKgGSTWx3xDm2i7NbhDSe1EVeBZlvDsUQauYIZTZ8tumgj6DfnXGYF8uVVRBL0sg5PwoY9srVq_QfOqtre_AbHex-Cju3gPtucMiHmIyeUW_JHYZFp2a8OCWFxt-zCaoyEyyqGNW5Ke0UGCKlHKjGk8tdIOFHnan_EB4jM35AqQ="  # сюда вставим строку сессии

# ============================================================
# 📋 СПИСОК КАНАЛОВ
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
    "cryptoinsider_ru",
    "ru_btc",
    "cryptorussia",
]

# ============================================================
# 🚫 ЧЁРНЫЙ СПИСОК
# ============================================================
BLACKLIST = [
    "реклама", "на правах рекламы", "партнёрский материал",
    "промо", "спонсор", "совместно с", "при поддержке",
    "#реклама", "#промо", "#ad", "#sponsored", "#partner",
    "купить сейчас", "успей купить", "ограниченное предложение",
    "только сегодня", "промокод", "реферальная ссылка",
    "пригласи друга", "пассивный доход", "гарантированная прибыль",
    "подпишись на", "подписывайся на", "наш партнёр",
    "раздача токенов", "бесплатные монеты", "удвоение",
    "вип группа", "закрытый клуб", "слив сигналов",
    "розыгрыш", "разыгрываем",
]

# ============================================================
# ✅ БЕЛЫЙ СПИСОК
# ============================================================
WHITELIST = [
    "bitcoin", "btc", "ethereum", "eth", "sec",
    "etf", "халвинг", "halving", "blackrock",
    "binance", "coinbase", "регулирование",
    "обвал", "рост", "ath", "рекорд",
]

# ============================================================
# 📝 МЕНЮ
# ============================================================
WELCOME_TEXT = """
👋 Привет! Это бот канала <b>Завод DAO</b>

📡 Агрегируем лучшие крипто-посты без рекламы и спама.

Выбери раздел 👇
"""

COOPERATION_TEXT = """
🤝 <b>Сотрудничество с Завод DAO</b>

📌 <b>Добавление в агрегатор</b>
Ваш канал попадает в список источников — лучшие посты будут репоститься к нам.

📢 <b>Рекламная интеграция</b>
Размещение поста о вашем канале или проекте.

📊 <b>Совместные активности</b>
Коллаборации, кросс-промо.

✉️ <b>Для связи:</b> @Donbassdrumnbass

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
# КОД
# ============================================================

def is_blacklisted(text: str) -> bool:
    text_lower = text.lower()
    for word in WHITELIST:
        if word.lower() in text_lower:
            return False
    for word in BLACKLIST:
        if word.lower() in text_lower:
            return True
    return False

async def run_reader():
    if not SESSION_STRING:
        print("SESSION_STRING пустой — читатель каналов не запущен")
        return
    reader = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await reader.start()
    print("✅ Читатель каналов запущен")

    @reader.on(events.NewMessage(chats=SOURCE_CHANNELS))
    async def handler(event):
        try:
            message = event.message
            if not message:
                return
            text = message.text or ""
            if is_blacklisted(text):
                print(f"🚫 Заблокирован: {text[:50]}")
                return
            await reader.forward_messages(TARGET_CHANNEL, message)
            print(f"✅ Опубликован пост из {event.chat.username}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")

    await reader.run_until_disconnected()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Наш канал", url="https://t.me/zavod_dao")],
        [InlineKeyboardButton("🤝 Сотрудничество", callback_data="cooperation")],
        [InlineKeyboardButton("ℹ️ О нас", callback_data="about")],
    ]
    await update.message.reply_html(WELCOME_TEXT, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    back_btn = [[InlineKeyboardButton("◀️ Назад", callback_data="back")]]
    if query.data == "cooperation":
        await query.edit_message_text(COOPERATION_TEXT, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(back_btn))
    elif query.data == "about":
        await query.edit_message_text(ABOUT_TEXT, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(back_btn))
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("📢 Наш канал", url="https://t.me/zavod_dao")],
            [InlineKeyboardButton("🤝 Сотрудничество", callback_data="cooperation")],
            [InlineKeyboardButton("ℹ️ О нас", callback_data="about")],
        ]
        await query.edit_message_text(WELCOME_TEXT, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

async def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    print("✅ Бот с меню запущен")
    await asyncio.Event().wait()

async def main():
    print("🚀 Zavod DAO starting...")
    print("Bot started")
    tasks = [run_bot()]
    if SESSION_STRING:
        tasks.append(run_reader())
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
