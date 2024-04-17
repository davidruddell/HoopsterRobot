from guizero import App, PushButton, Picture, Box, Slider, TextBox
import time
import serial
import subprocess
import sys
import serial
#import USB_Test_Tx

app = App(title = "Manual Inputs", layout = "grid", bg = (211, 211, 211), width = 1024, height = 600)

#try:
    #ser = serial.Serial('COM5', 9600)
#except:
    #print("COM Port not available")

def run_main_menu():
    try:
        # Hide Mobility Control Menu
        app.hide()
        sys.exit()
        #subprocess.run(['python', 'HoopsterGUI.py'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")

def adjust_hoopster():
    

    print("RPM 1: "+ str(slider.value))
    print("RPM 2: "+ str(slider2.value))
    print("Azimuth: "+ str(slider3.value))
    print("Launch Angle: "+ str(slider4.value))

    #Send serial information/commands representing the values inputted from the slider
    transmitCommand(Command.CHANGE_MOTOR1_RPM, slider.value)
    transmitCommand(Command.CHANGE_MOTOR2_RPM, slider2.value)
    transmitCommand(Command.CHANGE_AZIMUTH, 0, slider3.value)
    transmitCommand(Command.CHANGE_AIM, 0, slider4.value)

    run_main_menu()

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
logo = "Logo.png"
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
logo1 = Picture(array3, grid=[1,0], image = logo, width=160, height = 160)
spacer = Box(array3, grid=[2,0], width = 25, height=25);
adjust = PushButton(array3, command=adjust_hoopster, image = adjust_image, grid = [3,0], width = 600, height= 85)
spacer = Box(array3, grid=[4,0], width = 25, height=25);
logo2 = Picture(array3, grid=[5,0], image = logo, width=160, height = 160)
slider.bg="white"
slider2.bg="white"
slider3.bg="white"
slider4.bg="white"

app.display()