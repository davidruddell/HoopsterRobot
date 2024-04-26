# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import sys
print(sys.version)
import subprocess
import cv2
from guizero import App, Text, Picture, PushButton, Box, Window
from PIL import Image, ImageTk

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from calculations import calculate_manual
import math
from CV2 import cvMain

# Global variables
SUCCESS = 0
FAILURE = 0
TOTAL = 0
SUCCESS_RATE = 0.0
COUNTDOWN = 5
SET_TRIGGER = False
LAUNCHED = False
X_GOAL = 0
HYPOTENUSE = 0
RPM = [0,0]
THETA_RESULT = 0
THETA_DEGREES = 0
V_RESULT = 0

AZIMUTH_CAL=0.00
LAUNCH_ANG_CAL=0.00
VELOCITY_CAL=0.00

TRAJ_BOX_EXISTS = False
CAL_BOX_EXISTS = False


global graph_box, cal_box
global mobility_gui
mobility_gui = None

#global cap, live_feed

# Function to update the video feed frame
def update_frame():
    ret, frame = cap.read()
    frame = cv2.resize(frame, (round(3840*0.346), round(2160*0.358)))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame)
    tk_image = ImageTk.PhotoImage(image)
    live_feed.image = tk_image
    live_feed.after(1, update_frame)

# Function to handle closing the app
def on_closed(event=None):
    try:
        app.destroy()
    except Exception as e:
        # print(f"Error occurred: {e}")
        print("Error occurred")
        
# Function to handle a successful shot
def success_shot():
    global SUCCESS, TOTAL
    SUCCESS += 1
    TOTAL += 1
    app.show()
    launched_window.hide()
    update_stats()
    abort_launch()

# Function to handle a failed shot
def fail_shot():
    global FAILURE, TOTAL
    FAILURE += 1
    TOTAL += 1
    app.show()
    launched_window.hide()
    update_stats()
    abort_launch()

# Function to run the MobilityDisplay script
# def run_mobility_menu():
#     try:
#         app.hide()
#         process = subprocess.Popen(['python', 'MobilityDisplay.py'])
#         process.wait()
#         print("Parent script continues running...")
#         app.show()
#     except subprocess.CalledProcessError as e:
#         print(f"Error running the script: {e}")

def run_mobility_menu():
    global mobility_gui
    try:
        app.hide()
        if mobility_gui is None:
            # Create the GUI only once
            mobility_gui = subprocess.Popen(['python', 'MobilityDisplay.py'])
        else:
            # If the GUI already exists, just show it
            mobility_gui.show()
    except Exception as e:
        # print(f"Error running the script: {e}")
        print("Error occurred")
    finally:
        app.show()

# Function to run the ManualDisplay script
def run_manual_shot_menu():
    try:
        app.hide()
        process = subprocess.Popen(['python', 'ManualDisplay.py'])
        process.wait()
        print("Parent script continues running...")
        app.show()
    except subprocess.CalledProcessError as e:
        # print(f"Error running the script: {e}")
        print("Error occurred")



def run_trajectory_screen():
    global TRAJ_BOX_EXISTS, CAL_BOX_EXISTS, graph_box, cal_box, THETA_DEGREES, V_RESULT
    
    x, y, center = calculate_manual(THETA_DEGREES, V_RESULT)

    if TRAJ_BOX_EXISTS == True:
        graph_box.destroy()
    if CAL_BOX_EXISTS == True:
        cal_box.destroy()

    graph_box = Box(box1, layout="grid", grid=[0, 0], width=1, height=1, align="left")
    figure = Figure(figsize=(8.35, 4.85), dpi=160)
    canvas = FigureCanvasTkAgg(figure, master=graph_box.tk)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    canvas.figure.clear()

    ax = canvas.figure.add_subplot(111)
    ax.plot(x, y, color='#ff8c00', linewidth=2)  # Change line color and thickness
    ax.set_title('Trajectory', color='white', fontsize=16, fontweight='bold')  # Change title color, size, and weight
    ax.set_xlabel('x [m]', color='#cccccc', fontsize=15)  # Change X-label color and size
    ax.set_ylabel('y [m]', color='#cccccc', fontsize=15)  # Change Y-label color and size
    ax.errorbar([center], [3.05], xerr=[0.2286], ecolor="orange")
    distance = center
    
    # Set the x and y axis limits
    ax.set_xlim([0, 8])
    ax.set_ylim([0, 6])
    
    plt.tight_layout()

    # Set background color
    canvas.figure.patch.set_facecolor('#2b2b2b')
    ax.set_facecolor('#2b2b2b')

    # Set grid lines
    ax.grid(color='#444444', linestyle='--', linewidth=0.5)

    # Set tick colors
    ax.tick_params(axis='x', colors='#cccccc', labelsize=16)
    ax.tick_params(axis='y', colors='#cccccc', labelsize=16)
    
    ax.set

    canvas.draw()
    TRAJ_BOX_EXISTS = True
    CAL_BOX_EXISTS = False

