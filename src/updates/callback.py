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
from datetime import timedelta as td
from calendar import monthcalendar

import config
from ..objects.user import User
from ..objects.utils import Utils


utils = Utils()


def process_home_callback(query, message):
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
    keyboard[1].callback('🗓 Agenda', 'agenda')
    keyboard[2].callback('🏃 Assenze', 'absences')
    keyboard[2].callback('🙋‍♂️ Lezioni', 'lessons_by_subject')
    keyboard[2].callback('🗂‍ Files', 'files')
    keyboard[3].callback('⚙️ Impostazioni', 'settings')
    keyboard[3].callback('ℹ️ Informazioni', 'infos')
    message.edit(text, syntax="HTML", preview=False, attach=keyboard)


def process_login_callback(query, message):
    u = User(query.sender)
    u.state('login_1')

    keyboard = botogram.Buttons()
    keyboard[0].callback("⏮ Riprova", "login")
    text = (
        "🔐 <b>Login nell'account di ClasseViva</b>"
        "\nInserisci l'username o la mail di ClasseViva / Spaggiari"
        "\n\n⚠️ <i>Questo bot è accessibile dai soli studenti, "
        "i dati di login di un docente potrebbero non funzionare</i>"
    )
    message.edit(text, syntax="HTML", preview=False)


def process_lessons_by_day_callback(query, data, message):
    u = User(query.sender)
    if not u.logged_in:
        return  # TODO: Error! You must logged in to use this bot

    session = u.login()

    day = utils.from_iso_format(data)
    result = session.lessons(day=day)

    if not result['lessons']:
        text = (
            "📆 <b>Registro di classe del giorno {day}</b>"
            "\n<i>Nessuna lezione da mostrare.</i>"
            .format(
                day=utils.format_date(day).lower()
            )
        )
    else:
        text = (
            "📆 <b>Registro della classe {schoolclass} del giorno {day}</b>"
            .format(
                schoolclass=result['lessons'][0]['classDesc'],
                day=utils.format_date(day).lower()
            )
        )

        index = 0
        processed = []
        to_sort = {}
        for lesson in result['lessons']:
            index += 1

            search_index = 0
            teachers = [lesson['authorName']]
            abort = False
            for search_lesson in result['lessons']:
                search_index += 1
                if search_index != index and search_lesson['evtHPos'] == lesson['evtHPos']:
                    teachers.append(search_lesson['authorName'])
                    abort = True

            if abort and lesson['evtHPos'] in processed:
                continue

            to_sort = {
                **to_sort,
                lesson['evtHPos']: "\n\n{n} <b>{subject}</b> con <i>{teachers}</i>{arg}".format(
                    n=utils.format_lesson_to_emoji(lesson),
                    subject=lesson['subjectDesc'].capitalize(),
                    teachers=utils.format_teachers_list(teachers),
                    arg=('\n' + lesson['lessonArg']) if lesson['lessonArg'] else ''
                )}
            processed.append(lesson['evtHPos'])

        for index in sorted(to_sort):
            text += to_sort[index]

    keyboard = botogram.Buttons()
    yesterday = day - td(days=1)
    keyboard[0].callback("⏪ {yesterday}".format(yesterday=utils.format_date(yesterday)), "lessons_by_day",
                         yesterday.isoformat())
    tomorrow = day + td(days=1)
    if not (tomorrow > dt.today()):
        keyboard[0].callback("⏩ {tomorrow}".format(tomorrow=utils.format_date(tomorrow)), "lessons_by_day",
                             tomorrow.isoformat())

    calendar = monthcalendar(year=day.year, month=day.month)
    keyboard[2].callback("🗓 Calendario di {month}".format(month=utils.format_month(day.month)), "null")

    if day.year == dt.today().year:
        if day.month != 1:
            previous_month = dt(year=day.year, month=day.month - 1, day=1)
            if previous_month >= config.SCHOOL_YEAR_BEGINNING:
                keyboard[1].callback(
                    "⏮ {previous_month}".format(previous_month=utils.format_month(previous_month.month)),
                    "lessons_by_day", previous_month.isoformat()
                )
    else:
        if day.month == 1:
            previous_month = dt(year=day.year - 1, month=12, day=1)
            if previous_month >= config.SCHOOL_YEAR_BEGINNING:
                keyboard[1].callback(
                    "⏮ {previous_month}".format(previous_month=utils.format_month(previous_month.month)),
                    "lessons_by_day", previous_month.isoformat())
        else:
            previous_month = dt(year=day.year, month=day.month - 1, day=1)
            if previous_month >= config.SCHOOL_YEAR_BEGINNING:
                keyboard[1].callback(
                    "⏮ {previous_month}".format(previous_month=utils.format_month(previous_month.month)),
                    "lessons_by_day", previous_month.isoformat()
                )

    if day.month != 12:
        next_month = dt(year=day.year, month=day.month + 1, day=1)
        if next_month < dt.today() and next_month <= config.SCHOOL_YEAR_END:
            keyboard[1].callback("⏭ {next_month}".format(next_month=utils.format_month(next_month.month)),
                                 "lessons_by_day", next_month.isoformat())
    else:
        next_month = dt(year=day.year + 1, month=1, day=1)
        if next_month < dt.today() and next_month <= config.SCHOOL_YEAR_END:
            keyboard[1].callback("⏭ {next_month}".format(next_month=utils.format_month(next_month.month)),
                                 "lessons_by_day", next_month.isoformat())

    keyboard_index = 3
    index = 0
    for week in calendar:
        if dt(year=day.year, month=day.month, day=1).weekday() == 6 and index == 0:
            index += 1
            continue

        for weekday in week:
            if weekday == 0:
                keyboard[keyboard_index].callback("×", "null")
                continue

            weekday_dt = dt(year=day.year, month=day.month, day=weekday)

            if weekday_dt > dt.today():
                if weekday_dt.weekday() != 6:
                    n = weekday_dt.weekday()
                    while n <= 6:
                        keyboard[keyboard_index].callback("×", "null")
                        n += 1
                break

            if weekday_dt.weekday() == 6:
                keyboard[keyboard_index].callback("×", "null")
                continue

            keyboard[keyboard_index].callback(weekday,
                                              "lessons_by_day",
                                              dt(year=day.year, month=day.month, day=weekday).isoformat())

        keyboard_index += 1

    keyboard[keyboard_index + 1].callback("🔙 Torna indietro", "home")
    message.edit(text, syntax="HTML", preview=False, attach=keyboard)


