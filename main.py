import time
import threading
from controller import run_controller

# Function to run entire script
def run_script(filename):
    with open(filename, 'r') as file:
        script_content = file.read()
    exec(script_content, globals())

# Create a thread for the controller
controller_thread = threading.Thread(target=run_controller)
# Create a thread for the GUI
gui_thread = threading.Thread(target=run_script, args=("HoopsterGUI.py",))

# Start threads
controller_thread.start()
gui_thread.start()

# Wait for threads to finish
controller_thread.join()
gui_thread.join()