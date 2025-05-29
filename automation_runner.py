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
    (1808, 324): 5,
    (1812, 260): 5,
    (397, 580): 1,
    (456, 606): 1,
    (1805, 321): 5,
    (1814, 415): 5,
    (1806, 443): 4,
    (1818, 257): 4,
    (1807, 321): 5,
    (1813, 414): 5,
    (1808, 444): 5,
    (1815, 231): 5
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
    (1808, 324, 'left'), 1,              # Step 1
    5,                                   # 5-second delay
    (1812, 260, 'left'), 1,              # Step 2
    5,                                   # 5-second delay
    (253, 495, 'drag_start'),            # Step 3 drag start
    (586, 751, 'drag_end'), 1,           # Step 3 drag end
    (397, 580, 'right'), 1,              # Step 4
    (456, 606, 'left'), 1,               # Step 5
    (287, 18, 'left'), 1,                # Step 6
    (205, 322, 'left'), 1,               # Step 7
    (322, 321, 'left'), 1,               # Step 8
    (1077, 385, 'left'), 1,              # Step 9
    ('ctrl+a',), 1,                      # Step 10 - Ctrl+A
    ('ctrl+v',), 1,                      # Step 11 - Ctrl+V
    (1173, 1110, 'left'), 1,             # Step 12
    (245, 19, 'left'), 1                 # Step 13
]

# === Clicks Step 3 (SPX) ===
clicks_step3 = [
    (244, 22, 'left'), 1,                # Step 1
    (1805, 321, 'left'), 1,              # Step 2
    5,                                   # 5-second delay
    (253, 495, 'drag_start'),            # Step 3 drag start
    (586, 751, 'drag_end'), 1,           # Step 3 drag end
    (378, 585, 'right'), 1,              # Step 4
    (444, 607, 'left'), 1,               # Step 5
    (295, 16, 'left'), 1,                # Step 6
    (181, 327, 'left'), 1,               # Step 7
    (320, 325, 'left'), 1,               # Step 8
    (1068, 432, 'left'), 1,              # Step 9
    ('ctrl+a',), 1,                      # Step 10 - Ctrl+A
    ('ctrl+v',), 1,                      # Step 11 - Ctrl+V
    (1172, 1111, 'left'), 1,             # Step 12
    (243, 21, 'left'), 1                 # Step 13
]

# === Clicks Step 4 (QQQ) ===
clicks_step4 = [
    (243, 16, 'left'), 1,                # Step 1
    (1814, 415, 'left'), 1,              # Step 2
    5,                                   # 5-second delay
    (253, 495, 'drag_start'),            # Step 3 drag start
    (586, 751, 'drag_end'), 1,           # Step 3 drag end
    (421, 626, 'right'), 1,              # Step 4
    (487, 654, 'left'), 1,               # Step 5
    (294, 21, 'left'), 1,                # Step 6
    (248, 321, 'left'), 1,               # Step 7
    (321, 322, 'left'), 1,               # Step 8
    (1062, 483, 'left'), 1,              # Step 9
    ('ctrl+a',), 1,                      # Step 10 - Ctrl+A
    ('ctrl+v',), 1,                      # Step 11 - Ctrl+V
    (1177, 1111, 'left'), 1,             # Step 12
    (244, 19, 'left'), 1                 # Step 13
]

# === Clicks Step 5 (SPY) ===
clicks_step5 = [
    (243, 15, 'left'), 1,                # Step 1
    (1806, 443, 'left'), 1,              # Step 2
    4,                                   # 4-second delay
    (256, 546, 'drag_start'),            # Step 3 drag start
    (568, 764, 'drag_end'), 1,           # Step 3 drag end
    (454, 630, 'right'), 1,              # Step 4
    (522, 661, 'left'), 1,               # Step 5
    (287, 19, 'left'), 1,                # Step 6
    (242, 327, 'left'), 1,               # Step 7
    (321, 320, 'left'), 1,               # Step 8
    (1074, 535, 'left'), 1,              # Step 9
    ('ctrl+a',), 1,                      # Step 10 - Ctrl+A
    ('ctrl+v',), 1,                      # Step 11 - Ctrl+V
    (1171, 1105, 'left'), 1,             # Step 12
    (242, 16, 'left'), 1                 # Step 13
]

