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
from datetime import datetime as dt

from ...objects.user import User


def process(query, message):
    u = User(query.sender)
    u.state('home')

    name = u.get_redis('first_name').decode('utf-8') + ' ' + u.get_redis('last_name').decode('utf-8')
    text = (
        "📚 <b>Benvenuto in ClasseVivaBot!</b>"
        "\n✅ Sei loggato correttamente come <b>{name}</b>"
        "\n\n<i>Cosa vuoi fare? Clicca un pulsante sotto:</i>".format(name=name)
    )
    keyboard = botogram.Buttons()
    keyboard[0].callback('📆 Cosa si è fatto oggi a scuola?', 'lessons_by_day', dt.today().isoformat())
    keyboard[1].callback('📕 Voti', 'grades')
    keyboard[1].callback('✍️ Note', 'notes')
    keyboard[2].callback('🏃 Assenze', 'absences')
    keyboard[2].callback('🙋‍♂️ Lezioni', 'lessons_by_subject')
    keyboard[2].callback('🗓 Agenda', 'agenda')
    keyboard[3].callback('⚙️ Impostazioni', 'settings')
    keyboard[3].callback('ℹ️ Informazioni', 'infos')
    message.edit(text, syntax="HTML", preview=False, attach=keyboard)
