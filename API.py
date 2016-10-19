import sqlite3
import urllib.request
import json

from CONFIG import BASE_URL

conn = sqlite3.connect('ClasseViva.db')
c = conn.cursor()

class classeViva:
    '''ClasseViva mini-API wrapper'''
    def login(user_id, usercode, password):
        '''Login in ClasseViva'''
        info = BASE_URL+"/login?usercode={0}&password={1}".format(usercode, password) # TODO: use requests library
        response = urllib.request.urlopen(info)
        content = response.read()
        data = json.loads(content.decode("utf8"))

        if data['status'] != "OK":
            return False, False

        info = BASE_URL+"/{0}".format(data['sessionId'])
        response = urllib.request.urlopen(info)
        content = response.read()
        data2 = json.loads(content.decode("utf8"))

        session_id = data['sessionId']

        c.execute('''UPDATE users SET session_id=? WHERE user_id=?''', (session_id, user_id,))
        conn.commit()

        return data, data2

    def check_user(user_id):
        c.execute('''SELECT * FROM users WHERE user_id=?''', (user_id,))
        rows = c.fetchall()
        if not rows:
            return False

        for res in rows:
            session_id = res[3]

        if session_id == "None":
            return False
        else:
            return True

    def get_session_id(user_id):
        '''Get session_id'''
        c.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        rows = c.fetchall()
        conn.commit()

        for res in rows:
            usercode = res[1]
            password = res[2]
            session_id = res[3]

        info = BASE_URL+"/{0}".format(session_id) # TODO: use requests library
        response = urllib.request.urlopen(info)
        content = response.read()
        data = json.loads(content.decode("utf8"))

        if data['status'] != "OK":
            info = BASE_URL+"/login?usercode={0}&password={1}".format(usercode, password) # TODO: use requests library
            response = urllib.request.urlopen(info)
            content = response.read()
            data = json.loads(content.decode("utf8"))
            return data['sessionId']
        else:
            return session_id


    def grades(session_id):
        '''Search the grades'''
        info = BASE_URL+"/"+session_id+"/grades"
        response = urllib.request.urlopen(info)
        content = response.read()
        data = json.loads(content.decode("utf8"))
        if data['status'] == "OK":
            return data
        else:
            return False

    def agenda(session_id, start, end):
        '''Search agenda'''
        info = BASE_URL+"/{0}/agenda?start={1}&end={2}".format(session_id, start, end)
        response = urllib.request.urlopen(info)
        content = response.read()
        data = json.loads(content.decode("utf8"))
        if data['status'] == "OK":
            return data
        else:
            return False

    def files(session_id): # TODO
        '''Search files'''
        info = BASE_URL+"/"+session_id+"/files"
        response = urllib.request.urlopen(info)
        content = response.read()
        data = json.loads(content.decode("utf8"))
        if data['status'] == "OK":
            return data
        else:
            return False

    def notes(session_id):
        '''Search notes'''
        info = BASE_URL+"/"+session_id+"/notes"
        response = urllib.request.urlopen(info)
        content = response.read()
        data = json.loads(content.decode("utf8"))
        if data['status'] == "OK":
            return data
        else:
            return False

class db:
    '''Database management'''
    def createTables():
        '''Create all tables that I need!'''

        conn = sqlite3.connect('ClasseViva.db')
        c = conn.cursor()

        try:
            c.execute('''CREATE TABLE users (user_id INTEGER, usercode TEXT, password TEXT, session_id TEXT)''')
        except: #sqlite3 error
            pass

        try:
            c.execute('''CREATE TABLE state (user_id INTEGER, state INTEGER, temp INTEGER)''')
        except: #sqlite3 error
            pass

        conn.commit()

    def updateState(user_id, new_state, temp):
        c.execute('''DELETE FROM state WHERE user_id=?''',(user_id,))
        c.execute('''INSERT INTO state VALUES(?,?,?)''',(user_id, new_state, temp))
        conn.commit()

    def getState(user_id):
        c.execute('''SELECT * FROM state WHERE user_id=?''', (user_id,))
        items = c.fetchall()
        for res in items:
            return res[1], res[2]

    def resetState(user_id):
        updateState(user_id, "home", 0)

    def nullState(user_id):
        updateState(user_id, "nullstate", 0)