# === Clicks Step 6 (Blind Spots ES) ===
clicks_step6 = [
    (242, 21, 'left'), 1,                # Step 1
    (1818, 257, 'left'), 1,              # Step 2
    4,                                   # 4-second delay
    (646, 531, 'drag_start'),            # Step 3 drag start
    (974, 670, 'drag_end'), 1,           # Step 3 drag end
    (826, 580, 'right'), 1,              # Step 4
    (888, 601, 'left'), 1,               # Step 5
    (285, 21, 'left'), 1,                # Step 6
    (226, 369, 'left'), 1,               # Step 7
    (291, 368, 'left'), 1,               # Step 8
    (1074, 330, 'left'), 1,              # Step 9
    ('ctrl+a',), 1,                      # Step 10 - Ctrl+A
    ('ctrl+v',), 1,                      # Step 11 - Ctrl+V
    (1175, 1110, 'left'), 1,             # Step 12
    (242, 19, 'left'), 1                 # Step 13
]

# === Clicks Step 7 (Blind Spots SPX) ===
clicks_step7 = [
    (239, 16, 'left'), 1,                # Step 1
    (1807, 321, 'left'), 1,              # Step 2
    5,                                   # 5-second delay
    (646, 531, 'drag_start'),            # Step 3 drag start
    (974, 670, 'drag_end'), 1,           # Step 3 drag end
    (811, 560, 'right'), 1,              # Step 4
    (910, 587, 'left'), 1,               # Step 5
    (287, 20, 'left'), 1,                # Step 6
    (227, 374, 'left'), 1,               # Step 7
    (291, 370, 'left'), 1,               # Step 8
    (1062, 382, 'left'), 1,              # Step 9
    ('ctrl+a',), 1,                      # Step 10 - Ctrl+A
    ('ctrl+v',), 1,                      # Step 11 - Ctrl+V
    (1177, 1110, 'left'), 1,             # Step 12
    (244, 19, 'left'), 1                 # Step 13
]

# === Clicks Step 8 (Blind Spots QQQ) ===
clicks_step8 = [
    (245, 17, 'left'), 1,                # Step 1
    (1813, 414, 'left'), 1,              # Step 2
    5,                                   # 5-second delay
    (646, 531, 'drag_start'),            # Step 3 drag start
    (974, 670, 'drag_end'), 1,           # Step 3 drag end
    (843, 589, 'right'), 1,              # Step 4
    (920, 618, 'left'), 1,               # Step 5
    (288, 20, 'left'), 1,                # Step 6
    (215, 374, 'left'), 1,               # Step 7
    (292, 371, 'left'), 1,               # Step 8
    (1057, 431, 'left'), 1,              # Step 9
    ('ctrl+a',), 1,                      # Step 10 - Ctrl+A
    ('ctrl+v',), 1,                      # Step 11 - Ctrl+V
    (1178, 1109, 'left'), 1,             # Step 12
    (242, 24, 'left'), 1                 # Step 13
]

# === Clicks Step 9 (Blind Spots SPY) ===
clicks_step9 = [
    (244, 21, 'left'), 1,                # Step 1
    (1808, 444, 'left'), 1,              # Step 2
    5,                                   # 5-second delay
    (646, 531, 'drag_start'),            # Step 3 drag start
    (974, 670, 'drag_end'), 1,           # Step 3 drag end
    (874, 587, 'right'), 1,              # Step 4
    (943, 613, 'left'), 1,               # Step 5
    (287, 19, 'left'), 1,                # Step 6
    (209, 369, 'left'), 1,               # Step 7
    (295, 372, 'left'), 1,               # Step 8
    (1058, 483, 'left'), 1,              # Step 9
    ('ctrl+a',), 1,                      # Step 10 - Ctrl+A
    ('ctrl+v',), 1,                      # Step 11 - Ctrl+V
    (1174, 1104, 'left'), 1,             # Step 12
    (245, 22, 'left'), 1                 # Step 13
]

