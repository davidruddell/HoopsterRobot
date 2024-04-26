# -*- coding: utf-8 -*-

import sys
import math
import subprocess
import numpy as np
from guizero import App, PushButton, Picture, Box, Slider, TextBox, Text
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from calculations import calculate_manual

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
BACKGROUND_COLOR = "#2b2b2b"
SLIDER_MAX_RPM = 2000
SLIDER_MAX_AZIMUTH = 180
SLIDER_MAX_LAUNCH_ANGLE = 90
SLIDER_COLOR = "#4da6ff"
SLIDER_HANDLE_COLOR = "#ffffff"
global velocity
global distance
distance = 0
velocity = 0

def calculate_velocity(rW, rB, wC, wA):
    '''
    Calculates the linear and angular velocities of the basketball.

    rW: raidus of the wheels FIXME: is this right
    rB: radius of the basketball
    wC: angualr velocity of the first pair of wheels FIXME: is this right?
    wA: angulart velocity of the second pair of wheels

    return: array [linear velocity, angular velocity]
    '''
    omega_B = (rW / (2 * rB)) * (wC - wA)
    v_B = (rW / 2) * (wC + wA)

    return v_B, omega_B

def change_parameters(distance):
    '''
    Populates the parameters section of the GUI. Gets values from the different sliders.

    returns: the distance from the Hoopster to the basketball hoop
    '''

    # clear previous entries
    dis_lab2.clear()
    ang_lab2.clear()
    vel_lab2.clear()
    ang_vel_lab.clear()
    
    # cannot have a negative distance to launch to
    if distance < 0:
        distance = 0

    velocities =  calculate_velocity(0.1016, 0.1207, slider_rpm1.value * 2 * math.pi / 60, slider_rpm2.value * 2 * math.pi / 60)
    velocity = velocities[0]
    angular = velocities[1]

    # populate the fields
    dis_lab2.append("Expected Distance: {:.2f} m".format(distance))
    ang_lab2.append("Launch Angle: " + str(launch_angle_value.value) + "°")
    vel_lab2.append("Velocity: {:.2f} m/s".format(velocity))
    ang_vel_lab.append("Angular Velocity: {:.2f} rad/s".format(angular))
    
def run_main_menu():
    '''
    Hides this app and returns the main app page.
    '''
    try:
        app.hide()
        sys.exit()
    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")

def update_sliders():
    '''
    Updates the sliders.
    '''
    if rpm1_value.value:
        slider_rpm1.value = int(rpm1_value.value)
    else:
        slider_rpm1.value = 0

    if rpm2_value.value:
        slider_rpm2.value = int(rpm2_value.value)
    else:
        slider_rpm2.value = 0

    if azimuth_value.value:
        slider_azimuth.value = int(azimuth_value.value)
    else:
        slider_azimuth.value = 0

    if launch_angle_value.value:
        slider_launch_angle.value = int(launch_angle_value.value)
    else:
        slider_launch_angle.value = 0

    # determines the distance from the Hoopster to the hoop by executing trajectory calculations
    x_dist_to_center_of_hoop = update_graph()
    change_parameters(x_dist_to_center_of_hoop)

def adjust_hoopster():
    '''
    Handle the adjust button click event.
    '''
    print("RPM 1:", slider_rpm1.value)
    print("RPM 2:", slider_rpm2.value)
    print("Azimuth:", slider_azimuth.value)
    print("Launch Angle:", slider_launch_angle.value)
    run_main_menu()

def slider_changed(slider):
    '''
    Updates the variables asscoiated with the different sliders if the slider changed.
    '''
    if slider == slider_rpm1:
        rpm1_value.value = str(slider_rpm1.value)
    elif slider == slider_rpm2:
        rpm2_value.value = str(slider_rpm2.value)
    elif slider == slider_azimuth:
        azimuth_value.value = str(slider_azimuth.value)
    elif slider == slider_launch_angle:
        launch_angle_value.value = str(slider_launch_angle.value)

    # determines the distance from the Hoopster to the hoop by executing trajectory calculations   
    x_dist_to_center_of_hoop = update_graph()
    change_parameters(x_dist_to_center_of_hoop)

