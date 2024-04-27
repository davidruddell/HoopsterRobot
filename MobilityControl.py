from guizero import App, PushButton, Box
import serial
import subprocess
import sys
import serial.tools.list_ports

"""
   Function: run_main_menu
   Purpose: This function calls a subprocess to open the main menu GUI for Hoopster.
"""
def run_main_menu():
    try:
        # Hide Mobility Control Menu
        app.hide()
        app.destroy()
        sys.exit()
        #subprocess.run(['python', 'HoopsterGUI.py'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")

"""
   Function: check_state
   Purpose: This function periodically checks the state of each button. It
   writes to the serial the value for the Arduino code to evaluate and execute.
"""
prev_state = None

def check_state():
    global prev_state

    # Determine the current state
    current_state = None
    if button_up.value:
        current_state = '4', '1'
        print("Move Forward")
    elif button_left.value:
        current_state = '4', '4'
        print("Move Left")
    elif button_right.value:
        current_state = '4', '3'
        print("Move Right")
    elif button_back.value:
        current_state = '4', '2'
        print("Move Backward")
    elif button_fright.value:
        current_state = '4', '7'
        print("Move Forward Right")
    elif button_bright.value:
        current_state = '4', '9'
        print("Move Backward Right")
    elif button_fleft.value:
        current_state = '4', '8'
        print("Move Forward Left")
    elif button_bleft.value:
        current_state = '4', '0'
        print("Move Backward Left")
    elif button_rRight.value:
        current_state = '4', '6'
        print("Rotate Right")
    elif button_rLeft.value:
        current_state = '4', '5'
        print("Rotate Left")
    else:
        current_state = '4', '11'
        print("Stopping")

    # Send data only if the state has changed
    if current_state != prev_state:
        if current_state is not None:
            ser.write(bytes(current_state[0], 'UTF-8'))
            ser.write(bytes(' ', 'UTF-8'))
            ser.write(bytes(current_state[1], 'UTF-8'))
        prev_state = current_state

    app.after(100, check_state)

app = App("Movement Controls", layout="grid", width=1024, height=600)
left_panel = Box(app, layout="grid", grid=[0,0], align="left")
array = Box(app, layout="grid", grid=[1,0])
right_panel = Box(app, layout="grid", grid=[2,0], align="right")

ports = serial.tools.list_ports.comports()
for port in ports:
    ...
try:
    ser = serial.Serial('COM6', 9600)
    print(f"Successfully connected to port {ser.port}.")
except serial.SerialException as e:
    print(f"Error connecting to port: {e}")

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