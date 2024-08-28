from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from gtts import gTTS
import os
import tempfile

# Den Telegram-Bot-Token als Umgebungsvariable abrufen
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context):
    await update.message.reply_text('Willkommen! Du kannst wählen, ob ich in Text oder als Sprachnachricht antworte.')

async def text_response(update: Update, context):
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

async def toggle_voice_mode(update: Update, context):
    current_mode = context.user_data.get('voice_mode', False)
    context.user_data['voice_mode'] = not current_mode
    mode = 'Sprachnachrichten' if context.user_data['voice_mode'] else 'Textnachrichten'
    await update.message.reply_text(f'Antwortmodus geändert zu: {mode}')

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handler für Befehle und Nachrichten hinzufügen
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('voice_mode', toggle_voice_mode))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_response))

    # Telegram Bot Polling starten, ohne auf das Event-Loop-Management explizit zuzugreifen
    app.run_polling()

if __name__ == '__main__':
    main()
