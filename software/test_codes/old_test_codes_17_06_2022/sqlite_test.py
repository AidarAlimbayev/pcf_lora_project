import sqlite3
from cow_class import Cow


conn = sqlite3.connect('cow.db')

c = conn.cursor()

# c.execute("""CREATE TABLE cow (
#             id integer,
#             rf_id integer,
#             weight real,
#             spray_period integer,
#             next_spray_time integer,
#             last_drink_duration real
#             )""")

cow_1 = Cow(122, 1313, 313, 14, 28, 6)
cow_2 = Cow(124, 1414, 314, 14, 28, 4)

print(cow_1.id)
print(cow_1.rf_id)
print(cow_1.weight)

#c.execute("INSERT INTO cow VALUES ('123', '1212', '300', '14', '28', '7')")

c.execute("SELECT * FROM cow WHERE id = '123'")

print(c.fetchall())


conn.commit()

conn.close()