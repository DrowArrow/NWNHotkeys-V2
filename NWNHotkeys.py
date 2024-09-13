import keyboard
import pyautogui
import time

QBHK = 'ctrl + f'

def QB():
	for _ in range(10):
		MousePos = pyautogui.position()
		pyautogui.dragRel(
			xOffset= 300,
			button='right',
			duration= 0.257)
		pyautogui.moveTo(MousePos)
	return

keyboard.add_hotkey(QBHK, QB)

while True:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		break