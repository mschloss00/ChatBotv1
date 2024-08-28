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
        update = Update
