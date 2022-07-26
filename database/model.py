import sqlite3 as sql

#connect to SQLite
con = sql.connect('database.db')

#Create a Connection
cur = con.cursor()

#Drop users table if already exsist.
cur.execute("DROP TABLE IF EXISTS mitigasi")

#Create users table  in db_web database
query_sql ='CREATE TABLE "mitigasi" ("UID" INTEGER PRIMARY KEY AUTOINCREMENT, "sensor1" DOUBLE, "sensor2" DOUBLE, "sensor3" DOUBLE, "sensor4" DOUBLE, "sensor5" DOUBLE, "sensor6" DOUBLE, "sensor7" DOUBLE, "sensor8" DOUBLE, "sensor9" DOUBLE, "sensor10" DOUBLE, "kondisi" DOUBLE)'

cur.execute(query_sql)

#commit changes
con.commit()

#close the connection
con.close()