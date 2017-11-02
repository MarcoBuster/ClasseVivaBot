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


def process(message):
    keyboard = botogram.Buttons()
    text = (
        "ℹ️ <b>Informazioni sul bot</b>"
        "\n👤 <b>Sviluppatore</b>: <a href=\"t.me/MarcoBuster\">@MarcoBuster</a> "
        "(guarda i miei <a href=\"t.me/imieiprogetti\">altri progetti</a>)"
        "\n👥 <b>Gruppo di supporto</b>: <a href=\"t.me/MarcoBuster\">entra e chiedi</a>"
        "\n💻 <b>Codice sorgente</b>: <a href=\"https://github.com/MarcoBuster/ClasseVivaBot\">GitHub</a> (Python/MIT)"
        "\n📃 <b>Informativa privacy</b>: "
        "<a href=\"https://marcoaceti.it/classevivabot/informativa_privacy.html\">link</a>"
        "\n💎 <b>Dona</b> quanto vuoi per tenere il progetto online: "
        "<a href=\"https://paypal.me/marcoaceti\">con PayPal</a>"
        "\n#️⃣ <b>Versione</b>: <code>4.0 BETA</code>"
    )
    keyboard[1].url("👤 Scrivi allo sviluppatore", "https://t.me/MarcoBuster")
    keyboard[1].url("👥 Gruppo di supporto", "https://t.me/MarcoBusterGroup")
    keyboard[2].url("💻 Codice sorgente", "https://github.com/MarcoBuster/ClasseVivaBot")
    keyboard[2].url("📃 Informativa privacy", "https://marcoaceti.it/classevivabot/informativa_privacy.html")
    keyboard[2].url("💎 Dona", "https://paypal.me/marcoaceti")
    keyboard[3].callback("🔙 Torna indietro", "home")
    message.edit(text, syntax="HTML", preview=False, attach=keyboard)
