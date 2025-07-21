import sqlite3
from datetime import datetime
con = sqlite3.connect("C:/Users/Никита/PycharmProjects/TamSyam/db/job.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                  sqlite3.PARSE_COLNAMES, check_same_thread=False)







def get_all_orders():
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""
        SELECT 
            Id,
            Adress,
            Price,
            FullName,
            Phone,
            Done,
            WorkerId,
            Active,
            WorkerPrice,
            dateCreated,
            dateStarted,
            dateDone
        FROM Orders
        ORDER BY Id DESC
    """)
    rows = cur.fetchall()
    return [dict(row) for row in rows]


def get_users_stats():
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""
        SELECT 
            u.Name AS WorkerName,
            u.TelegramId,
            u.Status,
            COUNT(o.Id) AS OrdersCount,
            SUM(o.WorkerPrice) AS TotalEarned
        FROM Users u
        LEFT JOIN Orders o ON u.TelegramId = o.WorkerId AND o.Done = 1
        GROUP BY u.TelegramId
        ORDER BY OrdersCount DESC
    """)
    rows = cur.fetchall()
    return [dict(row) for row in rows]


def get_finance_stats():
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    today = datetime.now().strftime("%d:%m:%Y")

    cur.execute("""
        SELECT DISTINCT substr(dateDone, 4, 7) as month_year
        FROM Orders
        WHERE Done = 1 AND Active = 1
        ORDER BY month_year
    """)
    months = [row["month_year"] for row in cur.fetchall()]

    monthly_stats = []
    for month in months:
        like_pattern = f"%:{month}"

        cur.execute("""
            SELECT 
                COALESCE(SUM(CAST(Price AS INTEGER)), 0) AS income_month,
                COALESCE(SUM(CAST(WorkerPrice AS INTEGER)), 0) AS workers_month
            FROM Orders
            WHERE Done = 1 AND Active = 1 AND dateDone LIKE ?
        """, (like_pattern,))
        month_data = cur.fetchone()

        mm, yyyy = month.split(":")
        month_name = datetime.strptime(f"{yyyy}-{mm}-01", "%Y-%m-%d").strftime("%B %Y").capitalize()

        monthly_stats.append({
            "Месяц": month_name,
            "Доход (мес)": month_data["income_month"],
            "Выплаты (мес)": month_data["workers_month"],
            "Прибыль (мес)": month_data["income_month"] - month_data["workers_month"]
        })

    cur.execute("""
        SELECT 
            COALESCE(SUM(CAST(Price AS INTEGER)), 0) AS income_day,
            COALESCE(SUM(CAST(WorkerPrice AS INTEGER)), 0) AS workers_day
        FROM Orders
        WHERE Done = 1 AND Active = 1 AND dateDone = ?
    """, (today,))
    day = cur.fetchone()

    cur.execute("""
        SELECT 
            COALESCE(SUM(CAST(Price AS INTEGER)), 0) AS income_all,
            COALESCE(SUM(CAST(WorkerPrice AS INTEGER)), 0) AS workers_all
        FROM Orders
        WHERE Done = 1 AND Active = 1
    """)
    all_time = cur.fetchone()

    return {
        "По месяцам": monthly_stats,
        "Сегодня": {
            "Доход (день)": day["income_day"],
            "Выплаты (день)": day["workers_day"],
            "Прибыль (день)": day["income_day"] - day["workers_day"]
        },
        "За всё время": {
            "Доход (всего)": all_time["income_all"],
            "Выплаты (всего)": all_time["workers_all"],
            "Прибыль (всего)": all_time["income_all"] - all_time["workers_all"]
        }
    }
