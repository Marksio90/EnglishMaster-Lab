import streamlit as st, sqlite3, datetime
DB="users.sqlite"
def init_theme():
    con=sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS ui_prefs(id INTEGER PRIMARY KEY, uid INT, theme TEXT, font TEXT, created TEXT)")
    con.commit(); con.close()

def save_theme(uid, theme, font):
    con=sqlite3.connect(DB)
    con.execute("INSERT INTO ui_prefs(uid,theme,font,created) VALUES(?,?,?,?)",(uid,theme,font,str(datetime.datetime.now())))
    con.commit(); con.close()