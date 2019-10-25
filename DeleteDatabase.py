import sqlite3

conn = sqlite3.connect('solarPanel.db')
cursor = conn.cursor()

cursor.execute("DELETE FROM voltages")

conn.commit()
conn.close()