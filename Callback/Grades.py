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

    if query == "grades":
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
        data = API.classeViva.grades(session_id)

        inline_keyboard = '['
        numero = 0
        for dict in data['grades']:
            numero = numero + 1
            inline_keyboard = inline_keyboard + '[{"text":"'+dict.capitalize()+'", "callback_data":"m@'+dict+'"}],'
        inline_keyboard = inline_keyboard + '[{"text": "🔙Torna indietro", "callback_data": "cancel"}]]'

        if numero == 0:
            text = ("<b>Ecco la lista delle materie in cui hai voti</b>"
                "\n<i>Non hai ancora preso nessun voto nel 2016!</i>"
            )

        text = ("<b>Ecco la lista delle materie in cui hai voti</b>"
                "\n<i>Seleziona una materia per visualizzare i voti</i>"
                )

        bot.api.call("editMessageText", {
            "chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML", "reply_markup":
                         '{"inline_keyboard": '+inline_keyboard+'}'
        })

    if query.find('m') > -1:
        query = query.split('@')
        subject = query[1]

        session_id = API.classeViva.get_session_id(sender.id)
        data = API.classeViva.grades(session_id)

        text = "<b>I tuoi voti in "+subject.capitalize()+"</b>"

        for dict in data['grades'][subject]:
            text = text + (
                    "\n🔹 <b>[{type}]</b> <b>{grade}</b> ({date})".format(grade=dict['grade'], type=dict['type'], date=dict['date'])
            )

        bot.api.call("editMessageText", {
            "chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML", "reply_markup":
                                 '{"inline_keyboard": [[{"text":"🔙Torna alla lista delle materie", "callback_data": "grades"}]]}'
        })
