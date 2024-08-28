import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler
from flask import Flask

# Set up Flask app
flask_app = Flask(__name__)

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

    # Start the webhook service
    logger.info("Application started")

    # Keep the application running
    await app.start()

    # Sleep forever to keep the process alive
    await asyncio.Event().wait()

@flask_app.route('/')
def index():
    return "Bot is running!"

if __name__ == '__main__':
    # Start the Flask app in a separate thread to ensure Render detects the open port
    import threading
    flask_thread = threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000))))
    flask_thread.start()

    # Run the asynchronous main function for the Telegram bot
    asyncio.run(main())
