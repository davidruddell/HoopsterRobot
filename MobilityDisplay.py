from guizero import App, PushButton, Box
import subprocess
import time
import serial
import sys

def run_main_menu():
    """This function calls a subprocess to open the main menu GUI for Hoopster."""
    try:
        app.hide()
        #app.destroy()
    except Exception as e:
        print(f"Error running the script: {e}")

def check_state():
    """This function periodically checks the state of each button. It writes to the serial the value for the Arduino code to evaluate and execute."""
    button_values = {
        button_up: ('1', "Move Forward"),
        button_left: ('4', "Move Left"),
        button_right: ('3', "Move Right"),
        button_back: ('2', "Move Backward"),
        button_fright: ('7', "Move Forward Right"),
        button_bright: ('9', "Move Backward Right"),
        button_fleft: ('8', "Move Forward Left"),
        button_bleft: ('0', "Move Backward Left"),
        button_rRight: ('6', "Rotate Right"),
        button_rLeft: ('5', "Rotate Left")
    }
    
    for button, (value, message) in button_values.items():
        if button.value:
            print(message)
            ser.write(bytes(value, 'UTF-8'))
            app.after(100, check_state)
            return

    print("Stopping")
    ser.write(bytes('x', 'UTF-8'))


app = App("Movement Controls", layout="grid", width=1920, height=1080, bg="#2b2b2b")
app.set_full_screen()

left_panel = Box(app, layout="grid", grid=[0,0], align="left")
array = Box(app, layout="grid", grid=[1,0])
right_panel = Box(app, layout="grid", grid=[2,0], align="right")

try:
    ser = serial.Serial('COM5', 9600)
except:
    print("COM Port not available")

print("Reset Arduino")
time.sleep(0.5)

# Load images (replace these with the paths to your image files)
image_paths = {
    "left_arrow": "GUI/Left.png",
    "up_arrow": "GUI/Forward.png",
    "right_arrow": "GUI/Right.png",
    "logo": "GUI/Logo1.png",
    "backward": "GUI/Backward.png",
    "FRight": "GUI/ForwardRight.png",
    "BRight": "GUI/BackwardRight.png",
    "FLeft": "GUI/ForwardLeft.png",
    "BLeft": "GUI/BackwardLeft.png",
    "rotate_right": "GUI/RotateRight3.png",
    "rotate_left": "GUI/RotateLeft3.png"
}

button_left = PushButton(array, image=image_paths["left_arrow"], grid=[0, 1], width=343, height=343)
button_up = PushButton(array, image=image_paths["up_arrow"], grid=[1, 0], width=343, height=343)
button_right = PushButton(array, image=image_paths["right_arrow"], grid=[2, 1], width=343, height=343)
logo = PushButton(array, image=image_paths["logo"], grid=[1, 1], command=run_main_menu, width=343, height=343)
button_back = PushButton(array, image=image_paths["backward"], grid=[1, 2], width=343, height=343)
button_fright = PushButton(array, image=image_paths["FRight"], grid=[2,0], width=343, height=343)
button_bright = PushButton(array, image=image_paths["BRight"], grid=[2,2], width=343, height=343)
button_fleft = PushButton(array, image=image_paths["FLeft"], grid=[0,0], width=343, height=343)
button_bleft = PushButton(array, image=image_paths["BLeft"], grid=[0,2], width=343, height=343)

button_rRight = PushButton(right_panel, image=image_paths["rotate_right"], grid=[3,0],width=310, height=1045)
button_rLeft = PushButton(left_panel, image=image_paths["rotate_left"], grid=[3,2],width=310, height=1045)

# Register event handlers
button_up.when_clicked = check_state
button_left.when_clicked = check_state
button_right.when_clicked = check_state
button_back.when_clicked = check_state
button_fright.when_clicked = check_state
button_bright.when_clicked = check_state
button_fleft.when_clicked = check_state
button_bleft.when_clicked = check_state
button_rRight.when_clicked = check_state
button_rLeft.when_clicked = check_state

app.display()