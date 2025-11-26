import sqlite3, datetime
DB="english.sqlite"
def init_db():
    con=sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, level TEXT, streak INT, minutes INT)")
    con.execute("CREATE TABLE IF NOT EXISTS vocab(id INTEGER PRIMARY KEY, word TEXT, level TEXT, category TEXT)")
    con.execute("CREATE TABLE IF NOT EXISTS collocations(id INTEGER PRIMARY KEY, phrase TEXT, level TEXT, tag TEXT)")
    con.execute("CREATE TABLE IF NOT EXISTS errors(id INTEGER PRIMARY KEY, uid INT, text TEXT, tag TEXT, created TEXT)")
    con.execute("CREATE TABLE IF NOT EXISTS srs(id INTEGER PRIMARY KEY, uid INT, item TEXT, type TEXT, due TEXT)")
    con.commit(); con.close()
