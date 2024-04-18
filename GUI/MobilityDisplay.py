from guizero import App, PushButton, Picture, Box
import time
import serial
import subprocess
import sys
"""
   Function: run_main_menu
   Purpose: This function calls a subprocess to open the main menu GUI for Hoopster.
"""
def run_main_menu():
    try:
        # Hide Mobility Control Menu
        app.hide()
        sys.exit()
        #subprocess.run(['python', 'HoopsterGUI.py'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")

"""
   Function: check_state
   Purpose: This function periodically checks the state of each button. It
   writes to the serial the value for the Arduino code to evaluate and execute.
"""
def check_state():
    if button_up.value:
        print("Move Forward")
        ser.write(bytes('1', 'UTF-8'))
        app.after(100, check_state)
    elif button_left.value:
        print("Move Left")
        ser.write(bytes('4', 'UTF-8'))
        app.after(100, check_state)
    elif button_right.value:
        print("Move Right")
        ser.write(bytes('3', 'UTF-8'))
        app.after(100, check_state)
    elif button_back.value:
        ser.write(bytes('2', 'UTF-8'))
        print("Move Backward")
        app.after(100, check_state)
    elif button_fright.value:
        ser.write(bytes('7', 'UTF-8'))
        print("Move Forward Right")
        app.after(100, check_state)
    elif button_bright.value:
        ser.write(bytes('9', 'UTF-8'))
        print("Move Backward Right")
        app.after(100, check_state)
    elif button_fleft.value:
        print("Move Forward Left")
        ser.write(bytes('8', 'UTF-8'))
        app.after(100, check_state)
    elif button_bleft.value:
        print("Move Backward Left")
        ser.write(bytes('0', 'UTF-8'))
        app.after(100, check_state)
    elif button_rRight.value:
        print("Rotate Right")
        ser.write(bytes('6', 'UTF-8'))
        app.after(100, check_state)
    elif button_rLeft.value:
        print("Rotate Left")
        ser.write(bytes('5', 'UTF-8'))
        app.after(100, check_state)
    else:
        print("Stopping")
        ser.write(bytes('x', 'UTF-8'))

app = App("Movement Controls", layout="grid", width=1024, height=600)
left_panel = Box(app, layout="grid", grid=[0,0], align="left")
array = Box(app, layout="grid", grid=[1,0])
right_panel = Box(app, layout="grid", grid=[2,0], align="right")

#ser = serial.Serial('COM3', 9600)
try:
    ser = serial.Serial('COM5', 9600)
except:
    print("COM Port not available")
#ser = serial.Serial('/dev/rfcomm0')  # open serial port
#print(ser.name)         # check which port was really used
print("Reset Arduino")
time.sleep(0.5)
#ser.write(bytes('x', 'UTF-8'))

# Load images (replace these with the paths to your image files)
left_arrow_image = "Left.png"
up_arrow_image = "Forward.png"
right_arrow_image = "Right.png"
logo = "Logo1.png"
backward = "Backward.png"
FRight = "ForwardRight.png"
BRight = "BackwardRight.png"
FLeft = "ForwardLeft.png"
BLeft = "BackwardLeft.png"
rotate_right = "RotateRight3.png"
rotate_left = "RotateLeft3.png"

button_left = PushButton(array, image=left_arrow_image, grid=[0, 1], width=195, height=195);
button_up = PushButton(array, image=up_arrow_image, grid=[1, 0], width=195, height=195)
button_right = PushButton(array, image=right_arrow_image, grid=[2, 1], width=195, height=195)
logo = PushButton(array, image=logo, grid=[1, 1], command=run_main_menu, width=195, height=195)
button_back = PushButton(array, image=backward, grid=[1, 2], width=195, height=195)
button_fright = PushButton(array, image=FRight, grid=[2,0], width=195, height=195)
button_bright = PushButton(array, image=BRight, grid=[2,2], width=195, height=195)
button_fleft = PushButton(array, image=FLeft, grid=[0,0], width=195, height=195)
button_bleft = PushButton(array, image=BLeft, grid=[0,2], width=195, height=195)

button_rRight = PushButton(right_panel, image=rotate_right, grid=[3,0],width=205, height=595)
button_rLeft = PushButton(left_panel, image=rotate_left, grid=[3,2],width=205, height=595)

# Register event handlers
#button_logo.when_clicked = check_logo_state
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