def update_graph():
    '''
    Updates the manual trajectory graph. Calls on the calculate manual function and passes the manually inputted
    launch angle value and the manually inputted velocity value. Takes the returned array of x and y values plots the graph.
    Adds a bar to represent the center of the hoop.

    returns: x distance to the hoop.
    '''
    velocity = calculate_velocity(0.1016, 0.1207, slider_rpm1.value * 2 * math.pi / 60, slider_rpm2.value * 2 * math.pi / 60)[0]
    print("I AM UPDATING THE GRAPH: Launch Angle: ", launch_angle_value.value, " Velocity: ", velocity)
    x, y, x_dist_to_center_of_hoop = calculate_manual(int(launch_angle_value.value), velocity)

    canvas.figure.clear()

    ax = canvas.figure.add_subplot(111)
    ax.plot(x, y, color='#ff8c00', linewidth=2)  # Change line color and thickness
    ax.set_title('Trajectory', color='white', fontsize=16, fontweight='bold')  # Change title color, size, and weight
    ax.set_xlabel('x [m]', color='#cccccc', fontsize=15)  # Change X-label color and size
    ax.set_ylabel('y [m]', color='#cccccc', fontsize=15)  # Change Y-label color and size

    # Add legend and labels
    ax.errorbar([x_dist_to_center_of_hoop], [3.05], xerr=[0.2286], ecolor="orange")
    disp_str = "x = " + '{:.2f}'.format(x_dist_to_center_of_hoop)
    ax.annotate(disp_str, xy= (x_dist_to_center_of_hoop, 3.05), xytext=(0.95, 0.95), textcoords='axes fraction', 
             ha='right', va='top', fontsize=15, color="orange")
    
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
    
    return x_dist_to_center_of_hoop
    

app = App(
    title="Manual Inputs",
    layout="grid",
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    bg=BACKGROUND_COLOR
)
app.set_full_screen()
app.text_color = "#ff8c00"
app.font = "Arial Black"

main_container = Box(app, layout="grid", grid=[0, 0], align="top")

selector_box = Box(main_container, layout="grid", grid=[1, 0], align="top")
title_lab = Text(selector_box, grid=[0, 0], text="Parameters", align="bottom", size=38, color="#ff8c00", font="Arial Black", bg="#2b2b2b")

rpm1_box = Box(selector_box, layout="grid", grid=[0, 1], align="top", width=300, height=1)
rpm1_box2 = Box(rpm1_box, layout="grid", grid=[0, 1], align="top", width=300, height=1)

rpm1_image = Picture(rpm1_box2, image="GUI/rpm1.png", grid=[0, 0], width=200, height=63, align="top")
rpm1_value = TextBox(rpm1_box2, grid=[1, 0], width=4, command=update_sliders, align="top", text="0")
rpm1_value.text_size = 30
rpm1_value.bg = BACKGROUND_COLOR
slider_rpm1 = Slider(
    rpm1_box,
    grid=[0, 2],
    width=309,
    height=30,
    start=0,
    end=SLIDER_MAX_RPM,
    command=lambda: slider_changed(slider_rpm1),
    align="top"
)
slider_rpm1.text_color=BACKGROUND_COLOR
slider_rpm1.value = 1000

selector_dummy_box1= Text(selector_box, grid=[0,2], width=1, height=2)

rpm2_box = Box(selector_box, layout="grid", grid=[0, 3], align="top")
rpm2_box2 = Box(rpm2_box, layout="grid", grid=[0, 1], align="top")

rpm2_image = Picture(rpm2_box2, image="GUI/rmp2.png", grid=[0, 0], width=200, height=63, align="top")
rpm2_value = TextBox(rpm2_box2, grid=[1, 0], width=4, command=update_sliders, align="top", text="0")
rpm2_value.text_size = 30
rpm2_value.bg = BACKGROUND_COLOR
slider_rpm2 = Slider(
    rpm2_box,
    grid=[0, 2],
    width=309,
    height=30,
    start=0,
    end=SLIDER_MAX_RPM,
    command=lambda: slider_changed(slider_rpm2),
    align="top"
)
slider_rpm2.text_color=BACKGROUND_COLOR
slider_rpm2.value = 1000

selector_dummy_box2= Text(selector_box, grid=[0,4], width=1, height=2)

azimuth_box = Box(selector_box, layout="grid", grid=[0, 5], align="top")
azimuth_box2 = Box(azimuth_box, layout="grid", grid=[0, 1], align="top")

