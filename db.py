import sqlite3


class DBHelper:
    def __init__(self, dbname="Crocostat.sqlite3"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def new_user(self, id_user, name_user, answer):
        stmt = "INSERT INTO statistic (id_user, name_user, answer) VALUES (?, ?, ?)"
        args = (id_user, name_user, answer)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def find_user(self, id_user):
        stmt = "SELECT name_user, answer FROM statistic WHERE id_user=(?)"
        args = (id_user, )
        return self.conn.execute(stmt, args).fetchone()
    
    def update_user(self, id_user, name_user, answer):
        stmt = "UPDATE statistic SET name_user=(?), answer=(?) WHERE id_user=(?)"
        args = (name_user, answer, id_user)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT * FROM statistic ORDER BY answer DESC"
        return self.conn.execute(stmt).fetchall()

