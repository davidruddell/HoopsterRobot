from guizero import App, PushButton, Picture, Box, Slider, TextBox
import time
import serial
import subprocess
import sys
import struct


# Enumerations for commands
class Command:
    # Receiving
    NO_COMMAND = 0
    DRIVE = 1
    CHANGE_AZIMUTH = 2
    CHANGE_AIM = 3
    CHANGE_MOTOR1_RPM = 4
    CHANGE_MOTOR2_RPM = 5
    LAUNCH = 6
    # Sending
    AZIMUTH_SUCCESS = 7
    AIM_SUCCESS = 8
    MOTOR1_SUCCESS = 9
    MOTOR2_SUCCESS = 10

# Enumerations for states
class State:
    IDLE = 0
    DRIVING = 1
    CHANGING_AZIMUTH = 2
    CHANGING_AIM = 3
    CHANGING_MOTOR1_RPM = 4
    CHANGING_MOTOR2_RPM = 5
    CHECKING_AZIMUTH = 6
    CHECKING_AIM = 7
    CHECKING_MOTOR1_RPM = 8
    CHECKING_MOTOR2_RPM = 9
    LAUNCHING = 10
    ERROR = 11

prev_slider_value = 0
prev_slider2_value = 0
prev_slider3_value = 0
prev_slider4_value = 0

# Define start and end characters
START_CHAR = '<'
END_CHAR = '>'

# Create a serial object
mySerial = serial.Serial('COM6')
mySerial.baudrate = 9600
mySerial.timeout = 0.01
mySerial.bytesize = 8
mySerial.parity = 'N'
mySerial.stopbits = 1

def transmitCommand(command, intArg=0, floatArg=0.0):
    mySerial.write(START_CHAR.encode())
    mySerial.write(struct.pack('B', command))
    if command in [Command.DRIVE, Command.CHANGE_MOTOR1_RPM, Command.CHANGE_MOTOR2_RPM]:
        mySerial.write(struct.pack('h', intArg))
    elif command in [Command.CHANGE_AZIMUTH, Command.CHANGE_AIM]:
        mySerial.write(struct.pack('f', floatArg))
    mySerial.write(END_CHAR.encode())

def transmitCommandDrive(command, intArg1=0, intArg2=0, int8Arg1=0, int8Arg2=0):
    mySerial.write(START_CHAR.encode())
    mySerial.write(struct.pack('B', command))
    mySerial.write(struct.pack('l', intArg1))  # pack as signed long integer
    mySerial.write(struct.pack('l', intArg2))  # pack as unsigned long integer
    mySerial.write(struct.pack('B', int8Arg1))
    mySerial.write(struct.pack('B', int8Arg2))
    mySerial.write(END_CHAR.encode())
    
app = App(title = "Manual Inputs", layout = "grid", bg = (211, 211, 211), width = 1024, height = 600)

def run_main_menu():
    try:
        # Hide Mobility Control Menu
        app.hide()
        sys.exit()
        #subprocess.run(['python', 'HoopsterGUI.py'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")
        
def adjust_hoopster():
    
    global prev_slider_value, prev_slider2_value, prev_slider3_value, prev_slider4_value
    
    print("RPM 1: "+ str(slider.value))
    print("RPM 2: "+ str(slider2.value))
    print("Azimuth: "+ str(slider3.value))
    print("Launch Angle: "+ str(slider4.value))

    # Check if the slider value has changed
    if slider.value != prev_slider_value:
        print("RPM 1: "+ str(slider.value))
        transmitCommand(Command.CHANGE_MOTOR1_RPM, slider.value)
        prev_slider_value = slider.value  # Update the previous value
        time.sleep(2)

    # Repeat for the other sliders
    if slider2.value != prev_slider2_value:
        print("RPM 2: "+ str(slider2.value))
        transmitCommand(Command.CHANGE_MOTOR2_RPM, slider2.value)
        prev_slider2_value = slider2.value
        time.sleep(2)

    if slider3.value != prev_slider3_value:
        print("Azimuth: "+ str(slider3.value))
        transmitCommand(Command.CHANGE_AZIMUTH, 0, slider3.value)
        prev_slider3_value = slider3.value
        time.sleep(2)

    if slider4.value != prev_slider4_value:
        print("Launch Angle: "+ str(slider4.value))
        transmitCommand(Command.CHANGE_AIM, 0, slider4.value)
        prev_slider4_value = slider4.value
        time.sleep(2)
    
    #run_main_menu()

def slider_changed():    
    rpm1_value.value = slider.value
    rpm2_value.value = slider2.value
    azimuth_value.value = slider3.value
    launchAngle_value.value = slider4.value