azimuth_image = Picture(azimuth_box2, image="GUI/azimuth.png", grid=[0, 0], width=200, height=63, align="top")
azimuth_value = TextBox(azimuth_box2, grid=[1, 0], width=4, command=update_sliders, align="top", text="0")
azimuth_value.text_size = 30
azimuth_value.bg = BACKGROUND_COLOR
slider_azimuth = Slider(
    azimuth_box,
    grid=[0, 2],
    width=309,
    height=30,
    start=-SLIDER_MAX_AZIMUTH,
    end=SLIDER_MAX_AZIMUTH,
    command=lambda: slider_changed(slider_azimuth),
    align="top"
)
slider_azimuth.text_color=BACKGROUND_COLOR
slider_azimuth.value=0

selector_dummy_box3= Text(selector_box, grid=[0,6], width=1, height=2)

launch_angle_box = Box(selector_box, layout="grid", grid=[0, 7], align="top")
launch_angle_box2 = Box(launch_angle_box, layout="grid", grid=[0, 1], align="top")

launch_angle_image = Picture(launch_angle_box2, image="GUI/launchAngle.png", grid=[0, 0], width=200, height=63, align="top")
launch_angle_value = TextBox(launch_angle_box2, grid=[1, 0], width=4, command=update_sliders, align="top", text="0")
launch_angle_value.text_size = 30
launch_angle_value.bg = BACKGROUND_COLOR
slider_launch_angle = Slider(
    launch_angle_box,
    grid=[0, 2],
    width=309,
    height=30,
    start=0,
    end=SLIDER_MAX_LAUNCH_ANGLE,
    command=lambda: slider_changed(slider_launch_angle), 
    align="right"
)
slider_launch_angle.text_color=BACKGROUND_COLOR
slider_launch_angle.value=60

graph_box = Box(main_container, layout="grid", grid=[0, 0], width=1, height=1, align="left")
figure = Figure(figsize=(9, 5), dpi=160)
canvas = FigureCanvasTkAgg(figure, master=graph_box.tk)
canvas.draw()
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
update_graph()

adjust_button_box = Box(main_container, layout="grid", grid=[0, 1], align="top")
dummy1 = Text(adjust_button_box, grid=[1,0], width=1, height=10)
adjust_image = "GUI/adjust.png"
adjust_button = PushButton(
    adjust_button_box,
    grid=[1, 0],
    image=adjust_image,
    width=600*2,
    height=80*2,
    command=adjust_hoopster,
    align="bottom"
)

# Set up the main window UI
box1 = Box(main_container, layout="grid", grid=[1, 1], align="top", border=False, width=450, height=300)

row0 = Box(box1, layout="grid", grid=[0, 0], align="left", border=False)
row1 = Box(box1, layout="grid", grid=[0, 1], align="left", border=False)
row2 = Box(box1, layout="grid", grid=[0, 2], align="left", border=False)
row3 = Box(box1, layout="grid", grid=[0, 3], align="left", border=False)
row4 = Box(box1, layout="grid", grid=[0, 4], align="left", border=False)
row5 = Box(box1, layout="grid", grid=[0, 5], align="left", border=False)

#title_dummy = Text(row0, grid=[0, 0], text="", align="top", size=20, color="#ff8c00", font="Arial Black", bg="#2b2b2b")
title_lab2 = Text(row1, grid=[0, 0], text="Calculations", align="top", size=39, color="#ff8c00", font="Arial Black", bg="#2b2b2b")
dis_lab2 = Text(row2, grid=[0, 0], text="Expected Distance:", align="left", color="#c0c0c0", bg="#2b2b2b")
dis_lab2.text_size = 20
ang_lab2 = Text(row3, grid=[0, 0], text="Launch Angle:", align="left", color="#c0c0c0", bg="#2b2b2b")
ang_lab2.text_size = 20
vel_lab2 = Text(row4, grid=[0, 0], text="Velocity:", align="left", color="#c0c0c0", bg="#2b2b2b")
vel_lab2.text_size = 20
ang_vel_lab = Text(row5, grid=[0, 0], text="Angular Velocity:", align="left", color="#c0c0c0", bg="#2b2b2b")
ang_vel_lab.text_size = 20

change_parameters(0)
app.display()