def run_camera_screen():
    global TRAJ_BOX_EXISTS, CAL_BOX_EXISTS, graph_box, cal_box
    # Check if graph_box already exists
    if TRAJ_BOX_EXISTS == True:
        graph_box.destroy()
    if CAL_BOX_EXISTS == True:
        cal_box.destroy()
    
    TRAJ_BOX_EXISTS = False
    CAL_BOX_EXISTS = False

def run_calibration_screen():
    global TRAJ_BOX_EXISTS, CAL_BOX_EXISTS, cal_box, graph_box, AZIMUTH_CAL, LAUNCH_ANG_CAL, VELOCITY_CAL, velocity_cal_text, azimuth_cal_text, launch_angle_cal_text

    try:
        if TRAJ_BOX_EXISTS == True:
            graph_box.destroy()
        if CAL_BOX_EXISTS == True:
            cal_box.destroy()
        # clear all the elements from main_func_box so it is ready for the change in screend
        cal_box = Box(box1, layout="grid", grid=[0, 0], width=round(3840*0.346), height=round(2160*0.358))

        launch_angle_cal_box = Box(cal_box, layout="grid", grid=[0, 0], width=1, height=1, align="top")
        launchAngle_cal_image = Picture(launch_angle_cal_box, image="GUI/AngleLabel.png", grid=[0, 0], width=300, height=100)
        launchAngle_cal_add_button = PushButton(launch_angle_cal_box, text="+", command=launchAngle_plusCal, grid=[3, 0])
        launch_angle_cal_text = Text(launch_angle_cal_box, text=LAUNCH_ANG_CAL, grid=[2, 0], color="white")
        launch_angle_subtract_button = PushButton(launch_angle_cal_box, text="-", command=launchAngle_minusCal, grid=[1, 0])

        spacer_cal1 = Box(cal_box, layout="grid", grid=[0, 1], width=1, height=100, align="top")

        azimuth_box = Box(cal_box, layout="grid", grid=[0, 4], width=1, height=1, align="top")
        azimuth_image = Picture(azimuth_box, image="GUI/AzimuthLabel.png", grid=[0, 0], width=300, height=100)
        azimuth_add_button = PushButton(azimuth_box, text="+", command=azimuth_plusCal, grid=[3, 0])
        azimuth_cal_text = Text(azimuth_box, text=AZIMUTH_CAL, grid=[2, 0], color="white")
        azimuth_subtract_button = PushButton(azimuth_box, text="-", command=azimuth_minusCal, grid=[1, 0])

        spacer_cal2 = Box(cal_box, layout="grid", grid=[0, 3], width=1, height=100, align="top")

        velocity_cal_box = Box(cal_box, layout="grid", grid=[0, 2], width=1, height=1, align="top")
        velocity_cal_image = Picture(velocity_cal_box, image="GUI/VelocityLabel.png", grid=[0, 0], width=300, height=100)
        velocity_cal_add_button = PushButton(velocity_cal_box, text="+", command=velocity_plusCal, grid=[3, 0])
        velocity_cal_text = Text(velocity_cal_box, text=str(VELOCITY_CAL), grid=[2, 0], color="white")
        velocity_cal_subtract_button = PushButton(velocity_cal_box, text="-", command=velocity_minusCal, grid=[1, 0])

        spacer_cal3 = Box(cal_box, layout="grid", grid=[0, 5], width=1, height=100, align="top")

        apply_cal_button = PushButton(cal_box, text="Apply", image="GUI/Apply.png", command=apply_cal_press, grid=[0, 6], width=600, height=100)

        spacer_cal4 = Box(cal_box, layout="grid", grid=[0, 7], width=1, height=100, align="top")

        CAL_BOX_EXISTS = True
        TRAJ_BOX_EXISTS = False

    except subprocess.CalledProcessError as e:
        # print(f"Error running the script: {e}")
        print("Error occurred")

