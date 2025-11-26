import sqlite3, datetime, random, streamlit as st
from database import DB, init_db
class SRS:
    def __init__(self): init_db(); self.load()
    def load(self): self.con=sqlite3.connect(DB); self.cur=self.con.cursor()
    def add(self,uid,item,t): due=(datetime.date.today()+datetime.timedelta(days=1)).isoformat(); self.cur.execute("INSERT INTO srs(uid,item,type,due) VALUES(?,?,?,?)",(uid,item,t,due)); self.con.commit()
    def due(self,uid=None): today=datetime.date.today().isoformat(); q="SELECT id,item,type,due FROM srs WHERE due<=?"+(" AND uid=? " if uid else ""); r=self.cur.execute(q,(today,uid) if uid else (today,)).fetchall(); return r
