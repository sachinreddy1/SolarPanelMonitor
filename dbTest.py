import sqlite3
import datetime

def convertTime(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)

conn = sqlite3.connect('solarPanel.db')
cursor = conn.cursor()	

cursor.execute("SELECT timeRecorded, voltage_1 FROM voltages")
ret = cursor.fetchall()
conn.commit()

val = ""
for i in ret:
	i = (convertTime(i[0]) , i[1])
	val += str(i) + "\n"
print val


