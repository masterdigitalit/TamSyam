import sqlite3
from datetime import datetime
import os
DB_PATH = "C:/Users/maksi/PycharmProjects/job hendler/db/job.db"
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
    con = sqlite3.connect("C:/Users/maksi/PycharmProjects/job hendler/db/job.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                               sqlite3.PARSE_COLNAMES,
                          check_same_thread=False)
    cursor = con.cursor()

    # Создание таблиц
    cursor.execute(CREATE_ORDERS_TABLE)
    cursor.execute(CREATE_USERS_TABLE)

    con.commit()
    con.close()
    print("✅ База данных успешно создана.")


