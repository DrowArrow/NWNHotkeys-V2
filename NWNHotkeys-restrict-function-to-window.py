import keyboard
import mouse
import time
import pygetwindow as gw


QBHK = 'ctrl + f'
TARGET_WINDOW = 'Neverwinter Nights'

def QB():
	active_window = gw.getActiveWindow()
	MousePos = mouse.get_position()
	if "Neverwinter Nights" in active_window.title:
			for _ in range(10):
				mouse.hold("right")
				mouse.move(300, 0, False, 0.2)
				mouse.release("right")
				mouse.move(*MousePos, True, 0.2)

keyboard.add_hotkey(QBHK, QB)

while True:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		break
