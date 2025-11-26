import datetime, sqlite3
from db import DB, init_db
def tick(uid):
    con=sqlite3.connect(DB); con.execute("UPDATE users SET minutes=minutes+5 WHERE id=?",(uid,));
    con.execute("UPDATE users SET streak=streak+1 WHERE id=?",(uid,)); con.commit(); con.close()