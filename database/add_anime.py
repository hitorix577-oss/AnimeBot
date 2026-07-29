import sqlite3

conn = sqlite3.connect("anime.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO anime 
(title, poster, description, genre, rating, episodes)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    "Solo Leveling",
    "poster_url",
    "Sung Jin-Woo dunyodagi eng kuchsiz ovchi edi. Uning hayoti sirli tizim tufayli o'zgaradi.",
    "Action, Fantasy, Adventure",
    8.7,
    12
))

conn.commit()
conn.close()

print("Anime qo'shildi!")
