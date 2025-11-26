import streamlit as st, sqlite3
from drill_generator import init_drill_db
init_drill_db()
DB="users.sqlite"
def show_due_drills(uid=None):
    con=sqlite3.connect(DB); cur=con.cursor()
    if uid:
        r=cur.execute("SELECT id,uid,question,answer,tag FROM drills WHERE due<=?", (str(datetime.date.today()),)).fetchall()
    else:
        r=cur.execute("SELECT id,uid,question,answer,tag FROM drills WHERE due<=?", (str(datetime.date.today()),)).fetchall()
    con.close()
    for d in r:
        st.info(d[2])