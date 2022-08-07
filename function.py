import random, os
from datetime import datetime
from dotenv import load_dotenv

#import .env file
load_dotenv()
MY_CHAT = int(os.getenv('MY_CHAT'))
TIME_DELTA = os.getenv('TIME_DELTA')

#import SessionHelper
from session import SessionHelper
session = SessionHelper()

#import DBHelper
from db import DBHelper
db = DBHelper()

#new Function
class Function:
    def get_top(self):
        #Rating user from database
        items = db.get_items()
        messages = ""
        numeration = 1
        for row in items:
            messages += f"{str(numeration)}. {str(row[2])} – {str(row[3])} ответов\n"
            numeration+=1
        return messages

    def delta_time(self, time):
        #Get seconds between now and time
        time_delta = datetime.now() - datetime.strptime(str(time), '%Y-%b-%d %H:%M:%S')
        return time_delta.total_seconds()

    def time_checker(self, time):
        #check if the game can be started
        if(self.delta_time(time) < TIME_DELTA):
            return True
        else:
            return False

    def random_word(self):
        #new random word from database
        file = open("croco.txt", "r")
        lines = file.readlines()
        return lines[random.randint(0, 82492)].strip()

    def new_word(self):
        #Load new user to session
        data = session.read_data()
        data['word'] = self.random_word()
        data['time'] = datetime.now().strftime('%Y-%b-%d %H:%M:%S')
        session.load_data(data)
        return data['word'] 


    def update_user(self, user, chat):
        #Load new word to session
        data = session.read_data()
        data['id_user'] = user
        data['id_chat'] = MY_CHAT
        data['word'] = self.random_word()
        data['time'] = datetime.now().strftime('%Y-%b-%d %H:%M:%S')
        session.load_data(data)

    def db_update_user(self, user, name):
        #Update user to database with +1
        data = db.find_user(user)
        if(data == None):
            db.new_user(user, name, 0)
        else:
            db.update_user(user, name, data[1]+1)

    def db_user_downgrade(self, user, name):
        #Update user to database with -1
        data = db.find_user(user)
        if(data == None):
            db.new_user(user, name, -1)
        else:
            db.update_user(user, name, data[1]-1)