import sqlite3
DB="users.sqlite"
def init_db():
    con=sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, level TEXT, streak INT, minutes INT)")
    con.commit(); con.close()
def add_user(n, l):
    con=sqlite3.connect(DB); con.execute("INSERT INTO users(name,level,streak,minutes) VALUES(?,?,0,0)",(n,l)); con.commit(); con.close()
def get_users(): con=sqlite3.connect(DB); r=con.execute("SELECT id,name,level,streak,minutes FROM users").fetchall(); con.close(); return r