def process_grades_callback(query, data, message):
    u = User(query.sender)
    if not u.logged_in:
        return  # TODO: Error! You must logged in to use this bot

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
        subjects = []
        _subjects = []
        for grade in result['grades']:
            if grade['subjectId'] in _subjects:
                subjects[grade['subjectDesc']].append(grade)
            else:
                subjects.append({grade['subjectDesc']: [grade]})

            _subjects.append(grade['subjectId'])

        # Generate text message and inline keyboard
        text = (
            "📕 <b>Voti dell'anno scolastico {schoolyear}</b>"
            .format(schoolyear=utils.format_schoolyear())
        )
        keyboard = botogram.Buttons()
        index = 0
        for _subject in subjects:
            for subject in _subject:
                summation = 0
                count = 0
                highest = 0
                lowest = 10000
                for grade in _subject[subject]:
                    if grade.get('decimalValue') and grade['displayValue'] not in ["+", "-"]:
                        summation += (grade['decimalValue'] * grade['weightFactor'])
                        count += 1

                        if grade['decimalValue'] > highest:
                            highest = grade['displayValue']

                        if grade['decimalValue'] < lowest:
                            lowest = grade['displayValue']

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
                        average=round(average, 2), outcome="- <i>" + format(outcome) + "</i>"
                    )
                )
                keyboard[index].callback("🔹 {subject}".format(subject=subject.capitalize()),
                                         "grades", format(_subject[subject][0]['subjectId']))
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
