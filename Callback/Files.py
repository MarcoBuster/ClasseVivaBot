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

    if query == "files":
        bot.api.call("answerCallbackQuery", {
            "callback_query_id": callback_id, "text": "⚡️Funzione in sviluppo!", "show_alert": True
        })
