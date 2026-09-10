import keyboard
import mouse
import pygetwindow as gw
import configparser as cp
import os
from tkinter import *


# ============================================================
# Version / configuration
# ============================================================

# version 0.2.1

TARGET_WINDOW = "Neverwinter Nights"
CONFIG_FILE = "config.ini"


# ============================================================
# Configuration
# ============================================================

def create_config():
    config = cp.ConfigParser()

    config["General"] = {
        "QBHK": "ctrl + f",
        "LOOPS": "10"
    }

    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)


def read_config():
    config = cp.ConfigParser()

    config.read(CONFIG_FILE)

    LOOP = config.getint(
        "General",
        "LOOPS"
    )

    QBHK = config.get(
        "General",
        "QBHK"
    )

    config_values = {
        "LOOP": LOOP,
        "QBHK": QBHK
    }

    return config_values


# ============================================================
# Create configuration if necessary
# ============================================================

if not os.path.exists(CONFIG_FILE):
    create_config()
    print(
        "No configuration found\n"
        "Configuration file has been created"
    )


config_data = read_config()


# ============================================================
# Hotkey validation
# ============================================================

def is_valid_hotkey(hotkey):

    valid_keys = [
        "ctrl",
        "shift",
        "alt",

        "f1",
        "f2",
        "f3",

        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",

        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",

        "\\",
        "/",
        ",",
        ".",
        "[",
        "]",
        "'",
        "#",
        ";",
        "-"
    ]

    parts = hotkey.lower().split("+")

    return all(
        part.strip() in valid_keys
        for part in parts
    )


# ============================================================
# Hotkey capture
# ============================================================

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

    hotkeybox.delete(
        0,
        END
    )

    hotkeybox.insert(
        0,
        new_hotkey
    )


# ============================================================
# Update hotkey
# ============================================================

def update_hotkey():

    global config_data

    new_hotkey = hotkeybox.get()

    if is_valid_hotkey(new_hotkey):

        try:
            keyboard.remove_hotkey(
                config_data["QBHK"]
            )
        except KeyError:
            pass

        keyboard.add_hotkey(
            new_hotkey,
            QB
        )

        config = cp.ConfigParser()

        config["General"] = {
            "QBHK": new_hotkey,
            "LOOPS": str(
                config_data["LOOP"]
            )
        }

        with open(
            CONFIG_FILE,
            "w"
        ) as configfile:

            config.write(
                configfile
            )

        # Update the in-memory configuration too.
        config_data["QBHK"] = new_hotkey

        feedback_label.config(
            text=f"Hotkey updated to: {new_hotkey}",
            fg="green"
        )

    else:

        feedback_label.config(
            text="Invalid hotkey combination!",
            fg="red"
        )


# ============================================================
# Update loop count
# ============================================================

def update_loops():

    global config_data

    new_loopcount = buycountbox.get()

    # FIXED:
    # "is not" was incorrectly being used for string
    # comparison. Use != instead.
    if new_loopcount != "":

        config = cp.ConfigParser()

        config["General"] = {
            "QBHK": str(
                config_data["QBHK"]
            ),
            "LOOPS": new_loopcount
        }

        with open(
            CONFIG_FILE,
            "w"
        ) as configfile:

            config.write(
                configfile
            )

        # Update the in-memory value as well.
        config_data["LOOP"] = int(
            new_loopcount
        )

        feedback_label.config(
            text=(
                f"Buy count updated to: "
                f"{new_loopcount}"
            ),
            fg="green"
        )

    else:

        feedback_label.config(
            text="Box cannot be empty!",
            fg="red"
        )


# ============================================================
# Integer validation
# ============================================================

def is_integer(char):
    """
    Checks that entered characters are numbers
    and NOT letters.
    """

    return char.isdigit() or char == ""


# ============================================================
# Quick Buy Hotkey
# ============================================================

def QB():

    try:

        current_config = read_config()

        active_window = (
            gw.getActiveWindow()
        )

        if active_window is None:
            return

        if TARGET_WINDOW not in active_window.title:
            return

        mouse_pos = mouse.get_position()

        loop_count = current_config["LOOP"]

        for _ in range(loop_count):

            mouse.hold("right")

            mouse.move(
                300,
                0,
                False,
                0.15
            )

            mouse.release("right")

            mouse.move(
                *mouse_pos,
                True,
                0.15
            )

    except Exception as error:

        # Prevent an exception in the hotkey thread
        # from killing the listener unexpectedly.
        print(
            f"QB error: {error}"
        )


# ============================================================
# Cleanup
# ============================================================

def cleanup():

    """
    Cleanly shut down keyboard/mouse hooks and
    close the application.
    """

    global hotkey_handle

    print(
        "Shutting down NWNHotkeys..."
    )

    # Remove the registered hotkey.
    try:

        if hotkey_handle is not None:

            keyboard.remove_hotkey(
                hotkey_handle
            )

    except Exception:
        pass

    # Remove any remaining keyboard hooks.
    try:
        keyboard.unhook_all()
    except Exception:
        pass

    # Remove any mouse hooks.
    try:
        mouse.unhook_all()
    except Exception:
        pass

    # Finally destroy the Tkinter window.
    try:
        root.destroy()
    except Exception:
        pass


# ============================================================
# Register global hotkey
# ============================================================

hotkey_handle = keyboard.add_hotkey(
    config_data["QBHK"],
    QB
)


# ============================================================
# Tkinter GUI
# ============================================================

root = Tk()

root.title(
    "NWNHotkeys"
)

root.geometry(
    "300x200"
)


# ------------------------------------------------------------
# Hotkey controls
# ------------------------------------------------------------

hotkeylbl = Label(
    root,
    text="Hotkey"
)

hotkeylbl.place(
    x=150,
    y=5
)


hotkeybox = Entry()

hotkeybox.place(
    x=5,
    y=5
)

hotkeybox.insert(
    0,
    config_data["QBHK"]
)

hotkeybox.bind(
    "<Return>",
    lambda event: update_hotkey()
)

hotkeybox.bind(
    "<KeyPress>",
    capture_key
)


# ------------------------------------------------------------
# Feedback
# ------------------------------------------------------------

feedback_label = Label(
    root,
    text=""
)

feedback_label.place(
    x=50,
    y=70
)


# ------------------------------------------------------------
# Buy count validation
# ------------------------------------------------------------

is_int = (
    root.register(is_integer),
    "%S"
)


# ------------------------------------------------------------
# Buy count controls
# ------------------------------------------------------------

buycountlbl = Label(
    root,
    text="Buy Count"
)

buycountlbl.place(
    x=150,
    y=25
)


buycountbox = Entry(
    root,
    validate="key",
    validatecommand=is_int
)

buycountbox.place(
    x=5,
    y=27
)

buycountbox.insert(
    0,
    config_data["LOOP"]
)

buycountbox.bind(
    "<Return>",
    lambda event: update_loops()
)


# ============================================================
# Window close handler
# ============================================================

root.protocol(
    "WM_DELETE_WINDOW",
    cleanup
)


# ============================================================
# Start application
# ============================================================

root.mainloop()