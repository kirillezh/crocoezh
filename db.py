import sqlite3

#new DBHelper
class DBHelper:
    def __init__(self, dbname="Crocostat.db"):
        #connect database
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        self.create_table()

    def create_table(self):
        #create table
        stmt = "CREATE TABLE IF NOT EXISTS statistic (id INTEGER PRIMARY KEY AUTOINCREMENT, id_user bigint, name_user varchar, answer int)"
        self.conn.execute(stmt)
        self.conn.commit()

    def new_user(self, id_user, name_user, answer):
        #add new user
        stmt = "INSERT INTO statistic (id_user, name_user, answer) VALUES (?, ?, ?)"
        args = (id_user, name_user, answer)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def find_user(self, id_user):
        #find user
        stmt = "SELECT name_user, answer FROM statistic WHERE id_user=(?)"
        args = (id_user, )
        return self.conn.execute(stmt, args).fetchone()
    
    def update_user(self, id_user, name_user, answer):
        #update  user
        stmt = "UPDATE statistic SET name_user=(?), answer=(?) WHERE id_user=(?)"
        args = (name_user, answer, id_user)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        #get all user
        stmt = "SELECT * FROM statistic ORDER BY answer DESC"
        return self.conn.execute(stmt).fetchall()

