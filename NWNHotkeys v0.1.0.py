from platform import version
import keyboard
import mouse
import time
import pygetwindow as gw
import configparser as cp
import os
from tkinter import *

# version 0.2.0
TARGET_WINDOW = "Neverwinter Nights"

def create_config():
	config = cp.ConfigParser()

	config["General"] = {"QBHK": "ctrl + f", "LOOPS": "10"}
#	config["Options"] = {"Opacity": "100", "AlwaysOnTop": "1"}

	with open("config.ini", "w") as configfile:
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

def is_valid_hotkey(hotkey):
	valid_keys = ["ctrl", "shift", "alt", "f1", "f2", "f3", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "\\", "/", ",", ".", "[", "]", "'", "#", ";", "-"]
	parts = hotkey.lower().split("+")
	return all(part.strip() in valid_keys for part in parts)

def capture_key(event):
	keys = []
	if event.state & 0x0004:
		keys.append("ctrl")
	if event.state & 0x0001:
		keys.append("shift")
	if event.state & 0x0002:
		keys.append("alt")
	
	keys.append(event.keysym)
	new_hotkey = "+".join(keys)
	hotkeybox.delete(0, END)
	hotkeybox.insert(0, new_hotkey)

def update_hotkey():
	new_hotkey = hotkeybox.get()
	if is_valid_hotkey(new_hotkey):
		try:
			keyboard.remove_hotkey(config_data["QBHK"])
		except KeyError:
			pass

		keyboard.add_hotkey(new_hotkey, QB)
		config = cp.ConfigParser()
		config["General"] = {"QBHK": new_hotkey, "LOOPS": str(config_data["LOOP"])}
		with open("Config.ini", "w") as configfile:
			config.write(configfile)
		feedback_label.config(text=f"Hotkey updated to: {new_hotkey}", fg="green")
	else:
		feedback_label.config(text="invalid hotkey combination!", fg="red")
  
def update_loops():
	new_loopcount = buycountbox.get()
	if new_loopcount is not "":
		config = cp.ConfigParser()
		config["General"] = {"QBHK": str(config_data["QBHK"]), "LOOPS": new_loopcount}
		with open("Config.ini", "w") as configfile:
			config.write(configfile)
		feedback_label.config(text=f"Buy count updated to: {new_loopcount}", fg="green")
	else:
		feedback_label.config(text=f"Box cannot be empty!", fg="red")

def is_integer(char): #checks entered characters are numbers and NOT letters
    return char.isdigit() or char == ""

def QB():
	config_data = read_config()
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

root = Tk()
root.title("NWNHotkeys")
root.geometry("300x200")

hotkeylbl = Label(root, text = "Hotkey")
hotkeylbl.place(x=150, y=5)
hotkeybox = Entry()
hotkeybox.place(x=5, y=5)
hotkeybox.insert(0, config_data["QBHK"])
hotkeybox.bind("<Return>", lambda event: update_hotkey())
hotkeybox.bind("<KeyPress>", capture_key)

feedback_label = Label(root, text="")
feedback_label.place(x=50, y=70)

is_int = (root.register(is_integer), "%S") #validation used to restrict the entry box into only accept numbers

buycountlbl = Label(root, text="Buy Count")
buycountlbl.place(x=150, y=25)
buycountbox = Entry(root, validate="key", validatecommand=is_int)
buycountbox.place(x=5,y=27)
buycountbox.insert(0, config_data["LOOP"])
buycountbox.bind("<Return>", lambda event: update_loops())


root.mainloop()

while True:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		break