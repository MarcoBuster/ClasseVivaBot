import botogram

import API
import Bot

import sqlite3
conn = sqlite3.connect('ClasseViva.db')
c = conn.cursor()

def process(bot, chains, update):
    message = update.callback_query.message
    chat = message.chat
    query = update.callback_query.data
    callback_id = update.callback_query.id
    sender = update.callback_query.sender

    if query == "login":
        text = (
            "⚠️<b>ATTENZIONE! Questi dati vengono salvati nel database del bot (per ovvi motivi), ma non saranno MAI divulgati a terze parti</b>"
            "\n👀Per favore, leggi l\'<b>informativa del trattamento dei dati personali</b> raggiungibile a <a href=\"http://pastebin.com/A3VfzRYg\">questo indirizzo</a>."
            "\n❗️Premendo \"Continua\" <b>accetti quei termini</b>"
        )

        bot.api.call("editMessageText", {
            "chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML", "reply_markup":
                 '{"inline_keyboard": [[{"text":"✅Continua", "callback_data": "login2"}], [{"text":"❌Annulla", "callback_data": "cancel"}]]}'
        })

    if query == "login2":
        text = ("<b>🔐Login</b>\n✍️Per favore, inserisci il tuo <b>codice utente</b>"
            "\n\n💡<b>Suggerimento</b>: se hai associato un\'email a ClasseViva puoi usare quella!"
            )
        bot.api.call("editMessageText", {
            "chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML", "reply_markup":
                 '{"inline_keyboard": [[{"text":"❌Annulla", "callback_data": "cancel"}]]}'
        })

        API.db.updateState(sender.id, "login1", 0)
