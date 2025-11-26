import sqlite3
DB="users.sqlite"
def init_error_db():
    con=sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS errors(id INTEGER PRIMARY KEY, uid INT, text TEXT, tag TEXT, created TEXT)")
    con.commit(); con.close()
def save_error(uid, txt, tag):
    con=sqlite3.connect(DB)
    from datetime import datetime
    con.execute("INSERT INTO errors(uid,text,tag,created) VALUES(?,?,?,?)",(uid,txt,tag,str(datetime.now())))
    con.commit(); con.close()