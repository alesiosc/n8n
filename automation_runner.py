import pyautogui
import time
import requests
import base64
from PIL import ImageGrab
import pyperclip
import threading
import keyboard
from dotenv import load_dotenv
import os

load_dotenv()

# === QWEN OCR CONFIG ===
QWEN_API_KEY = os.getenv("QWEN_API_KEY")
QWEN_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
QWEN_MODEL = "qwen-vl-2.5-32b"

# === CONFIGURATION ===
ocr_region = (207, 118, 415, 174)
DEFAULT_DELAY = 2
pause_flag = threading.Event()
pause_flag.set()

# === Qwen OCR Function ===
def qwen_ocr(region):
    image = ImageGrab.grab(bbox=region)
    image_path = "ocr_capture.png"
    image.save(image_path)
    with open(image_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": QWEN_MODEL,
        "messages": [
            {"role": "system", "content": "You are an OCR assistant. Read the following image."},
            {"role": "user", "content": "<image>"}
        ],
        "images": [img_data]
    }

    response = requests.post(QWEN_ENDPOINT, headers=headers, json=payload)
    try:
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print("❌ OCR Error:", e)
        return ""

# === Special Delays ===
special_delays = {
    (1809, 414): 6,
    (1819, 260): 6,
    (1808, 327): 6,
    (1829, 231): 6,
    (1817, 258): 6
}

# === Clicks Step 1 (NQ) ===
clicks = [
    (240, 18, 'left'), 1,                # Step 1
    (92, 61, 'left'), 1,                 # Step 2
    5,                                   # Inserted delay of 5 seconds
    (200, 285, 'left'), 1,               # Step 3
    (78, 319, 'left'), 1,                # Step 4
    (1826, 229, 'left'), 1,              # Step 5
    5,                                   # Inserted delay of 5 seconds
    (253, 495, 'drag_start'),            # Step 6 drag start
    (586, 751, 'drag_end'), 1,           # Step 6 drag end
    (408, 565, 'right'), 1,              # Step 7
    (476, 592, 'left'), 1,               # Step 8
    (287, 19, 'left'), 1,                # Step 9
    (200, 296, 'left'), 1,               # Step 10
    (325, 298, 'left'), 1,               # Step 11
    (1075, 331, 'left'), 1,              # Step 12
    ('ctrl+a',), 1,                      # Step 13 - Ctrl+A
    ('ctrl+v',), 1,                      # Step 14 - Ctrl+V
    (1174, 1105, 'left'), 1,             # Step 15
    (205, 319, 'left'), 1,               # Step 16
    (322, 323, 'left'), 1,               # Step 17
    (1074, 330, 'left'), 1,              # Step 18
    ('ctrl+a',), 1,                      # Step 19 - Ctrl+A
    ('ctrl+v',), 1,                      # Step 20 - Ctrl+V
    (1179, 1103, 'left'), 1,             # Step 21
    (242, 23, 'left'), 1                 # Step 22
]

# === Clicks Step 2 (ES) ===
clicks_step2 = [
    (245, 19, 'left'),
    (1809, 414, 'left'),
    (1819, 260, 'left'),
    (1817, 258, 'left'),
    (256, 515, 'drag_start'), (590, 768, 'drag_end'),
    (359, 614, 'right'), (421, 642, 'left'),
    (296, 24, 'left'),
    (142, 322, 'left'), (266, 319, 'left'), (1059, 384, 'left'),
    ('ctrl+v',),
    (246, 20, 'left')
]

# === Clicks Step 3 (SPX) ===
clicks_step3 = [
    (242, 19, 'left'),
    (1808, 327, 'left'),
    6,
    (1817, 258, 'left'),
    6,
    (256, 515, 'drag_start'), (590, 768, 'drag_end'),
    (285, 23, 'left'), (167, 321, 'left'), (264, 321, 'left'), (1065, 434, 'left'),
    ('ctrl+a',),
    ('ctrl+v',),
    (1121, 681, 'left')
]

# === Clicks Step 4 (QQQ) ===
clicks_step4 = [
    (246, 18, 'left'),
    (1812, 415, 'left'),
    (336, 582, 'drag_start'), (402, 609, 'drag_end'),
    (294, 21, 'left'),
    (1075, 481, 'left'), (1086, 481, 'right'),
    (1143, 778, 'left'), (1059, 483, 'right'),
    (1127, 652, 'left'), (246, 21, 'left')
]

