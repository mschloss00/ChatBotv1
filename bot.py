import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler
from flask import Flask, request

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

# Initialize the Telegram bot application
telegram_app = Application.builder().token(TOKEN).build()

# Telegram command handler
async def start(update: Update, context):
    await update.message.reply_text('Hello! I am your bot.')

# Add the command handler to the Telegram bot application
telegram_app.add_handler(CommandHandler("start", start))

# Route for Telegram Webhook
@flask_app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        # Process the incoming Telegram update
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        asyncio.run(telegram_app.process_update(update))
        return "OK", 200

async def main():
    # Set the webhook for Telegram
    await telegram_app.bot.set_webhook(WEBHOOK_URL)
    
    # Start the Telegram bot application
    await telegram_app.start()
    logger.info("Telegram bot started")
    
    # Keep the bot running
    await telegram_app.updater.start_polling()

if __name__ == '__main__':
    # Start the Flask app on the port Render provides
    port = int(os.environ.get("PORT", 5000))
    
    # Start Flask in a separate thread
    import threading
    flask_thread = threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=port))
    flask_thread.start()

    # Run the Telegram bot in the main thread
    asyncio.run(main())