def launchAngle_plusCal():
    global LAUNCH_ANG_CAL, launch_angle_cal_text
    LAUNCH_ANG_CAL += 0.1
    LAUNCH_ANG_CAL = round(LAUNCH_ANG_CAL, 1)
    launch_angle_cal_text.value = str(LAUNCH_ANG_CAL)

def launchAngle_minusCal():
    global LAUNCH_ANG_CAL
    LAUNCH_ANG_CAL -= 0.1
    LAUNCH_ANG_CAL = round(LAUNCH_ANG_CAL, 1)
    launch_angle_cal_text.value = str(LAUNCH_ANG_CAL)

def azimuth_plusCal():
    global AZIMUTH_CAL, azimuth_cal_text
    AZIMUTH_CAL += 0.1
    AZIMUTH_CAL = round(AZIMUTH_CAL, 1)
    azimuth_cal_text.value = str(AZIMUTH_CAL)

def azimuth_minusCal():
    global AZIMUTH_CAL, azimuth_cal_text
    AZIMUTH_CAL -= 0.1
    AZIMUTH_CAL = round(AZIMUTH_CAL, 1)
    azimuth_cal_text.value = str(AZIMUTH_CAL)

def velocity_plusCal():
    global VELOCITY_CAL, velocity_cal_text
    VELOCITY_CAL += 0.1
    VELOCITY_CAL = round(VELOCITY_CAL, 1)
    velocity_cal_text.value = str(VELOCITY_CAL)

def velocity_minusCal():
    global VELOCITY_CAL, velocity_cal_text
    VELOCITY_CAL -= 0.1
    VELOCITY_CAL = round(VELOCITY_CAL, 1)
    velocity_cal_text.value = str(VELOCITY_CAL)

def apply_cal_press():
    global cal_box, CAL_BOX_EXISTS
    
    cal_box.destroy()

    angCal_lab.clear()
    velCal_lab.clear()
    azimuthCal_lab.clear()

    angCal_lab.append("Launch Angle: " + str(cal_symbol(LAUNCH_ANG_CAL)) + str(LAUNCH_ANG_CAL) + "°")
    velCal_lab.append("Velocity: " + str(cal_symbol(VELOCITY_CAL)) + str(VELOCITY_CAL) + "m/s")
    azimuthCal_lab.append("Azimuth: " + str(cal_symbol(AZIMUTH_CAL))  + str(AZIMUTH_CAL) + "°")

    CAL_BOX_EXISTS = False

def cal_symbol(x):
    if x < 0:
        return "-"
    else:
        return "+"

# Function to start the launch countdown
def launch_countdown():
    if SET_TRIGGER and launch_button.enabled:
        countdown_window.show()
        app.hide()
        countdown_window.repeat(1000, update_timer)
        print("Starting launch countdown...")
    else:
        print("Error: Not ready for launch. Set Hoopster first.")

#40.3 in+1.75
# Function to launch the basketball
def launch():
    global LAUNCHED

    if SET_TRIGGER and launch_button.enabled:
        print("Launching Basketball")
        LAUNCHED = True
        countdown_window.show()
        app.hide()
    else:
        print("Not ready for launch. Set Hoopster first.")

# Function to check if ready for launch
def launch_ready():
    if anom.value == 0:
        print("Ready for Launch...")

#convert radians to degrees
def radians_to_degrees(radians):
    degrees = radians * (180.0 / math.pi)
    return degrees

