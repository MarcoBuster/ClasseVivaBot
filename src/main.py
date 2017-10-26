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

from .updates import commands, messages
from .updates import callback
import config


bot = botogram.create(config.BOT_TOKEN)


@bot.command("start")
def start(message):
    commands.process_start_command(message)


@bot.process_message
def process_message(message):
    messages.process_message(message)


@bot.callback("home")
def process_home_callback(query, message):
    callback.home.process(query, message)


@bot.callback("login")
def login_callback(query, message):
    callback.login.process(query, message)


@bot.callback("infos")
def infos_callback(message):
    callback.infos.process(message)


@bot.callback("settings")
def settings_callback(query, data, message):
    callback.settings.process(query, data, message)


@bot.callback("lessons_by_day")
def lessons_by_day_callback(query, data, message):
    callback.lessons_by_day.process(query, data, message)


@bot.callback("grades")
def grades(query, data, message):
    callback.grades.process(query, data, message)


@bot.callback("agenda")
def agenda(query, data, message):
    callback.agenda.process(query, data, message)


@bot.callback("absences")
def absences(query, message):
    callback.absences.process(query, message)


@bot.callback("null")
def null_callback(query):
    query.notify("¯\_(ツ)_/¯", alert=False)
