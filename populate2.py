import sqlite3

conn = sqlite3.connect('imdb')
c = conn.cursor()

id_pk=range(400)
seat_no=1
room_no = 0
type_multiplier = 1
table = (id_pk, seat_no, room_no, type_multiplier)


for item in id_pk:
    if not(item % 100):  
        room_no +=1
        seat_no = 1
    type_multiplier = 1
    if  61 <= seat_no <= 80:
        type_multiplier = 1.3
    table = (item, seat_no, room_no, type_multiplier)
    c.execute("INSERT INTO universal_gopher_seat VALUES (?,?,?,?)", table)
    seat_no += 1
        


conn.commit()
conn.close()
