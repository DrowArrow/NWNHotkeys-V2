import keyboard
import pyautogui
import time
import psutil
import pygetwindow as gw

QBHK = 'ctrl + f'
TARGET_PROCESS = 'nwmain.exe'

def is_target_process_active():
	active_window = gw.getActiveWindow()
	
	if active_window is not None:
		try:
			process = psutil.Process(active_window._pid)
			return process.name() == TARGET_PROCESS
		except (psutil.NoSuchProcess, AttributeError):
			return False
	return False

def QB():
	if is_target_process_active():
		for _ in range(10):
			try:
				MousePos = pyautogui.position()
				pyautogui.dragRel(
					xOffset= 300,
					button='right',
					duration= 0.200)
				pyautogui.moveTo(MousePos)
			except Exception as e:
				print(f"Error during mouse action: {e}")
	else:
		print(f"Neverwinter Nights is not in focus or '{TARGET_PROCESS}' is not running")
  
keyboard.add_hotkey(QBHK, QB)

while True:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		break