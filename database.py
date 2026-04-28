import sqlite3

# Подключаемся к базе данных (если файла нет — он создастся)
# Ühendume andmebaasiga (kui faili pole, see luuakse)
conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

#  Сохраняем результаты теста в базу данных
#  Salvestame testi tulemused andmebaasi
cursor.execute("""                  

CREATE TABLE IF NOT EXISTS users(
user_id INTEGER PRIMARY KEY,
level TEXT,
direction TEXT
)
""")
# Таблица пользователей (сохраняем уровень и направление)
# Kasutajate tabel (salvestame taseme ja suuna)
cursor.execute("""
CREATE TABLE IF NOT EXISTS my_words(
user_id INTEGER,
word TEXT
)
""")
# Таблица слов пользователя (слова, которые он добавил)
# Kasutaja sõnade tabel (tema lisatud sõnad)
cursor.execute("""
CREATE TABLE IF NOT EXISTS stats(
user_id INTEGER,
tests INTEGER,
correct INTEGER,
wrong INTEGER
)
""")
# Сохраняем изменения в базе данных
# Salvestame muudatused andmebaasis
conn.commit()
