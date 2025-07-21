import sqlite3
from datetime import datetime
con = sqlite3.connect("C:/Users/Никита/PycharmProjects/TamSyam/db/job.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                  sqlite3.PARSE_COLNAMES, check_same_thread=False)

def createTable():
    cursor = con.cursor()
    cursor.close()

def getManagersId():
    cursor = con.cursor()
    req = cursor.execute("""SELECT telegramId FROM Users WHERE Status = "Manager" """, ).fetchall()
    if req == []:
        return []
    else:
        return [row[0] for row in req]


def show_workers(page: int = 0, page_size: int = 5):
    offset = page * page_size
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cursor.execute(
        """
        SELECT *
        FROM Users
        WHERE Status = 'User' 

        LIMIT ? OFFSET ?
        """,
        ( page_size, offset)
    )
    rows = cursor.fetchall()


    return [dict(row) for row in rows]

def count_user_orders() -> int:
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM Users WHERE Status = 'User' ", )
    return cursor.fetchone()[0]



def get_user_by_id(user_id: int):

    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Users WHERE TelegramId = ?", (user_id,))
    row = cur.fetchone()
    return dict(row) if row else None

def get_user_order_stats(worker_id):

    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""
        SELECT 
            COUNT(*) AS count,
            COALESCE(SUM(CAST(Price AS INTEGER)), 0) AS total_price,
            COALESCE(SUM(CAST(WorkerPrice AS INTEGER)), 0) AS total_worker_price
        FROM Orders
        WHERE Done = 1   AND Active = 1 AND WorkerId = ?
    """, (worker_id,))
    row =  cur.fetchone()
    return dict(row) if row else None




def get_orders(page: int = 0, page_size: int = 5, id: int = 0):
    offset = page * page_size
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cursor.execute(
        """
        SELECT *
        FROM Orders
        

        LIMIT ? OFFSET ?
        """,
        (page_size, offset)
    )
    rows = cursor.fetchall()


    return [dict(row) for row in rows]


def count_orders() -> int:
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM Orders ")
    return cursor.fetchone()[0]


def getOrderWorker(id):
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cursor.execute(
        """
        SELECT Name, UserName
        FROM Users


        WHERE TelegramId = ?
        """,
        [int(id)]
    )
    rows = cursor.fetchall()


    return [dict(row) for row in rows]

def getOrder(id):
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    req = cursor.execute("""SELECT * FROM Orders WHERE Id = ? """, [id]).fetchall()
    cursor.close()

    return req[0]


def deleteOrderById(order_id: int) -> bool:
    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM orders WHERE id = ?", [order_id])
        con.commit()
        return cursor.rowcount > 0
    except Exception as e:

        return False



def addOrderFromManager(adress: str, name: str, phone: str, desc: str, dateArrive: str):
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO Orders (Adress, FullName, Phone, Description, dateCreated, ArriveDate)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (adress, name, phone, desc,     datetime.now().strftime("%d:%m:%Y"), dateArrive))
    con.commit()
    cursor.close()

def addWorkerFromManager(telegramId, Name , UserName):
    cursor = con.cursor()
    cursor.execute("""
            INSERT INTO Users (TelegramId, Name, UserName, Status)
            VALUES (?, ?, ?, ?)
        """, [telegramId, Name , UserName, 'User'])
    con.commit()
    cursor.close()


def deleteUserFromManager(telegram_id):
    cursor = con.cursor()

    cursor.execute("DELETE FROM Users WHERE TelegramId = ?", [telegram_id])
    con.commit()

    deleted_count = cursor.rowcount
    cursor.close()
    return deleted_count > 0





def is_worker_exists(telegram_id: int) -> bool:

    cur = con.cursor()
    cur.execute("SELECT 1 FROM Users WHERE TelegramId = ?", (telegram_id,))
    return cur.fetchone() is not None
