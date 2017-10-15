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

import redis
import psycopg2

import config

r = redis.StrictRedis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    password=config.REDIS_PASSWORD
)
conn = psycopg2.connect(
    dbname=config.POSTGRESQL_DBNAME,
    host=config.POSTGRESQL_HOST,
    port=config.POSTGRESQL_PORT,
    user=config.POSTGRESQL_USER,
    password=config.POSTGRESQL_PASSWORD,
)
c = conn.cursor()


class User:
    """
    User base object
    """

    def __init__(self, user):
        """
        Create an user object
        :param user: Telegram's user object
        """
        self.id = user.id
        self.rhash = 'user:' + str(user.id)

        result = self.get_credentials()
        if not result:
            self.logged_in = False
            self.username = None
            self.password = None
        else:
            self.logged_in = True
            self.username = result['username']
            self.password = result['password']

        # Redis database
        if r.hget(self.rhash, 'id') != user.id:
            r.hset(self.rhash, 'id', user.id)
        if r.hget(self.rhash, 'username') != user.username:
            r.hset(self.rhash, 'username', user.username)
        r.hset(self.rhash, 'last_update', dt.now())
        if not self.state():
            r.hset(self.rhash, 'state', 'home')
        r.hset(self.rhash, 'active', True)

    def state(self, new_state=None):
        """
        Get current user state or set a new user state
        :param new_state: new state for the user
        :return: state
        """
        if not new_state:
            state = r.hget(self.rhash, 'state')
            if state:
                return state.decode('utf-8')
            return state

        r.hset(self.rhash, 'state', new_state)
        return True

    def set_credentials(self, username, password):
        """
        Set the user ClasseViva credentials
        :param username: ClasseViva username or email
        :param password: ClasseViva password
        """
        c.execute('INSERT INTO users VALUES(%s, %s, %s, %s) ON CONFLICT DO NOTHING',  # ¯\_(ツ)_/¯
                  (self.id, username, password, 'todo'))
        conn.commit()

        self.logged_in = True
        self.username = username
        self.password = password

    def get_credentials(self):
        """
        Get the user ClasseViva credentials
        :return: username, password
        """
        c.execute('SELECT username, password FROM users WHERE id=%s', (self.id,))
        row = c.fetchone()
        if not row:
            return False

        return {'username': row[0], 'password': row[1]}

    def set_redis(self, key, value):
        """
        Set a personal redis key
        :param key: key
        :param value: value
        """
        r.hset(self.rhash, key, value)

    def get_redis(self, key):
        """
        Get a redis key
        :param key: key
        """
        return r.hget(self.rhash, key)
