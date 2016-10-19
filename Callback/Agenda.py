import botogram
from datetime import datetime

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

    if query == "agenda":
        text = (
            "🗓<b>Agenda</b>"
            "\n\n<b>Seleziona un mese</b> in cui vuoi visualizzare il <b>planner programmazione</b>"
        )

        inline_keyboard = ('['
            '[{"text": "📅Settembre", "callback_data": "a@09"}, {"text": "📅Ottobre", "callback_data": "a@10"}],'
            '[{"text": "📅Novembre", "callback_data": "a@11"}, {"text": "📅Dicembre", "callback_data": "a@12"}],'
            '[{"text": "📅Gennaio", "callback_data": "a@01"}, {"text": "📅Febbraio", "callback_data": "a@02"}],'
            '[{"text": "📅Marzo", "callback_data": "a@03"}, {"text": "📅Aprile", "callback_data": "a@04"}],'
            '[{"text": "📅Maggio", "callback_data": "a@05"}, {"text": "📅Giugno", "callback_data": "a@06"}],'
            '[{"text": "🔙Torna indietro", "callback_data": "cancel"}]'
        ']')

        bot.api.call("editMessageText", {
            "chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML", "reply_markup":
            '{"inline_keyboard": '+inline_keyboard+'}'
        })

    if "a@" in query:
        query = query.split("@")
        month = int(query[1])

        if month < 9:
            year = 2017
            next_year = 2017
        else:
            year = 2016
            next_year = 2016

        if month == 12:
            next_month = 1
            next_year = 2017
        else:
            next_month = month + 1

        string = '{year}-{month}-01 00:00:00'.format(year=year, month=month)
        start = datetime.strptime(string, '%Y-%m-%d %H:%M:%S').timestamp()

        string = '{year}-{month}-01 00:00:00'.format(year=next_year, month=next_month)
        end = datetime.strptime(string, '%Y-%m-%d %H:%M:%S').timestamp()

        data = API.classeViva.agenda(API.classeViva.get_session_id(sender.id), start, end)

        if data['agenda'] == None:
            bot.api.call("answerCallbackQuery", {
                "callback_query_id": callback_id, "text": "❌Nessun evento in agenda per questo mese", "show_alert": True
            })
            return

        text = (
            "<b>Circolari, esercitazioni, compiti e appunti dal 1/{month}/{year} al 1/{next_month}/{next_year}</b>".format(month=month, year=year, next_month=next_month, next_year=next_year)
            )

        for dict in data['agenda']:
            start_time = datetime.strptime(dict['start'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m %H:%M')
            end_time = datetime.strptime(dict['end'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m %H:%M')
            text = text + (
            "\n\n🔹 <b>{title}</b>, <i>da {autore}</i>"
            "\nDal {start_time} al {end_time}".format(title=dict['title'], autore=dict['autore_desc'], start_time=start_time, end_time=end_time)
        )

        bot.api.call("editMessageText", {
            "chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML", "reply_markup":
                '{"inline_keyboard": [[{"text": "🔙Torna indietro", "callback_data": "agenda"}]]}'
        })
