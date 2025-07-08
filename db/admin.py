import sqlite3
from datetime import datetime
con = sqlite3.connect("C:/Users/maksi/PycharmProjects/job hendler/db/taro.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                  sqlite3.PARSE_COLNAMES, check_same_thread=False)

def createTable():
    cursor = con.cursor()
    cursor.close()

def getAdminsId():
    cursor = con.cursor()
    req = cursor.execute("""SELECT telegramId FROM Users WHERE Status = "Admin" """, ).fetchall()
    if req == []:
        return []
    else:
        return req[0]
def get_today_done_orders():
    current_date = datetime.now().strftime("%d:%m:%Y")
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    cursor.execute(
        """
        SELECT 
            SUM(CAST(WorkerPrice AS INTEGER)) as total_worker_price,
            SUM(CAST(Price AS INTEGER)) as total_price
        FROM Orders
        WHERE Active = 1 AND Done = 1 
           
            AND DateDone = ?
        """,
        [current_date]
    )
    row = cursor.fetchone()
    cursor.close()

    return {
        "worker_price": row["total_worker_price"] or 0,
        "total_price": row["total_price"] or 0
        }

def show_managers(page: int = 0, page_size: int = 5):
    offset = page * page_size
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cursor.execute(
        """
        SELECT *
        FROM Users
        WHERE Status = 'Manager' 

        LIMIT ? OFFSET ?
        """,
        ( page_size, offset)
    )
    rows = cursor.fetchall()


    return [dict(row) for row in rows]

def count_managers() -> int:
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM Users WHERE Status = 'Manager' ", )
    return cursor.fetchone()[0]



def get_user_by_id(user_id: int):

    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Users WHERE TelegramId = ?", (user_id,))
    row = cur.fetchone()
    return dict(row) if row else None

def get_user_order_stats_all():

    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""
        SELECT 
            COUNT(*) AS count,
            COALESCE(SUM(CAST(Price AS INTEGER)), 0) AS total_price,
            COALESCE(SUM(CAST(WorkerPrice AS INTEGER)), 0) AS total_worker_price
        FROM Orders
        WHERE Done = 1   AND Active = 1 
    """)
    row =  cur.fetchone()
    return dict(row) if row else None


from datetime import datetime
import sqlite3


def get_user_order_stats_today():
    today = datetime.now().strftime("%d:%m:%Y")

    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""
        SELECT 
            COUNT(*) AS count,
            COALESCE(SUM(CAST(Price AS INTEGER)), 0) AS total_price,
            COALESCE(SUM(CAST(WorkerPrice AS INTEGER)), 0) AS total_worker_price
        FROM Orders
        WHERE Done = 1 AND Active = 1 AND dateDone = ?
    """, (today,))

    row = cur.fetchone()
    return dict(row) if row else None


def get_unpaid_worker_all():

    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""
        SELECT 
            COALESCE(SUM(CAST(WorkerPrice AS INTEGER)), 0) AS unpaid_total
        FROM Orders
        WHERE Done = 1 AND (Paid IS NULL OR Paid != 1)
    """)
    row = cur.fetchone()
    return row["unpaid_total"] if row else 0

def get_unpaid_worker_today():
    today = datetime.now().strftime("%d:%m:%Y")

    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""
         SELECT 
             COALESCE(SUM(CAST(WorkerPrice AS INTEGER)), 0) AS unpaid_total
         FROM Orders
         WHERE  Done = 1 AND (Paid IS NULL OR Paid != 1) AND dateDone = ?
     """, (today,))
    row = cur.fetchone()
    return row["unpaid_total"] if row else 0


def get_unpaid_workers_paginated(offset: int = 0, limit: int = 10):
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""
        SELECT 
            Orders.Id, 
            Orders.WorkerId, 
            Orders.WorkerPrice, 
            Orders.Adress, 
            Orders.DateCreated,
            Users.Name AS WorkerName
        FROM Orders
        LEFT JOIN Users ON Orders.WorkerId = Users.TelegramId
        WHERE Orders.Done = 1 
          AND Orders.Active = 1 
          AND (Orders.Paid IS NULL OR Orders.Paid != 1)
        ORDER BY Orders.Id DESC
        LIMIT ? OFFSET ?
    """, (limit, offset))
    return cur.fetchall()


def delete_manager_by_id(telegram_id:int):
    cursor = con.cursor()

    cursor.execute("DELETE FROM Users WHERE TelegramId = ?", [telegram_id])
    con.commit()

    deleted_count = cursor.rowcount  # количество удалённых строк
    cursor.close()
    return deleted_count > 0


def addManager(telegramId, Name , UserName):
    cursor = con.cursor()
    cursor.execute("""
            INSERT INTO Users (TelegramId, Name, UserName, Status)
            VALUES (?, ?, ?, ?)
        """, [telegramId, Name , UserName, 'Manager'])
    con.commit()
    cursor.close()



def count_unpaid_workers() -> int:
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""
        SELECT COUNT(*) AS total
        FROM Orders
        WHERE Done = 1 AND Active = 1 AND (Paid IS NULL OR Paid != 1)
    """)
    row = cur.fetchone()
    return row["total"] if row else 0



def get_order_to_pay(order_id):
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""
           SELECT Orders.Id, Orders.WorkerId, Orders.WorkerPrice, Orders.Adress, Orders.dateCreated,Orders.dateDone,
                  Users.Name AS WorkerName
           FROM Orders
           LEFT JOIN Users ON Orders.WorkerId = Users.TelegramId
           WHERE Orders.Id = ?
             
       """, (order_id,))
    order = cur.fetchone()
    return order




def set_order_paid(order_id):
    cur = con.cursor()
    cur.execute("""
           UPDATE Orders
           SET Paid = 1
           WHERE Id = ?
       """, (order_id,))
    con.commit()


def is_manager_exists(telegram_id: int) -> bool:

    cur = con.cursor()
    cur.execute("SELECT 1 FROM Users WHERE TelegramId = ? ", (telegram_id,))
    return cur.fetchone() is not None
