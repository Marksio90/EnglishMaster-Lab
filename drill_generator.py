import sqlite3, random, datetime
DB="users.sqlite"
def init_drill_db():
    con=sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS drills(id INTEGER PRIMARY KEY, uid INT, question TEXT, answer TEXT, tag TEXT, due TEXT, created TEXT)")
    con.commit(); con.close()

def make_drills_from_error(eid, uid, text, tag):
    drills=[]
    pairs=[
       (f"Correct this sentence: {text}", "Corrected sentence", "error_correction"),
       (f"Rewrite using better vocabulary: {text}", "Improved sentence", "vocab_drill"),
       (f"Transform the sentence grammar: {text}", "Transformed sentence", "grammar_transform")
    ]
    for q,a,t in pairs:
        due=(datetime.date.today()+datetime.timedelta(days=1)).isoformat()
        con=sqlite3.connect(DB)
        con.execute("INSERT INTO drills(uid,question,answer,tag,due,created) VALUES(?,?,?,?,?,?)",(uid,q,t,due,str(datetime.datetime.now())))
        con.commit(); con.close()
        drills.append({"q":q,"a":"Saved","t":t,"due":due})
    return drills