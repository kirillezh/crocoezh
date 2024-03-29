import pickle, os
from dotenv import load_dotenv

#import .env file
load_dotenv()
MY_CHAT = int(os.getenv('MY_CHAT'))

#basic data in session
data = {
    'id_user': 0,
    'name_user': '',
    'id_chat': MY_CHAT,
    'word': '_',
    'time': '2016-Aug-04 08:24:38',
    "update": False,
    "warning": False,
    "language": "ua",
    "language_words": "ua"
}

#new SessionHelper
class SessionHelper:            
    def start_session(self):
        #Try to download session or start new seesion
        try: 
            with open('data.pickle', 'rb') as f:
                pickle.load(f)
        except:
            with open('data.pickle', 'wb') as f:
                pickle.dump(data, f)

    def load_data(self, data_new):
        #Upload new data to session
        with open('data.pickle', 'wb') as f:
            pickle.dump(data_new, f)

    def read_data(self):
        #Download data from session
        with open('data.pickle', 'rb') as f:
            data_new = pickle.load(f)
        return data_new

    def reset_data(self):
        with open('data.pickle', 'wb') as f:
            pickle.dump(data, f)