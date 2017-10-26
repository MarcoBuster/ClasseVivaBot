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


import botogram

from ...objects.user import User


def process(query, data, message):
    u = User(query.sender)
    if not data:
        name = u.get_redis('first_name').decode('utf-8') + ' ' + u.get_redis('last_name').decode('utf-8')
        text = (
            "⚙️ <b>Impostazioni di ClasseVivaBot</b>"
            "\n➖➖ <b>Informazioni account</b>"
            "\n✅ <b>Login effettuato con successo</b>"
            "\n👤 <b>Nome e cognome</b>: {name}"
            "\n\n🚪 <b>Esegui il logout</b> ed <b>elimina definitivamente</b> TUTTI i dati dal database."
            "\n🔌 <b>Connetti ad un gruppo classe</b> per condividere l'account (in <i>modalità speciale</i>, "
            "ovvero senza password, voti, note ed assenze) con il gruppo classe per un'esperienza unica."
            .format(name=name)
        )
        keyboard = botogram.Buttons()
        keyboard[0].callback("🚪 Esegui il logout", "settings", "logout")
        keyboard[1].callback("🔌 Connetti ad un gruppo classe", "settings", "connect")
        keyboard[2].callback("🔙 Torna indietro", "home")
        message.edit(text, syntax="HTML", preview=False, attach=keyboard)
        return

    elif data == 'logout':
        text = (
            "🚪 <b>Esegui il logout</b>"
            "\nEseguendo il <b>logout</b> elimini definitivamente tutti i dati dal <b>database</b>: "
            "per continuare ad usare il bot dovrai <b>rifare il login</b>."
        )
        keyboard = botogram.Buttons()
        keyboard[0].callback("❌ Annulla", "settings")
        keyboard[1].callback("⭕️ Esegui il logout", "settings", "logout_confirm")
        message.edit(text, syntax="HTML", preview=False, attach=keyboard)

    elif data == 'logout_confirm':
        u.delete_credentials()
        text = (
            "✳️ <b>Logout effettuato con successo</b>"
            "\nSe vuoi a continuare ad usare il <b>bot</b>, manda il comando /start ed <b>riesegui il login</b>."
        )
        message.edit(text, syntax="HTML", preview=False)
