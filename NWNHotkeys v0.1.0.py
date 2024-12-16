import keyboard
import mouse
import time
import pygetwindow as gw
import configparser as cp
import os

# version 0.0.1
TARGET_WINDOW = 'Neverwinter Nights'

def create_config():
	config = cp.ConfigParser()

	config["General"] = {"QBHK": "ctrl + f", "LOOPS": "10"}
#	config["Options"] = {"Opacity": "100", "AlwaysOnTop": "1"}

	with open('config.ini', 'w') as configfile:
		config.write(configfile)


if __name__ == "__main__":
	config_file_path = "config.ini"

	if not os.path.exists(config_file_path):
		create_config()
		print("No configuration found\nConfiguration file has been created")

def read_config():
	config = cp.ConfigParser()
	config.read("config.ini")
	
	LOOP = config.getint("General", "LOOPS")
	QBHK = config.get("General", "QBHK")
	
	config_values = {
		"LOOP": LOOP,
		"QBHK": QBHK
	}
	return config_values

if __name__ == "__main__":
	config_data = read_config()


def QB():
	active_window = gw.getActiveWindow()
	MousePos = mouse.get_position()
	loop_count = config_data["LOOP"]
	if TARGET_WINDOW in active_window.title:
		for _ in range(loop_count):
			mouse.hold("right")
			mouse.move(300, 0, False, 0.15)
			mouse.release("right")
			mouse.move(*MousePos, True, 0.15)

keyboard.add_hotkey(config_data["QBHK"], QB)

while True:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		break