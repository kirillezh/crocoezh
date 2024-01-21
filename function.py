import random, os
from datetime import datetime
from dotenv import load_dotenv

#import .env file
load_dotenv()
MY_CHAT = os.getenv('MY_CHAT')
TIME_DELTA = int(os.getenv('TIME_DELTA'))
#FILE = os.getenv('WORDFILE')

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

    def file_words(self):
        data = session.read_data()
        if(data['language_words'] == 'ru'):
            return 'croco_ru.txt'
        else:
            return 'croco_ua.txt'
    def random_word(self):
        #new random word from database
        file = open(self.file_words(), "r")
        lines = file.readlines()
        return lines[random.randint(0, len(lines)-1)].strip()

    def new_word(self):
        #Load new user to session
        data = session.read_data()
        data['word'] = self.random_word()
        data['time'] = datetime.now().strftime('%Y-%b-%d %H:%M:%S')
        data['update'] = False
        session.load_data(data)
        return data['word'] 
    

    def update_user(self, user, name, chat):
        #Load new word to session
        data = session.read_data()
        data['id_user'] = user
        data['name_user'] = name
        data['id_chat'] = MY_CHAT
        data['word'] = self.random_word()
        data['time'] = datetime.now().strftime('%Y-%b-%d %H:%M:%S')
        data['update'] = False
        data['warning'] = False
        session.load_data(data)
    
    def update_time(self):
        #Load new word to session
        data = session.read_data()
        if(not data['update']):
            data['time'] = datetime.now().strftime('%Y-%b-%d %H:%M:%S')
            data['update'] = True
            session.load_data(data)
    
    def warning_user(self):
        #Warning to reset
        data = session.read_data()
        data['warning'] = True
        session.load_data(data)

    def reset_user(self):
        data = session.read_data()
        data['id_user'] = 0
        data['name_user'] = ''
        data['word'] = ''
        data['time'] = datetime.now().strftime('%Y-%b-%d %H:%M:%S')
        data['update'] = False
        data['warning'] = False
        session.load_data(data)

    def update_data(self, id, data_new):
        data = session.read_data()
        data[id] = data_new
        session.load_data(data)

    def db_update_user(self, user, name):
        #Update user to database with +1
        data = db.find_user(user)
        if(data == None):
            db.new_user(user, name, 1)
        else:
            db.update_user(user, name, max(data[1]+1, 0))

    def db_user_downgrade(self, user, name):
        #Update user to database with -1
        data = db.find_user(user)
        if(data == None):
            db.new_user(user, name, -1)
        else:
            db.update_user(user, name, max(data[1]-1, -1))