# Function to prepare for launch
def set_launch():
    global SET_TRIGGER, X_GOAL, HYPOTENUSE, RPM, THETA_RESULT, V_RESULT, TRAJ_BOX_EXISTS, THETA_DEGREES, CAL_BOX_EXISTS

    print("Preparing for launch")
    SET_TRIGGER = True

    # dis_lab.clear()
    # ang_lab.clear()
    # vel_lab.clear()

    # dis_lab.append("Distance: 4.2 m")
    # ang_lab.append("Launch Angle: 65 deg")
    # vel_lab.append("Velocity: 8.35 m/s")

    # with open("CV2/cvMain.py") as file:
    #     result = exec(file.read())

    # what is X_GOAL?
    (result, X_GOAL, HYPOTENUSE, RPM) = cvMain.main()


    #if hoop not found
    if (HYPOTENUSE == -1):
        dis_lab.clear()
        disx_lab.clear()
        ang_lab.clear()
        vel_lab.clear()
        rpm1_lab.clear()
        rpm2_lab.clear()

        dis_lab.append("No Hoop Detected")
        return
    #if calculation is not possible
    if (HYPOTENUSE == -2):
        dis_lab.clear()
        disx_lab.clear()
        ang_lab.clear()
        vel_lab.clear()
        rpm1_lab.clear()
        rpm2_lab.clear()
        dis_lab.append("Shot Not Possible")
        return

    x_result, y_result, THETA_RESULT, V_RESULT = result
    
    THETA_DEGREES = radians_to_degrees(THETA_RESULT)

    if TRAJ_BOX_EXISTS == True:
        run_trajectory_screen()

    dis_lab.clear()
    disx_lab.clear()
    ang_lab.clear()
    vel_lab.clear()
    rpm1_lab.clear()
    rpm2_lab.clear()

    formatted_hypot = format(HYPOTENUSE, '.2f')
    formatted_x_goal = format(X_GOAL, '.2f')
    formatted_theta_result = format(THETA_DEGREES, '.2f')
    formatted_v_result = format(V_RESULT, '.2f')
    formatted_rpm1 = format(RPM[0], '.2f')
    formatted_rpm2 = format(RPM[1], '.2f')

    dis_lab.append("Distance: " + str(formatted_hypot) + "m")
    disx_lab.append("X-Axis Distance: " + str(formatted_x_goal) + "m")
    ang_lab.append("Launch Angle: " + str(formatted_theta_result) + "°")
    vel_lab.append("Velocity: " + str(formatted_v_result) + "m/s")
    rpm1_lab.append("RPM Front Wheels: " + str(formatted_rpm1))
    rpm2_lab.append("RPM Rear Wheels: " + str(formatted_rpm2))

    hoop_status.image = "GUI/Check.png"
    pos_status.image = "GUI/Check.png"
    dis_status.image = "GUI/Check.png"
    ang_status.image = "GUI/Check.png"
    vel_status.image = "GUI/Check.png"
    anom_status.image = "GUI/NotCheck.png"
    launch_button.enabled = True
    print("Ready for launch")

# Function to abort the launch process
def abort_launch():
    global LAUNCHED
    if not LAUNCHED:
        print("Launch Aborted.")

    dis_lab.clear()
    disx_lab.clear()
    ang_lab.clear()
    vel_lab.clear()
    rpm1_lab.clear()
    rpm2_lab.clear()

    dis_lab.append("Distance: ")
    disx_lab.append("X-Axis Distance: ")
    ang_lab.append("Launch Angle: ")
    vel_lab.append("Velocity: ")
    rpm1_lab.append("RPM Front Wheels: ")
    rpm2_lab.append("RPM Rear Wheels: ")

    hoop_status.image = "GUI/NotCheck.png"
    pos_status.image = "GUI/NotCheck.png"
    dis_status.image = "GUI/NotCheck.png"
    ang_status.image = "GUI/NotCheck.png"
    vel_status.image = "GUI/NotCheck.png"
    anom_status.image = "GUI/NotCheck.png"
    launch_button.enabled = False

# Function to abort the launch countdown
def abort_countdown():
    global COUNTDOWN
    app.cancel(update_timer)
    app.show()
    clock_dis.value = "5"
    COUNTDOWN = 5
    countdown_window.hide()
    abort_launch()

# Function to detect anomalies (placeholder)
def detect_anomaly():
    #anom_status.image = "GUI/Check.png"
    return 0

# Function to calculate the success rate
def calc_success_rate():
    global SUCCESS_RATE
    if TOTAL != 0:
        SUCCESS_RATE = (SUCCESS / TOTAL) * 100
    else:
        SUCCESS_RATE = 0
    return round(SUCCESS_RATE, 2)

# Function to reset statistics
def reset_stats():
    global SUCCESS, FAILURE, TOTAL, SUCCESS_RATE
    SUCCESS = 0
    FAILURE = 0
    TOTAL = 0
    SUCCESS_RATE = 0
    update_stats()

# Function to update the timer
def update_timer():
    global COUNTDOWN
    COUNTDOWN -= 1
    clock_dis.value = str(COUNTDOWN)
    if COUNTDOWN == 0:
        launch()
        app.cancel(update_timer)
        clock_dis.value = "5"
        COUNTDOWN = 5
        launched_window.show()
        countdown_window.hide()

