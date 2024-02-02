import sqlite3

con = sqlite3.connect("routers.db")
cur = con.cursor()
cur.execute("CREATE TABLE Routers(ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL, IP TEXT NOT NULL, USERNAME TEXT NOT NULL, PASSWORD TEXT NOT NULL, BACKUP_TIME TIME )")
res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchone())
con.close

con = sqlite3.connect("netflow.db")
cur = con.cursor()
cur.execute("CREATE TABLE Netflowdata(ID INTEGER PRIMARY KEY AUTOINCREMENT, DATE TEXT, TIME TEXT, ROUTER_IP TEXT, NO_OF_PACKETS INTEGER, SRC_IP TEXT, DES_IP TEXT, PROTOCOL TEXT, SRC_PRT TEXT, DES_PRT TEXT)")
res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchone())
con.close


con = sqlite3.connect("syslog.db")
cur = con.cursor()
cur.execute("CREATE TABLE syslog(ID INTEGER PRIMARY KEY AUTOINCREMENT, DATE TEXT, TIME TEXT, ROUTER_IP TEXT, MESSAGE TEXT)")
res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchone())
con.close

con = sqlite3.connect("linupdown.db")
cur = con.cursor()
cur.execute("CREATE TABLE link_up_down(ID INTEGER PRIMARY KEY AUTOINCREMENT, DATE TEXT, TIME TEXT, ROUTER_IP TEXT, INT_NAME TEXT, STATE TEXT)")
res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchone())
con.close