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
from ...objects.utils import Utils

utils = Utils()


def process(query, message):
    u = User(query.sender)
    if not u.logged_in:
        query.notify('❌ Devi aver fatto il login per usare questa funzione!', alert=True)
        return

    session = u.login()
    result = session.notes()

    name = u.get_redis('first_name').decode('utf-8') + ' ' + u.get_redis('last_name').decode('utf-8')

    text = "✍ <b>Note ed annotazioni dello studente {name}</b>".format(name=name)

    if not result['NTCL'] and not result['NTWN'] and not result['NTTE']:
        text += "\n<i>Nessuna nota o annotazione rilevata, studente modello! 😊</i>"
        keyboard = botogram.Buttons()
        keyboard[0].callback("🔙 Torna indietro", "home")
        message.edit(text, syntax="HTML", preview=False, attach=keyboard)
        return

    for disciplinary_note in result['NTCL']:
        if not disciplinary_note['readStatus']:
            disciplinary_note['evtText'] = "clicca sul tasto <i>\"Leggi\"</i> " \
                                           "dal <a href=\"https://web.spaggiari.eu\">registo web</a> " \
                                           "nella sezione <i>annotazioni</i> " \
                                           "per <b>leggere</b> questa nota disciplinare"

        text += (
            "\n• 🚫 <b>Nota disciplinare</b> dal prof <b>{author}</b> del <b>{date}</b>: {text}"
            .format(author=disciplinary_note['authorName'].title(),
                    date=disciplinary_note['evtDate'],
                    text=disciplinary_note['evtText'])
        )

    for warning in result['NTWN']:
        if not warning['readStatus']:
            warning['evtText'] = "clicca sul tasto <i>\"Leggi\"</i> " \
                                 "dal <a href=\"https://web.spaggiari.eu\">registo web</a> " \
                                 "nella sezione <i>annotazioni</i> " \
                                 "per <b>leggere</b> questo richiamo"

        text += (
            "\n• ⚠️ <b>Richiamo ({type})</b> dal prof <b>{author}</b> del <b>{date}</b>: {text}"
            .format(type=warning['warningType'].lower(),
                    author=warning['authorName'].title(),
                    date=warning['evtDate'],
                    text=warning['evtText']
                    )
        )

    for annotation in result['NTTE']:
        if not annotation['readStatus']:
            annotation['evtText'] = "clicca sul tasto <i>\"Leggi\"</i> " \
                                    "dal <a href=\"https://web.spaggiari.eu\">registo web</a> " \
                                    "nella sezione <i>annotazioni</i> " \
                                    "per <b>leggere</b> questo richiamo"
        text += (
            "\n• ℹ️ <b>Annotazione</b> dal prof <b>{author}</b> del <b>{date}</b>: {text}"
            .format(author=annotation['authorName'].title(),
                    date=annotation['evtDate'],
                    text=annotation['evtText'])
        )

    keyboard = botogram.Buttons()
    keyboard[0].callback("🔙 Torna indietro", "home")
    message.edit(text, syntax="HTML", preview=False, attach=keyboard)