# Function to update the statistics display
def update_stats():
    successes.clear()
    failures.clear()
    rate.clear()
    successes.append("Successes: " + str(SUCCESS))
    failures.append("Failures: " + str(FAILURE))
    rate.append("Success Rate: " + str(calc_success_rate()) + "%")


def calculate_velocity(rW, rB, wC, wA):
    omega_B = (rW / (2 * rB)) * (wC - wA)
    v_B = (rW / 2) * (wC + wA)
    return v_B, omega_B


# Initialize the video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(3, 3840)
cap.set(4, 2160)

# Create the main application window
app = App(title="Hoopster", layout="grid", bg="#2b2b2b", width=1920, height=1080)
app.font = "Arial Black"
app.text_size = 16
app.set_full_screen()

# Create the launched window
launched_window = Window(app, title="Launching", layout="grid", bg="#2b2b2b", width=1920, height=1080, visible=False)
launched_window.font = "Arial Black"
launched_window.text_size = 16
launched_window.set_full_screen()

# Set up the launched window UI
box_lw = Box(launched_window, layout="grid", grid=[0, 0], align="top")
center_lw = Box(box_lw, layout="grid", grid=[1, 1], align="top")
dummy_lw0 = Text(box_lw, grid=[0, 0], text="", width=16, height=16, color="#c0c0c0", bg="#2b2b2b")
gif = Picture(box_lw, image="GUI/swish.gif", width=620*2, height=420*2, grid=[1, 0])
dummy_lw1 = Text(box_lw, grid=[0, 0], text="", width=1, height=1, color="#c0c0c0", bg="#2b2b2b")

success_button = PushButton(center_lw, image="GUI/Success.png", width=200*3, height=200, grid=[1, 0], command=success_shot)
buffer = Box(center_lw, height=30, width=30, grid=[2, 0])
failure_button = PushButton(center_lw, image="GUI/Fail.png", width=200*3, height=200, grid=[3, 0], command=fail_shot)

# Create the countdown window
countdown_window = Window(app, title="Countdown", layout="grid", bg="#2b2b2b", width=1920, height=1080, visible=False)
countdown_window.font = "Arial Black"
countdown_window.text_size = 16
#countdown_window.set_full_screen()

# Set up the countdown window UI
box_cd = Box(countdown_window, layout="grid", grid=[0, 0], align="top")
dummy_cd0 = Text(box_cd, grid=[0, 0], text="", width=1, height=1, color="#c0c0c0", bg="#2b2b2b")
title_cd = Text(box_cd, grid=[1, 0], text="Backup from Hoopster", align="top", size=100, color="#ff8c00", font="Arial Black", bg="#2b2b2b")
dummy_cd1 = Text(box_cd, grid=[2, 0], text="", width=1, height=1, color="#c0c0c0", bg="#2b2b2b")
clock_dis = Text(box_cd, text="5", grid=[1, 1], size=300, align="top", color="#ff8c00", bg="#2b2b2b")
abort_button = PushButton(box_cd, text="Abort", image="GUI/AbortButton.png", command=abort_countdown, grid=[1, 2], align="top", width=175*3, height=175)

# Set up the main window UI
box1 = Box(app, layout="grid", grid=[0, 0], align="top", border=False, width=1, height=1)
box2 = Box(app, layout="grid", grid=[1, 0], align="top", border=False, width=350, height=1)
box3 = Box(app, layout="grid", grid=[0, 1], align="top", border=False, width=1, height=1)
box4 = Box(app, layout="grid", grid=[1, 1], align="top", border=False, width=350, height=350)

