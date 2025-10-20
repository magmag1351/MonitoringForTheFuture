import psutil
import keyboard
import mouse
import time

# 前回値保持用（キー・マウスカウント）
_last_keyboard_count = 0
_last_mouse_count = 0

def get_cpu_usage():
    """CPU使用率を取得（1秒間隔の平均）"""
    return psutil.cpu_percent(interval=1)

def get_keyboard_count():
    """キー入力数を簡易カウント"""
    global _last_keyboard_count
    count = keyboard._os_keyboard._pressed_keys_count  # keyboardモジュール内部カウント
    delta = count - _last_keyboard_count
    _last_keyboard_count = count
    return max(delta, 0)

def get_mouse_count():
    """マウスクリック数を簡易カウント"""
    global _last_mouse_count
    count = mouse.get_position()[0]  # マウス移動の変化を簡易カウントとして利用
    delta = count - _last_mouse_count
    _last_mouse_count = count
    return max(delta, 0)

def collect_activity():
    cpu_val = get_cpu_usage()
    key_val = get_keyboard_count()
    mouse_val = get_mouse_count()

    # 簡易疲労スコア計算（CPU/100 + key/100 + mouse/100 の平均）
    fatigue_score = (cpu_val/100 + key_val/100 + mouse_val/100) / 3

    return {
        "cpu": cpu_val,
        "keyboard": key_val,
        "mouse": mouse_val,
        "fatigue": fatigue_score
    }
