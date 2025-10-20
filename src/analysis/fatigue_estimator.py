import sqlite3
import pandas as pd

DB_PATH = "data/logs.db"

def calculate_fatigue_score():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM activity_log ORDER BY id DESC LIMIT 100", conn)
    conn.close()

    if df.empty:
        return 0.0

    # 簡易疲労スコア = CPU使用率 + 入力頻度から推定
    df["activity_level"] = df["mouse_clicks"] + df["keyboard_presses"]
    fatigue = 0.5 * (df["cpu_usage"].mean() / 100) + 0.5 * (df["activity_level"].mean() / 1000)
    fatigue = min(max(fatigue, 0), 1)
    return fatigue
