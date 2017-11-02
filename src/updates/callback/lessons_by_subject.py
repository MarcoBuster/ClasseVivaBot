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


import config

import botogram

from ...objects.user import User


def process(query, data, message):
    u = User(query.sender)
    if not u.logged_in:
        query.notify('❌ Devi aver fatto il login per usare questa funzione!', alert=True)
        return

    session = u.login()

    if not data:
        result = session.subjects()

        text = "🙋 <b>Elenco delle materie</b>\n" \
               "<i>Seleziona una materia per visualizzare gli argomenti fatti giorno per giorno</i>"
        keyboard = botogram.Buttons()
        index = 0
        for subject in result['subjects']:
            keyboard[index].callback(
                "🔷 {subject}".format(subject=subject['description'].capitalize()),
                "lessons_by_subject",
                str(subject['id'])
            )
            text += (
                "\n\n<b>🔹 {subject}</b>".format(subject=subject['description'].capitalize())
            )
            for teacher in subject['teachers']:
                text += (
                    "\n• <i>{teacher}</i>".format(teacher=teacher['teacherName'].title())
                )
            index += 1

        keyboard[index].callback("🔙 Torna indietro", "home")

        message.edit(text, syntax=None, preview=False, attach=keyboard)
        return

    result = session.lessons(begin=config.SCHOOL_YEAR_BEGINNING, end=config.SCHOOL_YEAR_END)

    lessons = []
    previous_arg = ""
    for lesson in result['lessons']:
        if lesson['subjectId'] != int(data):
            continue

        if previous_arg == lesson['lessonArg']:
            previous_arg = lesson['lessonArg']
            continue

        lessons.append(lesson)
        previous_arg = lesson['lessonArg']

    if not lessons:
        text = "🙋 <i>Nessuna lezione trovata per questa materia</i>"
        keyboard = botogram.Buttons()
        keyboard[0].callback("🔙 Torna indietro", "lessons_by_subject")
        message.edit(text, syntax=None, preview=False, attach=keyboard)
        return

    text = "🙋 <b>Lezioni di {subject}</b>"
    first = True
    for lesson in lessons:
        if first:
            text = text.format(subject=lesson['subjectDesc'].capitalize())
            first = False

        text += (
            "\n• <b>{date}</b> - <i>{type}</i> - {arg}"
            .format(date=lesson['evtDate'], type=lesson['lessonType'], arg=lesson['lessonArg'])
        )

    keyboard = botogram.Buttons()
    keyboard[0].callback("🔙 Torna indietro", "lessons_by_subject")
    message.edit(text, syntax=None, preview=False, attach=keyboard)
