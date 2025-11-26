import streamlit as st, sqlite3
from error_memory import init_error_db
init_error_db()
def show_errors(uid=None):
    con=sqlite3.connect("users.sqlite")
    q="SELECT id,uid,text,tag,created FROM errors"
    r=con.execute(q).fetchall()
    con.close()
    for e in r:
        st.error(f"{e[2]} ({e[3]})")