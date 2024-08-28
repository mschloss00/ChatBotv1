import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from gtts import gTTS
import tempfile
import asyncio

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Deine Render-URL als Webhook URL
WEBHOOK_URL = "https://chatbotv1-ocy6.onrender.com/webhook"

async def start(update: Update, context: Application):
    await update.message.reply_text('Willkommen! Du kannst wählen, ob ich in Text oder als Sprachnachricht antworte.')

async def text_response(update: Update, context: Application):
    user_message = update.message.text
    response_text = f'Du hast gesagt: {user_message}'

    if context.user_data.get('voice_mode', False):
        tts = gTTS(text=response_text, lang='de')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            await update.message.reply_voice(voice=open(tmp_file.name, 'rb'))
        os.remove(tmp_file.name)
    else:
        await update.message.reply_text(response_text)

async def toggle_voice_mode(update: Update, context: Application):
    current_mode = context.user_data.get('voice_mode', False)
    context.user_data['voice_mode'] = not current_mode
    mode = 'Sprachnachrichten' if context.user_data['voice_mode'] else 'Textnachrichten'
    await update.message.reply_text(f'Antwortmodus geändert zu: {mode}')

async def main():
    # Telegram Application erstellen
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handler für Kommandos und Nachrichten hinzufügen
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('voice_mode', toggle_voice_mode))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_response))

    # Webhook einrichten
    await app.bot.set_webhook(WEBHOOK_URL)

    # Starten des Webhook-Servers
    await app.start_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get('PORT', 5000)),
        url_path="/webhook"
    )

    # App laufen lassen
    await app.updater.start_polling()

if __name__ == '__main__':
    try:
        # Überprüfen, ob bereits ein Event-Loop läuft
        loop = asyncio.get_running_loop()
    except RuntimeError:  # Kein Event-Loop aktiv
        loop = None

    if loop and loop.is_running():
        loop.create_task(main())
    else:
        asyncio.run(main())
