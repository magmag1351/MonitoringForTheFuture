import sqlite3
import os

DB_PATH = os.path.join("data", "logs.db")

def init_db():
    """初回起動時にDBを作成"""
    os.makedirs("data", exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            cpu REAL,
            mouse REAL,
            keyboard REAL,
            fatigue REAL
        )
        """)
        conn.commit()

def insert_log(activity, fatigue):
    """活動データをDBに記録"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        INSERT INTO activity_log (timestamp, cpu, mouse, keyboard, fatigue)
        VALUES (?, ?, ?, ?, ?)
        """, (activity["timestamp"], activity["cpu"], activity["mouse"], activity["keyboard"], fatigue))
        conn.commit()

def fetch_latest_log():
    """最新のログを取得"""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("""
        SELECT timestamp, cpu, mouse, keyboard, fatigue
        FROM activity_log ORDER BY id DESC LIMIT 1
        """)
        row = cur.fetchone()
        if row:
            return {
                "timestamp": row[0],
                "cpu": row[1],
                "mouse": row[2],
                "keyboard": row[3],
                "fatigue": row[4]
            }
        return None
