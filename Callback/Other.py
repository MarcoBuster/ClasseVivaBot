import botogram
import time

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

    if query == "cancel":
        if API.classeViva.check_user(sender.id) == False:
            text = (
                '<b>Benvenuto in ClasseVivaBot!</b>\n'
                'Con questo bot puoi <b>controllare i voti</b>, <b>visualizzare l\'agenda</b>, i <b>files</b> e le <b>note</b> del registro elettronico '
                '<a href="web.spaggiari.eu">ClasseViva / Spaggiari</a>.'
                '\n\n<b>Per iniziare, esegui il login</b>'
            )
            bot.api.call("editMessageText", {"chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML", "reply_markup":
                            '{"inline_keyboard":['+
                            '[{"text":"🔐Esegui il login", "callback_data":"login"}]'+
                            ']}'
            })
            return

        text = (
            '<b>Benvenuto in ClasseVivaBot!</b>\n'
            'Hai già <b>eseguito il login</b>, cosa vuoi <b>visualizzare</b>?'
        )
        bot.api.call("editMessageText", {"chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML", "reply_markup":
                        '{"inline_keyboard":['+
                        '[{"text":"✍️Voti", "callback_data":"grades"}, {"text":"📜Agenda", "callback_data":"agenda"}, {"text":"📂Files", "callback_data":"files"}],'+
                        '[{"text":"👀Note e annotazioni", "callback_data":"notes"}, {"text": "⚙Altro", "callback_data":"other"}]'
                        ']}'
        })

    if query == "other":
        text = "<b>Cosa vuoi fare?</b>"

        bot.api.call("editMessageText",
        {"chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML",
            "reply_markup":
                '{"inline_keyboard": ['
                    '[{"text": "❌Cancella account", "callback_data": "destroy"}],'
                    '[{"text": "ℹAltre informazioni", "callback_data": "info"}],'
                    '[{"text": "🔙Torna indietro", "callback_data": "cancel"}]'
                ']}'
        })

    if query == "info":
        text = (
            "ℹ️ <b>Informazioni sul bot</b>"
            "\n 👤<b>Sviluppatore del Bot</b>: @MarcoBuster - [<a href=\"telegram.me/imieiprogetti\">Altri progetti</a>] • [<a href=\"telegram.me/MarcoBusterBlog\">Blog</a>] • [<a href=\"www.Github.com/MarcoBuster\">Github</a>]"
            "\n 👤<b>Sviluppatore API</b>: @ALCC01 - [<a href=\"http://www.albertocoscia.me\">Sito web</a>] • [<a href=\"https://www.Github.com/ALCC01\">Github</a>]"
            "\n 📖<b>Codice sorgente</b>: [<a href=\"https://www.Github.com/MarcoBuster/ClasseVivaBot\">Github</a>]"
            "\n 👀<b>Licenza</b>: <a href=\"https://opensource.org/licenses/MIT\">MIT</a>"
        )
        bot.api.call("editMessageText", {
            "chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML", "reply_markup":
            '{"inline_keyboard": [[{"text": "🔙Torna indietro", "callback_data": "cancel"}]]}'
        })

    if query == "destroy":
        text = (
            "❌<b>Cancellazione account</b>"
            "\nCancellando l'account <b>tutti i dati di login</b> verranno <b>eliminati</b> dal <b>database</b> del bot"
            "\nUna volta fatto, dovrai <b>eseguire</b> nuovamente il <b>login</b>"
            "\n\n<b>Vuoi davvero continuare?</b>"
        )

        bot.api.call("editMessageText",
        {"chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML",
            "reply_markup":
                '{"inline_keyboard": ['
                    '[{"text": "❌Continua", "callback_data": "destroy2"}],'
                    '[{"text": "✋Annulla", "callback_data": "settings"}]'
                ']}'
        })

    if query == "destroy2":
        message.edit(
            "<b>Sto eliminando l'account e tutti i dati</b>, <code>DELETE FROM users WHERE user_id={}</code>".format(str(sender.id))
        )
        time.sleep(3)
        c.execute('DELETE FROM users WHERE user_id=?',(sender.id,))
        conn.commit()
        message.edit(
            "<b>Fatto!</b>\nEsegui il comando /start per iniziare"
        )
