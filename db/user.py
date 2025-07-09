import sqlite3
from datetime import datetime

con = sqlite3.connect("C:/Users/maksi/PycharmProjects/job hendler/db/job.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                  sqlite3.PARSE_COLNAMES, check_same_thread=False)
from utils.calcWorkerShare import   calculate_payout
def createTable():
    cursor = con.cursor()
    cursor.close()

def getUsersId():
    cursor = con.cursor()
    req = cursor.execute("""SELECT telegramId FROM Users WHERE Status = "User" """).fetchall()
    cursor.close()
    return [row[0] for row in req]


def addNewOrder(name, age, comment,category, telegramId, link):
    cursor = con.cursor()

    cursor.execute("INSERT INTO Orders (Name, Age, Comment, Category,telegramId, Status, Link, Response ) VALUES (?,?,?,?,?,?,?,?)",
                   [name, age, comment,category,telegramId, str(0), str(link), '' ])
    con.commit()
    cursor.close()
def getOrder(id):
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    req = cursor.execute("""SELECT * FROM Orders WHERE Id = ? """, [id]).fetchall()
    cursor.close()

    return req[0]


def get_orders(page: int = 0, page_size: int = 5):
    offset = page * page_size
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cursor.execute(
        """
        SELECT *
        FROM Orders
        WHERE  Active IS NOT 1
        
        LIMIT ? OFFSET ?
        """,
        (page_size, offset)
    )
    rows = cursor.fetchall()

    return [dict(row) for row in rows]
def count_orders() -> int:

    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM Orders WHERE Active IS NOT 1")
    return cursor.fetchone()[0]


def setOrderActive(workerId, id):
    cursor = con.cursor()
    current_date = datetime.now().strftime("%d:%m:%Y")

    req = cursor.execute("""
        UPDATE Orders 
        SET Active = 1, 
            WorkerId = ?, 
            dateStarted = ?
        WHERE Id = ?
    """, [workerId, current_date, id])

    con.commit()
    cursor.close()

    return req


def get_user_orders(page: int = 0, page_size: int = 5, id: int = 0):
    offset = page * page_size
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cursor.execute(
        """
        SELECT *
        FROM Orders
        WHERE Active = 1  AND Done IS NOT 1 
        AND
        WorkerId = ?

        LIMIT ? OFFSET ?
        """,
        (id,page_size, offset)
    )
    rows = cursor.fetchall()
    print(rows)
    print(id)

    return [dict(row) for row in rows]


def count_user_orders(id) -> int:
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM Orders        WHERE Active = 1 AND WorkerId = ? AND Done IS NOT 1", [id])
    return cursor.fetchone()[0]
def confirmOrder(id, price, comment):
    cursor = con.cursor()
    current_date = datetime.now().strftime("%d:%m:%Y")
    req = cursor.execute("""UPDATE Orders SET Done = 1  , Price = ?, Description = ?, WorkerPrice = ?, DateDone = ? WHERE Id = ? """, [price,comment,calculate_payout(int(price)),current_date ,  id])
    con.commit()
    cursor.close()

    return req

def get_user_done_paid_orders(id):
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cursor.execute(
        """
        SELECT SUM(CAST(WorkerPrice AS INTEGER)) as total
        FROM Orders
        WHERE Active = 1 AND Done = 1  AND WorkerId = ?
        """,
        [id]
    )
    row = cursor.fetchone()
    return row["total"] or 0


