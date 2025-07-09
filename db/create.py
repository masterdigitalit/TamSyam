import sqlite3
import os

DB_PATH = "job.db"  # путь к файлу БД

# SQL-команды для создания таблиц
# ⚠️ Эти команды должны точно соответствовать структуре твоей БД!
CREATE_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS Orders (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Adress TEXT,
    Price TEXT,
    WorkerPrice TEXT,
    WorkerId INTEGER,
    dateCreated TEXT,
    dateStarted TEXT,
    dateDone TEXT,
    Done INTEGER DEFAULT 0,
    Active INTEGER DEFAULT 0,
    FullName TEXT
);
"""

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS Users (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    TelegramId TEXT,
    FullName TEXT,
    Role TEXT,
    IsBanned INTEGER DEFAULT 0
);
"""

def init_db():
    if os.path.exists(DB_PATH):
        print("✅ База данных уже существует.")
        return

    print("⚙️ Создание новой базы данных...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Создание таблиц
    cursor.execute(CREATE_ORDERS_TABLE)
    cursor.execute(CREATE_USERS_TABLE)

    conn.commit()
    conn.close()
    print("✅ База данных успешно создана.")


