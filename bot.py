import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Konfiguration des Loggings
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Dein Bot Token und Webhook URL
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = "https://chatbotv1-ocy6.onrender.com/webhook"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sendet eine Nachricht, wenn der Befehl /start gesendet wird."""
    await update.message.reply_text("Hallo! Ich bin dein Bot.")

async def main():
    """Startet den Bot."""
    # Erstelle die Application und setze den Bot-Token
    app = Application.builder().token(BOT_TOKEN).build()

 # Prüfe, ob der Webhook bereits gesetzt ist
    webhook_info = await app.bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await app.bot.set_webhook(WEBHOOK_URL)

    # Initialisiere die Application
    await app.initialize()

    # Setze den Webhook für den Bot
    await app.bot.set_webhook(WEBHOOK_URL)

    # Starte den Bot
    await app.start()

    # Halte den Bot am Laufen
    await app.updater.start_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
