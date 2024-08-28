from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from gtts import gTTS
import os

# Füge deinen neuen Token hier ein
TELEGRAM_TOKEN = '7508808182:AAEl7yS5Me425PumMYYDzRi1KoFu3dsgVLM'

# Funktion für den Start-Befehl
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Willkommen! Du kannst wählen, ob ich in Text oder als Sprachnachricht antworte.')

# Funktion, die Textnachrichten verarbeitet
def text_response(update: Update, context: CallbackContext):
    user_message = update.message.text
    response_text = f'Du hast gesagt: {user_message}'  # Hier kannst du später eine NLP-Logik einbauen

    # Falls der User Sprachantworten möchte
    if context.user_data.get('voice_mode', False):
        tts = gTTS(text=response_text, lang='de')
        tts.save('response.mp3')
        update.message.reply_voice(voice=open('response.mp3', 'rb'))
        os.remove('response.mp3')  # Löscht die Datei nach dem Senden
    else:
        update.message.reply_text(response_text)

# Funktion zum Umschalten zwischen Text- und Sprachmodus
def toggle_voice_mode(update: Update, context: CallbackContext):
    current_mode = context.user_data.get('voice_mode', False)
    context.user_data['voice_mode'] = not current_mode
    mode = 'Sprachnachrichten' if context.user_data['voice_mode'] else 'Textnachrichten'
    update.message.reply_text(f'Antwortmodus geändert zu: {mode}')

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Befehle
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('voice_mode', toggle_voice_mode))

    # Textnachrichten
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_response))

    # Startet den Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