# === Clicks Step 5 (SPY) ===
clicks_step5 = [
    (242, 17, 'left'), (1808, 442, 'left'),
    (359, 614, 'right'), (421, 642, 'left'), (296, 24, 'left'),
    (142, 322, 'left'), (266, 319, 'left'), (1059, 384, 'left'),
    ('ctrl+v',),
    (246, 20, 'left')
]

# === Clicks Step 6 (Blind Spots) ===
clicks_step6 = []

# === Toggle Pause Function ===
def monitor_pause():
    while True:
        keyboard.wait('space')
        if pause_flag.is_set():
            print("⏸️ Paused. Press space again to resume.")
            pause_flag.clear()
        else:
            print("▶️ Resumed.")
            pause_flag.set()

threading.Thread(target=monitor_pause, daemon=True).start()

# === Automated Step Input with Delay ===
def automated_step_input():
    print("\n🔹 Enter step(s) to run (1, 2, 3, 4, 5, 6, 1+2, 2+3, 3+4, 4+5, 5+6, etc.):")
    selected = input("⬆️  Your choice: ").strip()
    print("⏳ Preparing to run your selection in 3 seconds...")
    time.sleep(3)
    return selected

# === Define logic for executing selected steps ===
def run_click_sequence(sequence, delay=DEFAULT_DELAY):
    for item in sequence:
        pause_flag.wait()
        if isinstance(item, (int, float)):
            print(f"⏳ Waiting {item} seconds...")
            time.sleep(item)
            continue
        if isinstance(item, tuple) and len(item) == 3:
            x, y, btn = item
            if btn == 'drag_start':
                print(f"🔃 Drag Start at ({x}, {y})")
                pyautogui.moveTo(x, y)
                pyautogui.mouseDown()
            elif btn == 'drag_end':
                print(f"🔃 Drag End at ({x}, {y})")
                pyautogui.moveTo(x, y)
                pyautogui.mouseUp()
            else:
                print(f"🖱️ Click at ({x}, {y}) [{btn.upper()}]")
                pyautogui.moveTo(x, y)
                pyautogui.click(button=btn)
                if (x, y) in special_delays:
                    delay_time = special_delays[(x, y)]
                    print(f"⏳ Waiting {delay_time}s after click at ({x}, {y})")
                    time.sleep(delay_time)
                    continue
        elif isinstance(item, tuple) and item[0] == 'ctrl+a':
            print("⌨️ Sending Ctrl+A")
            pyautogui.hotkey('ctrl', 'a')
        elif isinstance(item, tuple) and item[0] == 'ctrl+v':
            print("⌨️ Sending Ctrl+V")
            pyautogui.hotkey('ctrl', 'v')
        elif isinstance(item, tuple) and item[0] == 'ctrl':
            print("⌨️ Ctrl pressed")
            pyautogui.keyDown('ctrl')
        elif isinstance(item, tuple) and item[0] == '☺':
            print("⌨️ Typing ☺")
            pyautogui.press('v')
        elif isinstance(item, tuple) and item[0] == '▬':
            print("⌨️ Typing ▬")
            pyautogui.press('c')
        time.sleep(delay)
    print("✅ Automation complete.")

# === Entry Point ===
if __name__ == "__main__":
    selected_steps = automated_step_input()

    if selected_steps == "1":
        run_click_sequence(clicks, delay=DEFAULT_DELAY)
    elif selected_steps == "2":
        run_click_sequence(clicks_step2, delay=DEFAULT_DELAY)
    elif selected_steps == "3":
        run_click_sequence(clicks_step3, delay=DEFAULT_DELAY)
    elif selected_steps == "4":
        run_click_sequence(clicks_step4, delay=DEFAULT_DELAY)
    elif selected_steps == "5":
        run_click_sequence(clicks_step5, delay=DEFAULT_DELAY)
    elif selected_steps == "6":
        run_click_sequence(clicks_step6, delay=DEFAULT_DELAY)
    elif selected_steps == "1+2":
        run_click_sequence(clicks + clicks_step2, delay=DEFAULT_DELAY)
    elif selected_steps == "2+3":
        run_click_sequence(clicks_step2 + clicks_step3, delay=DEFAULT_DELAY)
    elif selected_steps == "3+4":
        run_click_sequence(clicks_step3 + clicks_step4, delay=DEFAULT_DELAY)
    elif selected_steps == "4+5":
        run_click_sequence(clicks_step4 + clicks_step5, delay=DEFAULT_DELAY)
    elif selected_steps == "5+6":
        run_click_sequence(clicks_step5 + clicks_step6, delay=DEFAULT_DELAY)
    else:
        print("❌ Invalid selection.")
