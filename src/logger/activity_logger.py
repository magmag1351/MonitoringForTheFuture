import time
import psutil
import sqlite3
from datetime import datetime
import threading

import mouse
import keyboard

DB_PATH = "data/logs.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            cpu_usage REAL,
            mouse_clicks INTEGER,
            keyboard_presses INTEGER
        )
    """)
    conn.commit()
    conn.close()


# --- カウンタ変数をグローバル管理 ---
mouse_clicks = 0
keyboard_presses = 0
lock = threading.Lock()


def on_mouse_event(event):
    global mouse_clicks
    with lock:
        mouse_clicks += 1


def on_keyboard_event(event):
    global keyboard_presses
    with lock:
        keyboard_presses += 1


def collect_activity():
    """CPU使用率と操作数を1秒ごとにDBへ記録"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # イベントフックを登録
    mouse.hook(on_mouse_event)
    keyboard.hook(on_keyboard_event)

    print("Activity logger started. Press Ctrl+C to stop.")

    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with lock:
                m, k = mouse_clicks, keyboard_presses
                mouse_clicks, keyboard_presses = 0, 0  # リセット

            cur.execute(
                "INSERT INTO activity_log (timestamp, cpu_usage, mouse_clicks, keyboard_presses) VALUES (?, ?, ?, ?)",
                (timestamp, cpu, m, k),
            )
            conn.commit()

    except KeyboardInterrupt:
        print("Logging stopped.")
        conn.close()
    finally:
        mouse.unhook_all()
        keyboard.unhook_all()
