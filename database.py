import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
user_id INTEGER PRIMARY KEY,
level TEXT,
direction TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS my_words(
user_id INTEGER,
word TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS stats(
user_id INTEGER,
tests INTEGER,
correct INTEGER,
wrong INTEGER
)
""")

conn.commit()
