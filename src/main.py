import threading
from src.logger.activity_logger import collect_activity
from src.gui.dashboard import Dashboard

if __name__ == "__main__":
    # ロガーをバックグラウンドで起動
    logger_thread = threading.Thread(target=collect_activity, daemon=True)
    logger_thread.start()

    # GUI起動
    app = Dashboard()
    app.mainloop()
