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


from dateutil import parser


WEEKDAYS = {
    1: "Lunedì",
    2: "Martedì",
    3: "Mercoledì",
    4: "Giovedì",
    5: "Venerdì",
    6: "Sabato",
    7: "Domenica"
}
MONTHS = {
    1: "Gennaio",
    2: "Febbraio",
    3: "Marzo",
    4: "Aprile",
    5: "Maggio",
    6: "Giugno",
    7: "Luglio",
    8: "Agosto",
    9: "Settembre",
    10: "Ottobre",
    11: "Novembre",
    12: "Dicembre"
}
EMOJII_NUMBERS = {
    0: "0️⃣",
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
    10: "🔟",
}


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def format_date(date):
        weekday = WEEKDAYS[date.isoweekday()]
        month = MONTHS[date.month]
        return '{weekday} {day} {month}'.format(weekday=weekday,
                                                day=date.day,
                                                month=month)

    @staticmethod
    def format_month(month):
        return MONTHS[month]

    @staticmethod
    def format_lesson_to_emoji(lesson):
        return EMOJII_NUMBERS[lesson['evtHPos']]

    @staticmethod
    def format_teachers_list(teachers):
        index = 0
        result = ''
        for teacher in teachers:
            if index == 0:
                result += teacher.title()
            elif index == len(teachers) - 1:
                result += ' e ' + teacher.title()
            else:
                result += ', ' + teacher.title()
            index += 1

        return result

    @staticmethod
    def from_iso_format(iso):
        return parser.parse(iso)
