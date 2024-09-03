import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai

# OpenAI API-Key
openai.api_key = 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

# Logging-Konfiguration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Funktion für die Interaktion mit ChatGPT
def gpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Start-Funktion
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hallo! Ich bin Thomas, dein IT-Experte. Wie kann ich dir helfen?')

# Funktion, um auf Nachrichten zu reagieren
def respond(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    # Anpassung des Prompts für die spezielle Persönlichkeit
    prompt = f"Du bist Thomas, ein 60-jähriger IT-Experte mit 40 Jahren Erfahrung. Antworte auf folgende Frage:\n{user_message}"
    bot_response = gpt_response(prompt)
    update.message.reply_text(bot_response)

# Hauptfunktion zum Starten des Bots
def main():
    # Telegram-Bot Token
    updater = Updater("DEIN_TELEGRAM_BOT_TOKEN", use_context=True)

    # Dispatcher zum Registrieren der Handler
    dp = updater.dispatcher

    # Befehle und Nachrichten-Handler
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, respond))

    # Starten des Bots
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
