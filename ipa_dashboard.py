import streamlit as st, sqlite3
DB="users.sqlite"
def show_ipa_samples(uid=None):
    con=sqlite3.connect(DB); cur=con.cursor()
    if uid:
        r=cur.execute("SELECT text,ipa,score,created FROM ipa_samples WHERE uid=?", (uid,)).fetchall()
    else:
        r=cur.execute("SELECT text,ipa,score,created FROM ipa_samples").fetchall()
    con.close()
    for t,ipa,sc,cr in r:
        st.metric("Word/Sentence", t, f"{sc}%")
        st.code(ipa)