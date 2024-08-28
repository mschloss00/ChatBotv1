from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from gtts import gTTS
import os

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: Application):
    await update.message.reply_text('Willkommen! Du kannst wählen, ob ich in Text oder als Sprachnachricht antworte.')

import tempfile

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
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('voice_mode', toggle_voice_mode))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_response))

    await app.run_polling()

if __name__ == '__main__':
    import asyncio

    try:
        # Prüfen, ob bereits ein Event-Loop läuft
        loop = asyncio.get_running_loop()
    except RuntimeError:  # Kein Event-Loop aktiv
        loop = None

    if loop and loop.is_running():
        # Falls der Event-Loop läuft, main() als Aufgabe hinzufügen und laufen lassen
        loop.run_until_complete(main())
    else:
        # Wenn kein Event-Loop aktiv ist, starte einen neuen
        asyncio.run(main())