# === Clicks Step 10 (Blind Spots NQ) ===
clicks_step10 = [
    (244, 19, 'left'), 1,                # Step 1
    (1815, 231, 'left'), 1,              # Step 2
    5,                                   # 5-second delay
    (646, 531, 'drag_start'),            # Step 3 drag start
    (974, 670, 'drag_end'), 1,           # Step 3 drag end
    (785, 537, 'right'), 1,              # Step 4
    (850, 566, 'left'), 1,               # Step 5
    (296, 25, 'left'), 1,                # Step 6
    (225, 369, 'left'), 1,               # Step 7
    (294, 370, 'left'), 1,               # Step 8
    (1059, 535, 'left'), 1,              # Step 9
    ('ctrl+a',), 1,                      # Step 10 - Ctrl+A
    ('ctrl+v',), 1,                      # Step 11 - Ctrl+V
    (1172, 1112, 'left'), 1,             # Step 12
    (245, 22, 'left'), 1                 # Step 13
]

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

# === Automated Step Input with Delay ===
def automated_step_input():
    print("\n🔹 Enter step(s) to run (1-10, 1+2, 2+3, etc., test_es, test_spx, test_qqq, test_spy, test_nq):")
    selected = input("⬆️  Your choice: ").strip().lower()
    print("⏳ Preparing to run your selection in 3 seconds...")
    time.sleep(3)
    return selected

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
    elif selected_steps == "7":
        run_click_sequence(clicks_step7, delay=DEFAULT_DELAY)
    elif selected_steps == "8":
        run_click_sequence(clicks_step8, delay=DEFAULT_DELAY)
    elif selected_steps == "9":
        run_click_sequence(clicks_step9, delay=DEFAULT_DELAY)
    elif selected_steps == "10":
        run_click_sequence(clicks_step10, delay=DEFAULT_DELAY)
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
    elif selected_steps == "6+7":
        run_click_sequence(clicks_step6 + clicks_step7, delay=DEFAULT_DELAY)
    elif selected_steps == "7+8":
        run_click_sequence(clicks_step7 + clicks_step8, delay=DEFAULT_DELAY)
    elif selected_steps == "8+9":
        run_click_sequence(clicks_step8 + clicks_step9, delay=DEFAULT_DELAY)
    elif selected_steps == "9+10":
        run_click_sequence(clicks_step9 + clicks_step10, delay=DEFAULT_DELAY)
    elif selected_steps == "test_es":
        print("\n🔹 Testing Blind Spots ES sequence only")
        run_click_sequence(clicks_step6, delay=DEFAULT_DELAY)
    elif selected_steps == "test_spx":
        print("\n🔹 Testing Blind Spots SPX sequence only")
        run_click_sequence(clicks_step7, delay=DEFAULT_DELAY)
    elif selected_steps == "test_qqq":
        print("\n🔹 Testing Blind Spots QQQ sequence only")
        run_click_sequence(clicks_step8, delay=DEFAULT_DELAY)
    elif selected_steps == "test_spy":
        print("\n🔹 Testing Blind Spots SPY sequence only")
        run_click_sequence(clicks_step9, delay=DEFAULT_DELAY)
    elif selected_steps == "test_nq":
        print("\n🔹 Testing Blind Spots NQ sequence only")
        run_click_sequence(clicks_step10, delay=DEFAULT_DELAY)
    else:
        print("❌ Invalid selection.")
