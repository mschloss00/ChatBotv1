import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram token and webhook URL from environment variables
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = "https://chatbotv1-ocy6.onrender.com/webhook"

async def start(update: Update, context):
    await update.message.reply_text('Hello! I am your bot.')

async def main():
    # Create the Application object and initialize it
    app = Application.builder().token(TOKEN).build()

    # Set up command handlers
    app.add_handler(CommandHandler("start", start))

    # Set the webhook
    await app.bot.set_webhook(WEBHOOK_URL)

    # Initialize the application
    await app.initialize()

    # Start the application webhook
    await app.start()

    # Keep the bot running
    await app.updater.start_polling()

if __name__ == '__main__':
    # Run the asynchronous main function
    asyncio.run(main())
