from pynput import mouse, keyboard as kb
import time

clicks = []
actions = []  # Stores both clicks and delays
MAX_CLICKS = 40

print("⏳ You have 3 seconds to prepare...")
time.sleep(3)
print("🎯 Start recording clicks and key presses (press Escape to cancel early)")

start_time = time.time()
last_event_time = start_time

# Function to introduce delay
def introduce_delay(delay):
    print(f"⏳ Waiting {delay} seconds...")
    time.sleep(delay)

# Flag to control the listeners
running = True

# === MOUSE CLICK HANDLER ===
def on_click(x, y, button, pressed):
    global last_event_time
    if pressed and running:
        now = time.time()
        delay = round(now - last_event_time, 3)
        last_event_time = now
        btn_type = 'right' if button == mouse.Button.right else 'left'
        print(f"{btn_type.upper()} at ({x}, {y})  [#{len(clicks)+1}]")
        clicks.append((x, y, btn_type, delay))
        actions.append(('click', x, y, btn_type, delay))

        # Introduce default delay
        introduce_delay(1)

        if len(clicks) >= MAX_CLICKS:
            print("✅ Max clicks reached.")
            return False

# === KEYBOARD PRESS HANDLER ===
def on_press(key):
    global last_event_time, running
    if not running:
        return False

    now = time.time()
    delay = round(now - last_event_time, 3)
    last_event_time = now

    try:
        if key.char is not None:
            if key.char.isdigit():
                seconds = int(key.char)
                print(f"⏱️ Inserted delay of {seconds} seconds")
                actions.append(('delay', seconds))
                # Introduce custom delay
                introduce_delay(seconds)
            else:
                print(f"KEY '{key.char}' pressed")
                actions.append(('key', key.char, delay))
                # Introduce default delay
                introduce_delay(1)
        else:
            print(f"SPECIAL KEY '{key}' pressed")
            actions.append(('key', str(key), delay))
            # Introduce default delay
            introduce_delay(1)
    except AttributeError:
        if key == kb.Key.esc:
            print("\n❌ Recording cancelled manually by pressing Escape.")
            running = False
            return False
        else:
            print(f"SPECIAL KEY '{key}' pressed")
            actions.append(('key', str(key), delay))
            # Introduce default delay
            introduce_delay(1)

# === LISTENING ===
try:
    with mouse.Listener(on_click=on_click) as mouse_listener, \
         kb.Listener(on_press=on_press) as keyboard_listener:
        while running:
            time.sleep(0.1)
except KeyboardInterrupt:
    print("\n❌ Recording cancelled manually.")

# === OUTPUT ===
print("\n📝 Final recorded sequence:")
for act in actions:
    if act[0] == 'click':
        _, x, y, btn, delay = act
        print(f"({x}, {y}, '{btn}'),")
    elif act[0] == 'delay':
        print(f"WAIT {act[1]}")
    elif act[0] == 'key':
        _, keyname, delay = act
        print(f"KEY '{keyname}'")
