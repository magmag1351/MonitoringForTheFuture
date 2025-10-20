import tkinter as tk
from src.analysis.fatigue_estimator import calculate_fatigue_score

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Monitoring for the Future")
        self.geometry("400x200")

        self.label_fatigue = tk.Label(self, text="Fatigue Score: --", font=("Arial", 14))
        self.label_fatigue.pack(pady=20)

        self.update_score()

    def update_score(self):
        score = calculate_fatigue_score()
        self.label_fatigue.config(text=f"Fatigue Score: {score:.2f}")
        self.after(5000, self.update_score)  # 5秒ごとに更新

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
