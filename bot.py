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

    # Füge einen Handler für /start hinzu
    app.add_handler(CommandHandler("start", start))

    # Setze den Webhook für den Bot
    await app.bot.set_webhook(WEBHOOK_URL)

    # Starte den Bot
    await app.start()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
