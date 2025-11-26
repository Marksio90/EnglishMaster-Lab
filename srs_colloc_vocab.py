import sqlite3, datetime
DB="users.sqlite"
class SRSVocabColloc:
    def __init__(self): self.load()
    def load(self):
        con=sqlite3.connect(DB)
        con.execute("CREATE TABLE IF NOT EXISTS review(id INTEGER PRIMARY KEY, uid INT, item TEXT, type TEXT, due TEXT)")
        self.items={"vocab":con.execute("CREATE TABLE IF NOT EXISTS vocab(id INTEGER PRIMARY KEY, word TEXT, level TEXT, category TEXT)"), "colloc":con.execute("CREATE TABLE IF NOT EXISTS collocations(id INTEGER PRIMARY KEY, phrase TEXT, level TEXT, tag TEXT, created TEXT)")}
        con.commit(); con.close()
    def add(self, uid, item, t):
        due=(datetime.date.today()+datetime.timedelta(days=1)).isoformat()
        con=sqlite3.connect(DB); con.execute("INSERT INTO review(uid,item,type,due) VALUES(?,?,?,?)",(uid,item,t,due)); con.commit(); con.close()
    def get_due(self):
        con=sqlite3.connect(DB); r=con.execute("SELECT uid,item,type,due FROM review WHERE due<=? ",(datetime.date.today().isoformat(),)).fetchall(); con.close(); return r