row0 = Box(box2, layout="grid", grid=[0, 1], align="left", border=False)
row1 = Box(box2, layout="grid", grid=[0, 2], align="left", border=False)
row2 = Box(box2, layout="grid", grid=[0, 3], align="left", border=False)
row3 = Box(box2, layout="grid", grid=[0, 4], align="left", border=False)
row4 = Box(box2, layout="grid", grid=[0, 5], align="left", border=False)
row5 = Box(box2, layout="grid", grid=[0, 6], align="left", border=False)
row6 = Box(box2, layout="grid", grid=[0, 7], align="left", border=False)
row7 = Box(box2, layout="grid", grid=[0, 8], align="left", border=False)
row8 = Box(box2, layout="grid", grid=[0, 9], align="left", border=False)
row9 = Box(box2, layout="grid", grid=[0, 10], align="left", border=False)
row10 = Box(box2, layout="grid", grid=[0, 11], align="left", border=False)
row11 = Box(box2, layout="grid", grid=[0, 12], align="left", border=False)
row12 = Box(box2, layout="grid", grid=[0, 13], align="left", border=False)
row13 = Box(box2, layout="grid", grid=[0, 14], align="left", border=False)
row14 = Box(box2, layout="grid", grid=[0, 15], align="left", border=False)
row15 = Box(box2, layout="grid", grid=[0, 16], align="left", border=False)
row16 = Box(box2, layout="grid", grid=[0, 17], align="left", border=False)
row17 = Box(box2, layout="grid", grid=[0, 18], align="left", border=False)
row18 = Box(box2, layout="grid", grid=[0, 19], align="left", border=False)
row19 = Box(box2, layout="grid", grid=[0, 20], align="left", border=False)
row20 = Box(box2, layout="grid", grid=[0, 21], align="left", border=False)
row21 = Box(box4, layout="grid", grid=[0, 22], align="left", border=False)
row22 = Box(box4, layout="grid", grid=[0, 23], align="left", border=False)
row23 = Box(box4, layout="grid", grid=[0, 24], align="left", border=False)
row24 = Box(box4, layout="grid", grid=[0, 25], align="left", border=False)
row25 = Box(box4, layout="grid", grid=[0, 26], align="left", border=False)

live_feed = Picture(box1, grid=[0, 0], align="top")
update_frame()

# Set up status indicators
hoop_status = Picture(row1, image="GUI/NotCheck.png", grid=[0, 0], width=45, height=45, align="left")
pos_status = Picture(row2, image="GUI/NotCheck.png", grid=[0, 0], width=45, height=45, align="left")
dis_status = Picture(row3, image="GUI/NotCheck.png", grid=[0, 0], width=45, height=45, align="left")
ang_status = Picture(row4, image="GUI/NotCheck.png", grid=[0, 0], width=45, height=45, align="left")
vel_status = Picture(row5, image="GUI/NotCheck.png", grid=[0, 0], width=45, height=45, align="left")
anom_status = Picture(row6, image="GUI/NotCheck.png", grid=[0, 0], width=45, height=45, align="left")

# Set up text labels
verification = Text(row0, grid=[0, 0], text="Verification", align="top", size=39, color="#ff8c00", font="Arial Black", bg="#2b2b2b")
hoop = Text(row1, grid=[1, 0], text="HOOP DETECTED", align="left", color="#c0c0c0", bg="#2b2b2b")
pos = Text(row2, grid=[1, 0], text="POSITION SET", align="left", color="#c0c0c0", bg="#2b2b2b")
dis = Text(row3, grid=[1, 0], text="DISTANCE CALCULATED", align="left", color="#c0c0c0", bg="#2b2b2b")
ang = Text(row4, grid=[1, 0], text="ANGLE CALCULATED", align="left", color="#c0c0c0", bg="#2b2b2b")
vel = Text(row5, grid=[1, 0], text="VELOCITY CALCULATED", align="left", color="#c0c0c0", bg="#2b2b2b")
anom = Text(row6, grid=[1, 0], text="ANOMALY DETECTED", align="left", color="#c0c0c0", bg="#2b2b2b")

padding1 = PushButton(box3, image="GUI/SetButton.png", grid=[0, 0], width=269, height=125, visible=False)

prepare_launch_button = PushButton(box3, text="Prepare for Launch", image="GUI/SetButton.png", command=set_launch, grid=[1, 0], align="top", width=269, height=125)

launch_button = PushButton(box3, text="Start Launch", image="GUI/LaunchButton.png", command=launch_countdown, grid=[2, 0], align="top", width=269, height=125, enabled=False)

abort_button = PushButton(box3, text="Stop Launch", image="GUI/AbortButton.png", command=abort_launch, grid=[3, 0], align="top", width=269, height=125)

dummy_button0 = PushButton(box3, text="Camera", image="GUI/CameraButton.png", command=run_camera_screen, grid=[0, 2], align="top", width=230, height=100)
dummy_padding0 = Picture(box3, grid=[0, 1], width=0, height=0)
dummy_button0.bg = "white"

