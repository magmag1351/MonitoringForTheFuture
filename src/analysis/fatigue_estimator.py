def estimate_fatigue(activity):
    """
    シンプルな疲労推定（ダミーモデル）
    CPU負荷・マウス・キーボード活動を重みづけしてスコア化
    """
    fatigue = (
        activity["cpu"] * 0.5 +
        activity["mouse"] * 0.3 +
        activity["keyboard"] * 0.2
    ) / 100
    return min(max(fatigue, 0), 1)
