import sqlite3
DB="users.sqlite"
def init_listening_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS listening(id INTEGER PRIMARY KEY, title TEXT, level TEXT, topic TEXT, script TEXT, created TEXT)")
    con.commit(); con.close()

def add_listening(title, level, topic, script):
    con = sqlite3.connect(DB)
    con.execute("INSERT INTO listening(title, level, topic, script, created) VALUES(?,?,?,?,?)",
                (title, level, topic, script, str(datetime.datetime.now())))
    con.commit(); con.close()

def get_listening(level=None):
    con = sqlite3.connect(DB); cur = con.cursor()
    if level:
        r = cur.execute("SELECT id,title,level,topic,script FROM listening WHERE level=?", (level,)).fetchall()
    else:
        r = cur.execute("SELECT id,title,level,topic,script FROM listening").fetchall()
    con.close(); return r