import streamlit as st
import sqlite3, datetime
DB="users.sqlite"
def init_ipa_db():
    con=sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS ipa_samples(id INTEGER PRIMARY KEY, uid INT, text TEXT, ipa TEXT, score INT, created TEXT)")
    con.commit(); con.close()

def save_ipa(uid, text, ipa, score):
    con=sqlite3.connect(DB)
    con.execute("INSERT INTO ipa_samples(uid,text,ipa,score,created) VALUES(?,?,?,?,?)",(uid,text,ipa,score,str(datetime.datetime.now())))
    con.commit(); con.close()

def fake_ipa(text):
    return "/ˈfeɪk-ˈaɪ-piː-eɪ/"

def score_pron(text): return 72