import threading
from pydualsense import *
import serial

# Initialize serial connection
ser = serial.Serial('/xxx/xxx', 9600)

prev_state = None

def check_state(current_state):
    global prev_state
    if current_state != prev_state:
        if current_state is not None:
            ser.write(bytes(current_state[0], 'UTF-8'))
            ser.write(bytes(current_state[1], 'UTF-8'))
        prev_state = current_state

# Define event handlers
def cross_down(state):
    if state:
        current_state = '1', '1'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("Cross")

def square_down(state):
    if state:
        current_state = '2', '2'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("Square")

def triangle_down(state):
    if state:
        current_state = '3', '3'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("Triangle")

def circle_down(state):
    if state:
        current_state = '4', '4'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("Circle")

def dpad_down(state):
    if state:
        current_state = '5', '5'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("Down")

def dpad_left(state):
    if state:
        current_state = '6', '6'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("Left")

def dpad_right(state):
    if state:
        current_state = '7', '7'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("Right")

def dpad_up(state):
    if state:
        current_state = '8', '8'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("Up")

def microphone_down(state):
    if state:
        current_state = '9', '9'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("Microphone")

def options_down(state):
    if state:
        current_state = '10', '10'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("Options")

def share_down(state):
    if state:
        current_state = '11', '11'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("Share")

def ps_down(state):
    if state:
        current_state = '12', '12'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("PS")

def touch_down(state):
    if state:
        current_state = '13', '13'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("Touch")

def r1_down(state):
    if state:
        current_state = '14', '14'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("R1")

action_performed_r2 = False
def r2_down(state):
    global action_performed_r2
    current_state = None
    if state != 0 and not action_performed_r2:
        current_state = '15', '15'  
        print("Pressed")
        action_performed_r2 = True
    elif state == 0:
        current_state = '0', '0'  
        print("Released")
        action_performed_r2 = False
    check_state(current_state)
    
def r3_down(state):
    if state:
        current_state = '16', '16'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("R3")

def l1_down(state):
    if state:
        current_state = '17', '17'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("L1")

action_performed_l2 = False
def l2_down(state):
    global action_performed_l2
    current_state = None
    if state != 0 and not action_performed_l2:
        current_state = '18', '18'  
        print("Pressed")
        action_performed_l2 = True
    elif state == 0:
        current_state = '0', '0'  
        print("Released")
        action_performed_l2 = False
    check_state(current_state)

def l3_down(state):
    if state:
        current_state = '19', '19'  
    else:
        current_state = '0', '0'  
    check_state(current_state)
    print("L3")

def run_controller():
    dualsense = pydualsense()
    dualsense.init()

    # Assign event handlers
    dualsense.cross_pressed += cross_down
    dualsense.circle_pressed += circle_down
    dualsense.triangle_pressed += triangle_down
    dualsense.square_pressed += square_down
    dualsense.dpad_down += dpad_down
    dualsense.dpad_left += dpad_left
    dualsense.dpad_right += dpad_right
    dualsense.dpad_up += dpad_up
    dualsense.microphone_pressed += microphone_down
    dualsense.option_pressed += options_down
    dualsense.share_pressed += share_down
    dualsense.r1_changed += r1_down
    dualsense.r2_changed += r2_down
    dualsense.r3_changed += r3_down
    dualsense.l1_changed += l1_down
    dualsense.l2_changed += l2_down
    dualsense.l3_changed += l3_down
    dualsense.touch_pressed += touch_down
    dualsense.ps_pressed += ps_down

    while True:
        pass  # Keep the loop running or add other logic

    dualsense.close()

# Run the controller directly
if __name__ == "__main__":
    run_controller()
