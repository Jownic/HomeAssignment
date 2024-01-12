import sqlite3


#ManageDEvices.py Router list
con = sqlite3.connect("routers.db")
cur = con.cursor()
cur.execute("CREATE TABLE Routers(ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL, IP TEXT NOT NULL, USERNAME TEXT NOT NULL, PASSWORD TEXT NOT NULL)")
res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchone())
con.close
