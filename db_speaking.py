import sqlite3, datetime
DB="users.sqlite"
def init_speaking():
    con=sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS speaking_samples(id INTEGER PRIMARY KEY, uid INT, transcript TEXT, created TEXT)")
    con.commit(); con.close()
def save(uid, txt):
    con=sqlite3.connect(DB)
    con.execute("INSERT INTO speaking_samples(uid,transcript,created) VALUES(?,?,?)",(uid,txt,str(datetime.datetime.now())))
    con.commit(); con.close()
