from config import MY_CHAT
import pickle

data = {
    'id_user': 0,
    'id_chat': MY_CHAT,
    'word': '',
    'time': '2016-Aug-04 08:24:38'
}

class SessionHelper:
    pass
            
    def start_session(self):
        try: 
            with open('data.pickle', 'rb') as f:
                pickle.load(f)
        except:
            with open('data.pickle', 'wb') as f:
                pickle.dump(data, f)

    def load_data(self, data_new):
        with open('data.pickle', 'wb') as f:
            pickle.dump(data_new, f)

    def read_data(self):
        with open('data.pickle', 'rb') as f:
            data_new = pickle.load(f)
        return data_new