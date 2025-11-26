import sqlite3, datetime
DB="users.sqlite"
def init_collocation():
    con=sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS collocations(id INTEGER PRIMARY KEY, phrase TEXT, level TEXT, tag TEXT, created TEXT)")
    con.commit(); con.close()
def add_colloc(p, lvl, tag):
    con=sqlite3.connect(DB)
    con.execute("INSERT INTO collocations(phrase,level,tag,created) VALUES(?,?,?,?)",(p,lvl,tag,str(datetime.datetime.now())))
    con.commit(); con.close()
def get_colloc(lvl=None):
    con=sqlite3.connect(DB); r=con.execute("SELECT phrase,level,tag FROM collocations").fetchall(); con.close()
    if lvl: r=[x for x in r if x[1]==lvl]
    return r