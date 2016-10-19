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

    if query == "notes":
        if API.classeViva.check_user(sender.id) == False:
            text = (
                "❌<b>Errore!</b> - <i>Login non effetuato</i>"
                "\nPer vedere i tuoi voti devi <b>eseguire il login</b> con il tuo account di <b>ClasseViva</b>"
            )
            bot.api.call("editMessageText", {
                "chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML", "reply_markup":
                     '{"inline_keyboard": [[{"text":"🔐Esegui il login", "callback_data": "login"}]]}'
            })
            return

        session_id = API.classeViva.get_session_id(sender.id)
        data = API.classeViva.notes(session_id)

        if data['notes'] == {} or data['notes'] == None:
            text = (
                "☺️<i>Non hai preso nessuna nota nel 2016!</i>"
            )
            bot.api.call("editMessageText", {
                "chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML", "reply_markup":
                    '{"inline_keyboard": [[{"text": "🔙Torna indietro", "callback_data": "cancel"}]]}'
            })
            return

        text = (
            "<b>Ecco le tue note e annotazioni che hai preso durante l'anno</b>"
        )

        for dict in data['notes']:
            text = text + (
                "\n\n🔹 <b>{type} del {date}</b> da {teacher}"
                "\n<i>{content}</i>".format(type=dict['type'], date=dict['date'], teacher=dict['teacher'], content=dict['content'])
            )

        bot.api.call("editMessageText", {
            "chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML", "reply_markup":
                '{"inline_keyboard": [[{"text": "🔙Torna indietro", "callback_data": "cancel"}]]}'
        })
