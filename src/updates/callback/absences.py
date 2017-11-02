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
        return  # TODO: Error! You must logged in to use this bot

    session = u.login()
    result = session.absences()

    name = u.get_redis('first_name').decode('utf-8') + ' ' + u.get_redis('last_name').decode('utf-8')

    if not result.get('events'):
        text = (
            "🏃 <b>Assenze e ritardi</b> dello studente <b>{name}</b>"
            "\n<i>Nessuna assenza o ritardo da mostrare. Studente modello! 😊</i>"
            .format(name=name)
        )
        keyboard = botogram.Buttons()
        keyboard[0].callback("🔙 Torna indietro", "home")
        message.edit(text, syntax="HTML", preview=False, attach=keyboard)
        return

    text = (
        "🏃 <b>Assenze e ritardi</b> dello studente <b>{name}</b>".format(name=name)
    )
    absences = ""
    delays = ""
    anticipated_relases = ""
    not_justified = 0
    for event in result['events']:
        if not event['isJustified']:
            not_justified += 1

        if event['evtCode'] == 'ABA0':
            if not absences:
                absences = "\n➖➖ <b>Assenze</b>"

            absences += (
                "\n• <b>{date}</b>{reason}{e}"
                .format(
                    e=" ⚠️ da giustificare!" if not event['isJustified'] else "",
                    date=utils.format_date(utils.from_iso_format(event['evtDate'])),
                    reason=" per <i>{reason}</i>".format(reason=event['justifReasonDesc']).lower()
                    if event['isJustified'] else ""
                )
            )

        elif event['evtCode'] == 'ABR0':
            if not delays:
                delays = "\n➖➖ <b>Ritardi</b>"

            delays += (
                "\n• <b>{date}</b> in {hour}a ora {reason}{e}"
                .format(
                    e=" ⚠️ da giustificare!" if not event['isJustified'] else "",
                    date=utils.format_date(utils.from_iso_format(event['evtDate'])),
                    reason="per <i>{reason}</i>".format(reason=event['justifReasonDesc']).lower()
                    if event['isJustified'] else "",
                    hour=event['evtHPos'] + event['evtValue'] - 1  # Beacuse arrays here starts at 1, damn!
                )
            )

        elif event['evtCode'] == 'ABU0':
            if not anticipated_relases:
                anticipated_relases = "\n➖➖ <b>Uscite anticipate</b>"

            anticipated_relases += (
                "\n• <b>{date}</b> in {hour}a ora {reason}{e}"
                .format(
                    e=" ⚠️ da giustificare!" if not event['isJustified'] else "",
                    date=utils.format_date(utils.from_iso_format(event['evtDate'])),
                    reason="per <i>{reason}</i>".format(reason=event['justifReasonDesc']).lower()
                    if event['isJustified'] else "",
                    hour=event['evtHPos'] + event['evtValue'] - 1  # Beacuse arrays here starts at 1, damn!
                )
            )

    text += (
        ("\n<b>‼️ {not_justified} da giustificare</b>".format(not_justified=not_justified)
            if not_justified != 0 else "") + absences + delays + anticipated_relases
    )
    keyboard = botogram.Buttons()
    keyboard[0].callback("🔙 Torna indietro", "home")
    message.edit(text, syntax="HTML", preview=False, attach=keyboard)
