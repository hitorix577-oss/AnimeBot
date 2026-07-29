import sqlite3


def create_database():
    conn = sqlite3.connect("anime.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS anime (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        poster TEXT,
        description TEXT,
        genre TEXT,
        rating REAL,
        episodes INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS episodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        anime_id INTEGER,
        episode_number INTEGER,
        video_id TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        last_anime INTEGER,
        last_episode INTEGER
    )
    """)

    conn.commit()
    conn.close()


create_database()

print("Database yaratildi!")
