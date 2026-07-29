import sqlite3


def get_anime(anime_id):
    conn = sqlite3.connect("database/anime.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM anime WHERE id = ?",
        (anime_id,)
    )

    anime = cursor.fetchone()

    conn.close()

    return anime
def search_anime(name):
    conn = sqlite3.connect("database/anime.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM anime WHERE title LIKE ?",
        ('%' + name + '%',)
    )

    anime = cursor.fetchone()

    conn.close()

    return anime
