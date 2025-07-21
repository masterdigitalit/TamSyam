import sqlite3
from datetime import datetime
con = sqlite3.connect("C:/Users/Никита/PycharmProjects/TamSyam/db/job.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                  sqlite3.PARSE_COLNAMES, check_same_thread=False)

def createTable():
    cursor = con.cursor()
    cursor.close()

def getOwnersId():
    cursor = con.cursor()
    req = cursor.execute("""SELECT telegramId FROM Users WHERE Status = "Owner" """, ).fetchall()
    print(req)
    if req == []:
        return [0]
    else:
        return [row[0] for row in req]
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










def delete_manager_by_id(telegram_id:int):
    cursor = con.cursor()

    cursor.execute("DELETE FROM Users WHERE TelegramId = ?", [telegram_id])
    con.commit()

    deleted_count = cursor.rowcount
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









def is_manager_exists(telegram_id: int) -> bool:

    cur = con.cursor()
    cur.execute("SELECT 1 FROM Users WHERE TelegramId = ? ", (telegram_id,))
    return cur.fetchone() is not None





def get_all_order_months():
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("""
         SELECT DISTINCT substr(dateDone, 4, 7) as month_year
         FROM Orders
         WHERE Done = 1 AND Active = 1
     """)

    raw_months = [row["month_year"] for row in cur.fetchall()]

    result = []
    for item in raw_months:
        try:
            mm, yyyy = item.split(":")
            date_obj = datetime.strptime(f"{yyyy}-{mm}-01", "%Y-%m-%d")
            formatted = date_obj.strftime("%B %Y").capitalize()
            result.append({
                "Name": formatted,
                "Key": f"{mm}:{yyyy}"
            })
        except ValueError:
            continue  # если дата повреждена — пропустить

    # Сортировка по дате
    result.sort(key=lambda x: datetime.strptime(x["Key"], "%m:%Y"))
    return result

def get_month_stats(month_key: str):
    # Пример: month_key = "03:2025"
    cur = con.cursor()
    like_pattern = f"%:{month_key}"

    cur.execute("""
        SELECT
            COUNT(*) AS count,
            COALESCE(SUM(CAST(Price AS INTEGER)), 0) AS total_price,
            COALESCE(SUM(CAST(WorkerPrice AS INTEGER)), 0) AS total_worker_price
        FROM Orders
        WHERE Done = 1 AND Active = 1 AND dateDone LIKE ?
    """, (like_pattern,))

    row = cur.fetchone()
    return {
        "count": row[0],
        "total_price": row[1],
        "total_worker_price": row[2],
        "profit": row[1] - row[2]
    }