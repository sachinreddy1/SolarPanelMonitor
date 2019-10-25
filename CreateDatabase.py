import sqlite3

conn = sqlite3.connect('solarPanel.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE voltages (
			timeRecorded integer,
			voltage_1 real,
			voltage_2 real,
			voltage_3 real,
			voltage_4 real
			)""")

conn.commit()
conn.close()