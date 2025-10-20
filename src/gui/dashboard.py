import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import threading
import time

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "logs.db")

def get_latest_fatigue():
    """SQLiteから最新の疲労スコアを取得"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT fatigue FROM activity_log ORDER BY timestamp DESC LIMIT 1")
        row = cur.fetchone()
        conn.close()
        return float(row[0]) if row else 0.0
    except Exception as e:
        print(f"[WARN] DBアクセス中にエラー: {e}")
        return 0.0


def get_recent_activity_counts():
    """最近のCPU / キー / マウス平均値を取得"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            SELECT AVG(cpu), AVG(keyboard), AVG(mouse)
            FROM (
                SELECT cpu, keyboard, mouse
                FROM activity_log
                ORDER BY timestamp DESC
                LIMIT 30
            )
        """)
        row = cur.fetchone()
        conn.close()
        if row:
            return {"cpu": row[0] or 0, "keyboard": row[1] or 0, "mouse": row[2] or 0}
        return {"cpu": 0, "keyboard": 0, "mouse": 0}
    except Exception as e:
        print(f"[WARN] DBアクセス中にエラー: {e}")
        return {"cpu": 0, "keyboard": 0, "mouse": 0}


class FatigueDashboard:
    """リアルタイム更新型ダッシュボード"""
    def __init__(self, root):
        self.root = root
        self.root.title("Monitoring for the Future - Fatigue Dashboard")
        self.root.geometry("500x400")
        self.root.configure(bg="#f5f5f5")

        # --- UI要素 ---
        self.label_title = ttk.Label(root, text="🧠 Fatigue Monitoring Dashboard", font=("Segoe UI", 16, "bold"))
        self.label_title.pack(pady=20)

        self.label_score = ttk.Label(root, text="現在の疲労スコア: ---", font=("Segoe UI", 14))
        self.label_score.pack(pady=10)

        self.label_cpu = ttk.Label(root, text="CPU使用率: ---%", font=("Segoe UI", 12))
        self.label_cpu.pack(pady=5)

        self.label_keyboard = ttk.Label(root, text="キー入力数: ---", font=("Segoe UI", 12))
        self.label_keyboard.pack(pady=5)

        self.label_mouse = ttk.Label(root, text="マウスクリック数: ---", font=("Segoe UI", 12))
        self.label_mouse.pack(pady=5)

        self.status = ttk.Label(root, text="データ取得中...", font=("Segoe UI", 10))
        self.status.pack(pady=15)

        # 定期更新を開始
        self.update_interval_ms = 2000  # 2秒ごとに更新
        self.update_dashboard()

    def update_dashboard(self):
        """DBから最新データを取得してラベル更新"""
        fatigue = get_latest_fatigue()
        recent = get_recent_activity_counts()

        # --- ラベル更新 ---
        self.label_score.config(text=f"現在の疲労スコア: {fatigue:.2f}")
        self.label_cpu.config(text=f"CPU使用率: {recent['cpu']:.1f}%")
        self.label_keyboard.config(text=f"キー入力数: {recent['keyboard']:.1f}")
        self.label_mouse.config(text=f"マウスクリック数: {recent['mouse']:.1f}")

        # スコア色分け
        if fatigue < 0.4:
            self.label_score.config(foreground="green")
        elif fatigue < 0.7:
            self.label_score.config(foreground="orange")
        else:
            self.label_score.config(foreground="red")

        # 再実行予約
        self.root.after(self.update_interval_ms, self.update_dashboard)


def launch_gui():
    """GUI起動関数"""
    root = tk.Tk()
    app = FatigueDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