dummy_button1 = PushButton(box3, text="Mobility Control", image="GUI/MobilityControlButton.png", command=run_mobility_menu, grid=[2, 2], align="top", width=230, height=100)
dummy_padding1 = Picture(box3, grid=[1, 1], width=0, height=0)
dummy_button1.bg = "white"

dummy_button2 = PushButton(box3, text="Trajectory", image="GUI/TrajectoryButton.png", command=run_trajectory_screen, grid=[1, 2], align="top", width=230, height=100)
dummy_padding3 = Picture(box3, grid=[2, 1], width=0, height=0)
dummy_button2.bg = "white"

dummy_button3 = PushButton(box3, text="Manual Shot", image="GUI/ManualButton.png", command=run_manual_shot_menu, grid=[3, 2], align="top", width=230, height=100)
dummy_padding3 = Picture(box3, grid=[3, 1], width=0, height=0)
dummy_button3.bg = "white"

dummy_button4 = PushButton(box3, text="Shot Calibration", image="GUI/CalibrationButton.png", command=run_calibration_screen, grid=[4, 2], align="top", width=230, height=100)
dummy_padding4 = Picture(box3, grid=[4, 1], width=0, height=0)
dummy_button4.bg = "white"

# dummy1 = Text(row7, grid=[0, 0], text="", align="left", bg="#2b2b2b", color="#c0c0c0")
# dummy2 = Text(row8, grid=[0, 0], text="", align="left", bg="#2b2b2b", color="#c0c0c0")
# dummy3 = Text(row9, grid=[0, 0], text="", align="left", bg="#2b2b2b", color="#c0c0c0")

# FIXME: to be checked; diatance = distance to the the hoop; x distance = x intercept
title_lab = Text(row7, grid=[0, 0], text="Parameters", align="top", size=39, color="#ff8c00", font="Arial Black", bg="#2b2b2b")
dis_lab = Text(row8, grid=[0, 0], text="Distance: ", align="left", color="#c0c0c0", bg="#2b2b2b")
disx_lab = Text(row9, grid=[0, 0], text="X-Axis Distance: ", align="left", color="#c0c0c0", bg="#2b2b2b")
ang_lab = Text(row10, grid=[0, 0], text="Launch Angle: ", align="left", color="#c0c0c0", bg="#2b2b2b")
vel_lab = Text(row11, grid=[0, 0], text="Velocity: ", align="left", color="#c0c0c0", bg="#2b2b2b")
rpm1_lab = Text(row12, grid=[0, 0], text="RPM Front Wheels: ", align="left", color="#c0c0c0", bg="#2b2b2b")
rpm2_lab = Text(row13, grid=[0, 0], text="RPM Rear Wheels: ", align="left", color="#c0c0c0", bg="#2b2b2b")

parameters_lab = Text(row17, grid=[0, 0], text="Calibration", align="top", size=39, color="#ff8c00", font="Arial Black", bg="#2b2b2b")
angCal_lab = Text(row18, grid=[0, 0], text="Launch Angle: +0.0°", align="left", color="#c0c0c0", bg="#2b2b2b")
velCal_lab = Text(row19, grid=[0, 0], text="Velocity: +0.0m/s", align="left", color="#c0c0c0", bg="#2b2b2b")
azimuthCal_lab = Text(row20, grid=[0, 0], text="Azimuth: +0.0°", align="left", color="#c0c0c0", bg="#2b2b2b")


stats = Text(box4, grid=[0, 0], text="Statistics", align="top", size=39, color="#ff8c00", font="Arial Black", bg="#2b2b2b")
successes = Text(box4, grid=[0, 1], text="Successes: " + str(SUCCESS), align="left", color="#c0c0c0", bg="#2b2b2b")
failures = Text(box4, grid=[0, 2], text="Failures: " + str(FAILURE), align="left", color="#c0c0c0", bg="#2b2b2b")
rate = Text(box4, grid=[0, 3], text="Success Rate: " + str(calc_success_rate()) + "%", align="left", color="#c0c0c0", bg="#2b2b2b")
reset_button = PushButton(box4, grid=[0, 5], image="GUI/ResetButton.png", text="Reset Statistics", align="left", width=340, height=60, command=reset_stats)

# Repeat function calls
app.repeat(1000, detect_anomaly)

# Close the app
app.when_closed = on_closed

# Start the application
app.display()