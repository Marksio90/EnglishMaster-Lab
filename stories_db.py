import sqlite3, datetime
DB="users.sqlite"
def init_stories():
    con=sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS stories(id INTEGER PRIMARY KEY, uid INT, title TEXT, story TEXT, cefr TEXT, tone TEXT, created TEXT)")
    con.commit(); con.close()

def add_story(uid,title,story,cefr,tone):
    con=sqlite3.connect(DB)
    con.execute("INSERT INTO stories(uid,title,story,cefr,tone,created) VALUES(?,?,?,?,?,?)",(uid,title,story,cefr,tone,str(datetime.datetime.now())))
    con.commit(); con.close()