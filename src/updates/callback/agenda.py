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


from datetime import datetime as dt

import botogram

from ...objects.user import User
from ...objects.utils import Utils
import config

utils = Utils()


def process(query, data, message):
    u = User(query.sender)
    if not u.logged_in:
        return  # TODO: Error! You must logged in to use this bot

    session = u.login()
    if not data:
        today = dt.today()
    else:
        today = utils.from_iso_format(data)
    result = session.agenda(begin=dt(year=today.year, month=today.month, day=1),
                            end=dt(year=today.year + (1 if today.month == 12 else 0),
                                   month=today.month + (1 if today.month != 12 else -11),
                                   day=1))

    if not result.get('agenda'):
        text = (
            "🗓 <b>Agenda</b> di classe"
            "\n<i>Nessun evento in agenda.</i>"
        )
        keyboard = botogram.Buttons()
        keyboard[0].callback("🔙 Torna indietro", "home")
        message.edit(text, syntax="HTML", preview=False, attach=keyboard)
        return

    agnt = {}
    aghw = {}
    for event in result['agenda']:
        if event['evtCode'] == "AGNT":
            agnt = {
                **agnt,
                event['evtDatetimeBegin']: (
                    "\n\n📃 <i>{date}</i> • <b>{author}</b>\n{text}"
                    .format(
                        author=event['authorName'].title(),
                        date=utils.format_date(utils.from_iso_format(
                            event['evtDatetimeBegin'])).capitalize(),
                        text=event['notes']
                    )
                )
            }

        elif event['evtCode'] == "AGHW":
            aghw = {
                **aghw,
                event['evtDatetimeBegin']: (
                    "\n\n📚 <i>{date}</i> • <b>{author}</b> / {subject}\n{text}"
                    .format(
                        author=event['authorName'].title(),
                        date=utils.format_date(utils.from_iso_format(
                            event['evtDatetimeBegin'])).capitalize(),
                        subject=event['subjectDesc'].capitalize(),
                        text=event['notes']
                    )
                )
            }

    text = (
        "🗓 <b>Agenda</b> della classe {schoolclass}"
        .format(schoolclass=result['agenda'][0]['classDesc'])
    )
    for i in sorted({**aghw, **agnt}, reverse=True):
        text += aghw.get(i, '')
        text += agnt.get(i, '')

    keyboard = botogram.Buttons()
    keyboard[1].callback("🔙 Torna indietro", "home")

    if today.year == dt.today().year:
        if today.month != 1:
            previous_month = dt(year=today.year, month=today.month - 1, day=1)
            if previous_month >= config.SCHOOL_YEAR_BEGINNING:
                keyboard[0].callback(
                    "⏮ {previous_month}".format(previous_month=utils.format_month(previous_month.month)),
                    "agenda", previous_month.isoformat()
                )
    else:
        if today.month == 1:
            previous_month = dt(year=today.year - 1, month=12, day=1)
            if previous_month >= config.SCHOOL_YEAR_BEGINNING:
                keyboard[0].callback(
                    "⏮ {previous_month}".format(previous_month=utils.format_month(previous_month.month)),
                    "agenda", previous_month.isoformat())
        else:
            previous_month = dt(year=today.year, month=today.month - 1, day=1)
            if previous_month >= config.SCHOOL_YEAR_BEGINNING:
                keyboard[0].callback(
                    "⏮ {previous_month}".format(previous_month=utils.format_month(previous_month.month)),
                    "agenda", previous_month.isoformat()
                )

    if today.month != 12:
        next_month = dt(year=today.year, month=today.month + 1, day=1)
        if next_month < dt.today() and next_month <= config.SCHOOL_YEAR_END:
            keyboard[0].callback("⏭ {next_month}".format(next_month=utils.format_month(next_month.month)),
                                 "agenda", next_month.isoformat())
    else:
        next_month = dt(year=today.year + 1, month=1, day=1)
        if next_month < dt.today() and next_month <= config.SCHOOL_YEAR_END:
            keyboard[0].callback("⏭ {next_month}".format(next_month=utils.format_month(next_month.month)),
                                 "agenda", next_month.isoformat())

    message.edit(text, syntax="HTML", preview=False, attach=keyboard)
