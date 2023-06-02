import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO fretes (client, destination, value, execution_date) VALUES (?, ?, ?, ?)",
            ('PMG Distribuidora', 'Rua Tutoia, 1157', 230.0, '2023-03-01' )
            )

cur.execute("INSERT INTO fretes (client, destination, value, execution_date) VALUES (?, ?, ?, ?)",
            ('Mc Donalds', 'Alameda Santos, 238', 1200.0, '2023-03-01' )
            )

cur.execute("INSERT INTO despesas (client, execution_date, category, value) VALUES (?, ?, ?, ?)",
            ('PMG Distribuidora','2023-03-01', 'Alimentação', 20.0)
            )
cur.execute("INSERT INTO despesas (client, execution_date, category, value) VALUES (?, ?, ?, ?)",
            ('Mc Donalds','2023-03-11', 'Alimentação', 30.0)
            )

connection.commit()
connection.close()