def update_slider():
    if(rpm1_value.value == ""):
        slider.value=0
    else:
        slider.value = int(rpm1_value.value)
    if(rpm2_value.value == ""):
        slider2.value=0
    else:
        slider2.value = int(rpm2_value.value)
    if(azimuth_value.value == ""):
        slider3.value=0
    else:
        slider3.value = int(azimuth_value.value)
    if(launchAngle_value.value == ""):
        slider4.value=0
    else:
        slider4.value = int(launchAngle_value.value)



array = Box(app, layout="grid", grid=[0,0])
array2 = Box(app, layout="grid", grid=[0,1])
rpm1_image = "rpm1.png"
rpm2_image = "rmp2.png"
azimuth_image = "azimuth.png"
logo = "Logo1.png"
launchAngle_image = "launchAngle.png"
adjust_image = "adjust.png"

spacer = Box(array, grid=[0,0], width = 100, height=50);
rpm1 = Picture(array, image=rpm1_image, grid=[0, 1], width=256, height=100);
spacer = Box(array, grid=[0,2], width = 256, height=100);
rpm2 = Picture(array, image=rpm2_image, grid=[0, 3], width=256, height=100)
spacer = Box(array, grid=[1,1], width = 50, height=100);

slider_array1 = Box(array,layout="grid", grid=[2,1],  height=30)
spacer = Box(slider_array1, grid=[0,1], width = 15, height=15);
rpm1_box = Box(slider_array1, grid = [0,2],border=True, width=156, height=30)
rpm1_value = TextBox(rpm1_box, width = 15, command = update_slider)
rpm1_value.text_size = 14
rpm1_value.bg = "white"
slider_box = Box(slider_array1, grid = [0,0],border=True, width=156, height=60)
slider = Slider(slider_box, width = 156,height=30, end=2000, command= slider_changed)
spacer = Box(array, grid=[3,1], width = 50, height=100);
spacer = Box(array, grid=[1,3], width = 50, height=100);

slider_array2 = Box(array, layout="grid", grid=[2,3],  height=30)
spacer = Box(slider_array2, grid=[0,1], width = 15, height=15);
rpm2_box = Box(slider_array2, grid = [0,2],border=True, width=156, height=30)
rpm2_value = TextBox(rpm2_box, width = 15, command = update_slider)
rpm2_value.text_size = 14
rpm2_value.bg = "white"
slider2_box = Box(slider_array2, grid = [0,0],border=True, width=156, height=60)

slider2 = Slider(slider2_box, width = 156, height=30, end=2000, command= slider_changed)

spacer = Box(array, grid=[3,3], width = 50, height=100);

azimuth = Picture(array, image=azimuth_image,grid=[4,1], width=256, height=100)

launch_angle = Picture(array, image=launchAngle_image,grid=[4,3], width=256, height=100)
spacer = Box(array, grid=[5,1], width = 50, height=100);
slider_array3 = Box(array, layout="grid", grid=[6,1],  height=30)
spacer = Box(slider_array3, grid=[0,1], width = 15, height=15);
azimuth_box = Box(slider_array3, grid = [0,2],border=True, width=156, height=30)

azimuth_value = TextBox(azimuth_box, width = 15, command = update_slider)
azimuth_value.text_size = 14
azimuth_value.bg = "white"
slider3_box = Box(slider_array3, grid = [0,0],border=True, width=156, height=60)

slider3 = Slider(slider3_box, width = 156, height=30, end=180, command= slider_changed)

spacer = Box(array, grid=[5,3], width = 50, height=100);

slider_array4 = Box(array, layout="grid", grid=[6,3])
spacer = Box(slider_array4, grid=[0,1], width = 15, height=15);
launchAngle_box = Box(slider_array4, grid = [0,2],border=True, width=156, height=30)
launchAngle_value = TextBox(launchAngle_box, width = 15, command = update_slider)
launchAngle_value.text_size = 14
launchAngle_value.bg = "white"
slider4_box = Box(slider_array4, grid = [0,0],border=True, width=156, height=60)
slider4 = Slider(slider4_box,  width = 156,height=30, end=90, command= slider_changed)


spacer = Box(array2, grid=[0,0], width = 50, height=55);
array3 = Box(array2, grid=[0,1], layout="grid", width = 1024, height = 200)
spacer = Box(array3, grid=[0,0], width = 25, height=25);
logo1 = Picture(array3, grid=[1,0], image = logo)
spacer = Box(array3, grid=[2,0], width = 25, height=25);
adjust = PushButton(array3, command=adjust_hoopster, image = adjust_image, grid = [3,0], width = 600, height= 85)
spacer = Box(array3, grid=[4,0], width = 25, height=25);
logo2 = Picture(array3, grid=[5,0], image = logo)
slider.bg="white"
slider2.bg="white"
slider3.bg="white"
slider4.bg="white"

app.display()