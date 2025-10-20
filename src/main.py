import tkinter as tk
from src.gui.dashboard import FatigueDashboard
from src.logger.activity_logger import collect_activity
from utils.db_handler import insert_log
import threading
import time

def activity_monitor_loop():
    """
    バックグラウンドでマウス/キーボード/CPU情報を収集し、
    SQLiteに保存するループ
    """
    while True:
        # データ収集
        activity = collect_activity()
        fatigue_score = activity['fatigue']  # collect_activity で fatigue を返す場合

        # データベースに保存
        insert_log(activity, fatigue_score)

        print(f"💾 データ保存完了: {activity} -> fatigue={fatigue_score:.2f}")

        # 1秒ごとに更新
        time.sleep(1)


def main():
    print("🔧 Fatigue Monitor 起動中...")

    # --- バックグラウンドスレッドでログ収集開始 ---
    monitor_thread = threading.Thread(target=activity_monitor_loop, daemon=True)
    monitor_thread.start()

    # --- GUI起動 ---
    root = tk.Tk()
    app = FatigueDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
