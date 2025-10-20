import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "data/logs.db"

def show_activity_graph():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM activity_log", conn)
    conn.close()

    if df.empty:
        print("No data to visualize.")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    plt.figure(figsize=(8,4))
    plt.plot(df["timestamp"], df["cpu_usage"], label="CPU Usage (%)")
    plt.xlabel("Time")
    plt.ylabel("CPU Usage")
    plt.title("CPU Usage Trend")
    plt.legend()
    plt.tight_layout()
    plt.show()
