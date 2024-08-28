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
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = "https://chatbotv1-ocy6.onrender.com/webhook"

async def start(update: Update, context):
    await update.message.reply_text('Hello! I am your bot.')

def main():
    # Create the Application object
    app = Application.builder().token(TOKEN).build()

    # Set up command handlers
    app.add_handler(CommandHandler("start", start))

    # Start the webhook
    async def run_webhook():
        # Set the webhook once and check if it's needed to reset again
        await app.bot.set_webhook(WEBHOOK_URL)

        # Start receiving updates via webhook
        await app.start()

        # Run the application until interrupted
        await app.updater.start_polling()

    # Run the async function
    asyncio.run(run_webhook())

if __name__ == '__main__':
    main()
