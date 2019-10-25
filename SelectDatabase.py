import sqlite3

conn = sqlite3.connect('solarPanel.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM voltages")
ret = cursor.fetchall()

for i in ret:
	print i

conn.commit()
conn.close()