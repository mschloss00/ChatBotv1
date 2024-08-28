from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from gtts import gTTS
import os

# Füge deinen neuen Token hier ein
TELEGRAM_TOKEN = '7508808182:AAEl7yS5Me425PumMYYDzRi1KoFu3dsgVLM'

# Funktion für den Start-Befehl
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Willkommen! Du kannst wählen, ob ich in Text oder als Sprachnachricht antworte.')

# Funktion, die Textnachrichten verarbeitet
async def text_response(update: Update, context: CallbackContext):
    user_message = update.message.text
    response_text = f'Du hast gesagt: {user_message}'  # Hier kannst du später eine NLP-Logik einbauen

    # Falls der User Sprachantworten möchte
    if context.user_data.get('voice_mode', False):
        tts = gTTS(text=response_text, lang='de')
        tts.save('response.mp3')
        await update.message.reply_voice(voice=open('response.mp3', 'rb'))
        os.remove('response.mp3')  # Löscht die Datei nach dem Senden
    else:
        await update.message.reply_text(response_text)

# Funktion zum Umschalten zwischen Text- und Sprachmodus
async def toggle_voice_mode(update: Update, context: CallbackContext):
    current_mode = context.user_data.get('voice_mode', False)
    context.user_data['voice_mode'] = not current_mode
    mode = 'Sprachnachrichten' if context.user_data['voice_mode'] else 'Textnachrichten'
    await update.message.reply_text(f'Antwortmodus geändert zu: {mode}')

async def main():
    # Erstelle die Anwendung
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Befehle
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('voice_mode', toggle_voice_mode))

    # Textnachrichten
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_response))

    # Startet den Bot
    await app.start_polling()
    await app.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
