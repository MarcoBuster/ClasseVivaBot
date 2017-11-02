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


def process(query, data, message):
    u = User(query.sender)
    if not u.logged_in:
        query.notify('❌ Devi aver fatto il login per usare questa funzione!', alert=True)
        return

    session = u.login()

    result = session.grades()

    if not result.get('grades'):
        text = (
            "📕 <b>Voti dell'anno scolastico {schoolyear}</b>"
            "\n<i>Nessun voto da mostare 😔</i>"
            .format(schoolyear=utils.format_schoolyear())
        )
        keyboard = botogram.Buttons()
        keyboard[0].callback("🔙 Torna indietro", "home")
        message.edit(text, syntax="HTML", preview=False, attach=keyboard)
        return

    if not data:
        # Reorganize grades under subjects
        subjects = {}
        _subjects = []
        for grade in result['grades']:
            if grade['subjectId'] in _subjects:
                subjects[grade['subjectDesc']].append(grade)
            else:
                subjects = {**subjects, grade['subjectDesc']: [grade]}

            _subjects.append(grade['subjectId'])

        # Generate text message and inline keyboard
        text = (
            "📕 <b>Voti dell'anno scolastico {schoolyear}</b>"
            .format(schoolyear=utils.format_schoolyear())
        )
        keyboard = botogram.Buttons()
        index = 0
        for subject in subjects:
            summation = 0
            count = 0
            highest = 0
            lowest = 10000
            for grade in subjects[subject]:
                if grade.get('decimalValue') and grade['displayValue'] not in ["+", "-"]:
                    summation += (grade['decimalValue'] * grade['weightFactor'])
                    count += 1

                    if grade['decimalValue'] > highest:
                        highest = grade['decimalValue']

                    if grade['decimalValue'] < lowest:
                        lowest = grade['decimalValue']

            if count != 0:
                average = summation / count

                if average >= 8:
                    outcome = 'largamente positivo'
                elif 6 <= average < 8:
                    outcome = 'positivo'
                elif 5 <= average < 6:
                    outcome = 'negativo'
                else:
                    outcome = 'gravemente negativo'

            else:
                average = 'non disponibile'
                outcome = 'non disponibile'
                highest = 'non disponibile'
                lowest = 'non disponibile'

            text += (
                "\n\n➖ <b>{subject}</b>"
                "\n<b>Voti</b> (facenti media): {count}"
                "\n<b>Voto più alto</b>: {highest}"
                "\n<b>Voto più basso</b>: {lowest}"
                "\n<b>Media</b>: {average} {outcome}"
                .format(
                    subject=subject.capitalize(),
                    count=count,
                    highest=highest,
                    lowest=lowest,
                    average=round(average, 2) if type(average) in [int, float] else average,
                    outcome="- <i>" + format(outcome) + "</i>"
                )
            )
            keyboard[index].callback("🔹 {subject}".format(subject=subject.capitalize()),
                                     "grades", format(subjects[subject][0]['subjectId']))
            index += 1

        keyboard[index + 1].callback("🔙 Torna indietro", "home")
        message.edit(text, syntax="HTML", preview=False, attach=keyboard)

    else:
        subject_name = None
        for grade in result['grades']:
            if str(grade['subjectId']) != data:
                continue

            subject_name = grade['subjectDesc']

        text = (
            "👁‍🗨 <b>Voti dell'anno scolastico {schoolyear}</b> in {subject}"
            .format(schoolyear=utils.format_schoolyear(),
                    subject=subject_name.lower())
        )
        for grade in result['grades']:
            if str(grade['subjectId']) != data:
                continue

            if grade['color'] == 'green':
                e = '📗'
            elif grade['color'] == 'red':
                e = '📕'
            else:
                e = '📘'

            if grade['componentDesc'] == 'Scritto':
                grade_type = '✍️ scritto'
            elif grade['componentDesc'] == 'Orale':
                grade_type = '🗣 orale'
            elif grade['componentDesc'] == 'Pratico':
                grade_type = '🛠 pratico'
            else:
                grade_type = grade['componentDesc']

            text += (
                "\n🔹 {e}<b>{grade}</b> • {type} • {date} <i>({period})</i> <i>{comment}</i>"
                .format(e=e,
                        grade=grade['displayValue'],
                        date=utils.format_date(utils.from_iso_format(grade['evtDate'])).lower(),
                        period=format(grade['periodPos']) + ' ' + grade['periodDesc'].lower(),
                        type=grade_type,
                        comment='• ' + grade['notesForFamily'] if grade['notesForFamily'] else '')
            )

        keyboard = botogram.Buttons()
        keyboard[0].callback("🔙 Torna alla lista delle materie", "grades")
        message.edit(text, syntax="HTML", preview=False, attach=keyboard)
