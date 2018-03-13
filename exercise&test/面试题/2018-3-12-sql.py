import sqlite3
conn = sqlite3.connect('test.db')
c = conn.cursor()
p=c.execute("select sid from A where not exists (select distinct sid from A where SNAME='p7')")
for i in p:
    print(i)
conn.commit()
conn.close()
