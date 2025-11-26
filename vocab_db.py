import sqlite3
DB="users.sqlite"
def add_word(w, level, cat):
    con=sqlite3.connect(DB); con.execute("CREATE TABLE IF NOT EXISTS vocab(id INTEGER PRIMARY KEY, word TEXT, level TEXT, category TEXT)")
    con.execute("INSERT INTO vocab(word,level,category) VALUES(?,?,?)",(w,level,cat)); con.commit(); con.close()
def get_words(level=None):
    con=sqlite3.connect(DB); r=con.execute("SELECT word, level, category FROM vocab").fetchall(); con.close();
    if level: r=[x for x in r if x[1]==level];
    return r