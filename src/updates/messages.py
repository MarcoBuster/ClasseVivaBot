# This file is a part of ClasseVivaBot, a Telegram bot for Classe Viva electronic register
#
# Copyright (c) 2016-2017 The ClasseVivaBot Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from ..objects.user import User

from classeviva.errors import AuthenticationFailedError
import classeviva
import botogram


def process_message(message):
    u = User(message.sender)

    if not message.text:
        return

    if u.state() == 'login_1':
        u.set_redis('login_username', message.text)

        keyboard = botogram.Buttons()
        keyboard[0].callback("⏮ Riprova", "login")
        text = (
            "🔐 <b>Login nell'account Classe Viva</b>"
            "\nOra inserisci la password del tuo account Classe Viva / Spaggiari"
            "\n\n💡 <b>Suggerimento</b>: "
            "<i>Per preservare la tua privacy, elimina il messaggio contenente la password dopo averlo inviato!</i>"
        )
        message.reply(text, syntax="HTML", preview=False, attach=keyboard)
        u.state('login_2')
        return

    elif u.state() == 'login_2':
        username = u.get_redis('login_username').decode('utf-8')
        password = message.text

        s = classeviva.Session()
        try:
            result = s.login(username, password)
        except AuthenticationFailedError:
            keyboard = botogram.Buttons()
            keyboard[0].callback("⏮ Riprova", "login")

            text = (
                "⛔️ <b>Credenziali invalide</b>"
                "\nLe credenziali inserite non sono riconosciute dal sistema Classe Viva come valide. Riprovare."
                "\n\n💡 <b>Suggerimenti</b>: "
                "\n1️⃣ Controllare le credenziali inserite, specialmente la distinazione fra "
                "<b>maiuscole</b> e <b>minuscole</b>"
                "\n2️⃣ Se si è sicuri che la password sia corretta, provare ad eseguire il login dal "
                "<a href=\"https://web.spaggiari.eu\">sito di Classe Viva</a>"
                "\n3️⃣ Se il sito di Classe Viva riconosce le credenziali, provare a mettere il codice utente "
                "al posto dell'indirizzo e-mail"
                "\n4️⃣ <b>Reimpostare la password</b> dal sito di Classe Viva"
                "\n5️⃣ Se, <b>dopo aver provato tutte le opzioni sopra</b>, continua a non funzionare, "
                "contattare lo sviluppatore del bot <a href=\"https://t.me/MarcoBuster\">in chat privata</a>"
            )
            message.reply(text, syntax="HTML", preview=False, attach=keyboard)
            return

        text = (
            "✅ <b>Login completato con successo</b>"
            "\n\n<i>Cosa vuoi fare? Clicca un pulsante sotto:</i>"
        )
        keyboard = botogram.Buttons()
        keyboard[0].callback('📆 Cosa si è fatto oggi a scuola?', 'test')
        keyboard[1].callback('📕 Voti', 'grades')
        keyboard[1].callback('✍️ Note', 'notes')
        keyboard[1].callback('🗓 Agenda', 'agenda')
        keyboard[2].callback('🏃 Assenze', 'absences')
        keyboard[2].callback('🙋‍♂️ Lezioni', 'lessons')
        keyboard[2].callback('🗂‍ Files', 'files')
        keyboard[3].callback('⚙️ Impostazioni', 'settings')
        keyboard[3].callback('ℹ️ Informazioni', 'infos')
        message.reply(text, syntax="HTML", preview=False, attach=keyboard)

        u.set_credentials(username, password)
        u.set_redis('first_name', result['first_name'])
        u.set_redis('last_name', result['last_name'])
