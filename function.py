from datetime import datetime

import random

from config import MY_CHAT, TIME_DELTA

from session import SessionHelper
session = SessionHelper()

from db import DBHelper
db = DBHelper()

class Function:
    def get_top(self):
        items = db.get_items()
        messages = ""
        numeration = 1
        for row in items:
            messages += f"{str(numeration)}. {str(row[2])} – {str(row[3])} ответов\n"
            numeration+=1
        return messages

    def delta_time(self, time):
        time_delta = datetime.now() - datetime.strptime(str(time), '%Y-%b-%d %H:%M:%S')
        return time_delta.total_seconds()

    def time_checker(self, time):
        if(self.delta_time(time) < TIME_DELTA):
            return True
        else:
            return False

    def random_word(self):
        file = open("croco.txt", "r")
        lines = file.readlines()
        return lines[random.randint(0, 82492)].strip()

    def new_word(self):
        data = session.read_data()
        data['word'] = self.random_word()
        data['time'] = datetime.now().strftime('%Y-%b-%d %H:%M:%S')
        session.load_data(data)
        return data['word'] 


    def update_user(self, user, chat):
        data = session.read_data()
        data['id_user'] = user
        data['id_chat'] = MY_CHAT
        data['word'] = self.random_word()
        data['time'] = datetime.now().strftime('%Y-%b-%d %H:%M:%S')
        session.load_data(data)

    def db_update_user(self, user, name):
        data = db.find_user(user)
        if(data == None):
            db.new_user(user, name)
        else:
            db.update_user(user, name, data[1]+1)