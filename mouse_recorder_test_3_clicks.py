from pynput import mouse
import time

clicks = []
click_counter = 1
MAX_CLICKS = 3  # Change this if you need more clicks

print("⏳ You have 3 seconds to prepare...")
time.sleep(3)
print(f"🎯 Start recording {MAX_CLICKS} clicks.\n")

def on_click(x, y, button, pressed):
    global click_counter
    if pressed:
        print(f"{button.name.upper()} at ({x}, {y})  [#{click_counter}]")
        clicks.append((x, y, button.name))
        click_counter += 1

        if len(clicks) < MAX_CLICKS:
            print("⏳ Waiting 1 second...")
            time.sleep(1)  # Force 1-second delay

        if len(clicks) >= MAX_CLICKS:
            return False

with mouse.Listener(on_click=on_click) as listener:
    listener.join()

print("\n📝 Generated click coordinates:")
for i, (x, y, btn) in enumerate(clicks, 1):
    print(f"    ({x}, {y}, '{btn}'),  # [#{i}]")
