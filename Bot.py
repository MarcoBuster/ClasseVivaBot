import API

from Callback import Login, Grades, Agenda, Files, Other, Notes
from CONFIG import TOKEN, BASE_URL

import botogram.objects.base
class CallbackQuery(botogram.objects.base.BaseObject):
    required = {
        "id": str,
        "from": botogram.User,
        "data": str,
    }
    optional = {
        "inline_message_id": str,
        "message": botogram.Message,
    }
    replace_keys = {
        "from": "sender"
    }
botogram.Update.optional["callback_query"] = CallbackQuery

import botogram
bot = botogram.create(TOKEN)

import sqlite3
conn = sqlite3.connect('ClasseViva.db')
c = conn.cursor()

API.db.createTables()

@bot.command("start")
def welcome(chat, message, args):
    if args != None:
        pass

    if API.classeViva.check_user(message.sender.id) == False:
        text = (
            '<b>Benvenuto in ClasseVivaBot!</b>\n'
            'Con questo bot puoi <b>controllare i voti</b>, <b>visualizzare l\'agenda</b>, i <b>files</b> e le <b>note</b> del registro elettronico '
            '<a href="web.spaggiari.eu">ClasseViva / Spaggiari</a>.'
            '\n\n<b>Per iniziare, esegui il login</b>'
        )
        bot.api.call("sendMessage", {"chat_id": chat.id, "text": text, "parse_mode": "HTML", "reply_markup":
                        '{"inline_keyboard":['+
                        '[{"text":"🔐Esegui il login", "callback_data":"login"}]'+
                        ']}'
        })
        return

    text = (
        '<b>Benvenuto in ClasseVivaBot!</b>\n'
        'Hai già <b>eseguito il login</b>, cosa vuoi <b>visualizzare</b>?'
    )
    bot.api.call("sendMessage", {"chat_id": chat.id, "text": text, "parse_mode": "HTML", "reply_markup":
                    '{"inline_keyboard":['+
                    '[{"text":"✍️Voti", "callback_data":"grades"}, {"text":"📜Agenda", "callback_data":"agenda"}, {"text":"📂Files", "callback_data":"files"}],'+
                    '[{"text":"👀Note e annotazioni", "callback_data":"notes"}, {"text": "⚙Altro", "callback_data":"other"}]'
                    ']}'
    })

def process_callback(bot, chains, update):
    Login.process(bot, chains, update)
    Files.process(bot, chains, update)
    Grades.process(bot, chains, update)
    Agenda.process(bot, chains, update)
    Other.process(bot, chains, update)
    Notes.process(bot, chains, update)
bot.register_update_processor("callback_query", process_callback)

@bot.command("post")
def post(chat, message, args):
    """Post a message to all users"""
    if message.sender.id != 26170256: #Only admin command
        message.reply("This command it's only for the admin of the bot")
        return

    c.execute('''SELECT * FROM users''')
    users_list = c.fetchall()

    message = " ".join(message.text.split(" ", 1)[1:])

    for res in users_list:
        try:
            bot.chat(res[0]).send(message)
            chat.send("Post sent to "+str(res[0]))
        except botogram.api.ChatUnavailableError:
            c.execute('DELETE FROM users WHERE user_id={}'.format(res[0]))
            chat.send("The user "+str(res[0])+" has blocked your bot, so I removed him from the database")
            conn.commit()
        except Exception as e:
            chat.send("*Unknow error :(*\n"+str(e))

    chat.send("<b>Done!</b>\nThe message has been delivered to all users") #Yeah
    conn.commit()

@bot.process_message
def login1(chat, message): #CHIEDE NOME RICEVE USERNAME
    state, temp = API.db.getState(chat.id)
    if state != "login1":
        return

    if message.text == None:
        return

    usercode = message.text
    s_id = message.sender.id

    c.execute('''DELETE FROM users WHERE user_id=?''',(s_id,))
    c.execute('''INSERT INTO users VALUES(?,?,?,?)''',(s_id, "None", "None", "None"))
    c.execute('''UPDATE users SET usercode=? WHERE user_id=?''',(usercode, s_id,))
    conn.commit()

    testo = ("<b>🔐Login</b>\n✍️Scrivi ora la tua <b>password personale</b>"
            "\n\n💡<b>Suggerimento</b>: elimina il messaggio con la password dopo averlo inviato!"
    )
    bot.api.call("sendMessage", {"chat_id":chat.id, "text":testo, "parse_mode":"HTML",
            "reply_markup":
                '{"inline_keyboard":[[{"text":"❌Annulla","callback_data":"cancel"}]]}'
    })

    API.db.updateState(chat.id, "login3", 0)

@bot.process_message
def login2(chat, message):
    state, temp = API.db.getState(chat.id)
    if state != "login3":
        return

    if temp != 1:
        API.db.updateState(chat.id, "login3", 1)
        return

    if message.text == None:
        return

    password = message.text
    s_id = message.sender.id

    c.execute('''UPDATE users SET password=? WHERE user_id=?''', (password, s_id))

    c.execute('''SELECT * FROM users WHERE user_id=?''', (s_id,))
    rows = c.fetchall()
    conn.commit()

    for res in rows:
        usercode = res[1]
        password = res[2]

    try:
        data, data2 = API.classeViva.login(s_id, usercode, password)
    except Exception as e:
        data = False

    if data == False:
        chat.send("⛔️<b>Login fallito</b>"
            "\n<i>Username o password errati</i>"
            "\n\n💡<b>Suggerimento</b>: Se stai utilizzando la <b>mail</b>, prova ad utilizzare il <b>codice utente</b>"
            "\n💡<b>Suggerimento</b>: Con la nuova versione di <b>ClasseViva</b>, per usare questo bot bisogna aver fatto <b>almeno una volta</b> <i>(e con successo)</i> il <b>login</b> nel sito web.spaggiari.eu"
            , preview=False
        )
        return

    text = ("✅<b>Login effettuato con successo!</b>"
        "\n\n📚<b>Profilo utente</b>"
        "\n👤<b>Nome</b>: {0}"
        "\n🏫<b>Scuola</b>: {1}".format(data2['profile']['name'], data2['profile']['school']))

    bot.api.call("sendMessage", {
        "chat_id": chat.id, "text": text, "parse_mode": "HTML", "reply_markup":
        '{"inline_keyboard": ['
                '[{"text":"✍️Voti", "callback_data":"grades"}, {"text":"📜Agenda", "callback_data":"agenda"}, {"text":"📂Files", "callback_data":"files"}],'+
                '[{"text":"👀Note e annotazioni", "callback_data":"notes"}, {"text": "⚙Altro", "callback_data":"other"}]'
            ']}'
    })

    API.db.updateState(chat.id, "home", 0)
if __name__ == "__main__":
    bot.run()
