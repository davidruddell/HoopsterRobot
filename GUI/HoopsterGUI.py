import guizero
import subprocess
from guizero import MenuBar, App, Text, Picture, CheckBox, PushButton, Box, ButtonGroup, Window

import time

app = App(title = "Hoopster", layout = "grid", bg = (211, 211, 211), width = 1024, height = 600)
window = Window(app, title = "Launching",  bg= "white", width = 1024, height = 600, visible = False)

pady1 = Box(window, height = 30, width = 30)
gif = Picture(window, image = "swish.gif", width = 600, height = 400)
pady = Box(window, height = 30, width = 30)
box = Box(window, layout = "grid")

suc = 0
fail = 0
total = 0
rateval = 0

set_trig = False
launched = False

def success_shot():
    global suc
    suc += 1
    app.show()
    update_stats()
    abort_fun()
    window.hide()

def fail_shot():
    global fail
    fail += 1
    app.show()
    update_stats()
    abort_fun()
    window.hide()

def run_move_menu():
    try:
        # Replace 'path/to/your/script.py' with the actual path to your Python script
        app.hide()
        process = subprocess.Popen(['python', 'MobilityDisplay.py'])
        # Continue with the rest of the parent script without waiting for the subprocess
        
        process.wait()
        print("Parent script continues running...")
        # Display the application again    
        app.show()

    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")

def run_manual_menu():
    try:
        # Replace 'path/to/your/script.py' with the actual path to your Python script
        app.hide()
        process = subprocess.Popen(['python', 'ManualDisplay.py'])
        # Continue with the rest of the parent script without waiting for the subprocess
        
        process.wait()
        print("Parent script continues running...")
        # Display the application again    
        app.show()


    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")

menubar = MenuBar(app,
                  toplevel=["Displays"],
                  options=[
                      [ ["Manual Input", run_manual_menu], ["Mobility", run_move_menu] ]                     
                  ])

#success = PushButton(box,text="Success",  width=10, height = 2, grid=[0,0], command=success_shot)
success = PushButton(box, image="Success.png",  width=215, height = 95, grid=[0,0], command=success_shot)
success.bg = "green"
buffer = Box(box,  height=20, width=30, grid=[1,0])
#failure = PushButton(box, text="Fail", width=10, height = 2, grid=[2,0], command=fail_shot)
failure = PushButton(box, image="Fail.png", width=215, height = 95, grid=[2,0], command=fail_shot)
failure.bg="#CC6600";
#success.bg="green"
#failure.bg="red"

app.font="Arial Black"
app.text_size=16;
#box_main = Box(app, grid=[0,0], width=35,height=25)
#box_main.bg="green"
#logo = PushButton(app, image="logo.png",  grid=[0,0], align="left", command=run_move_menu, width=165, height=165)
logo = PushButton(app, image="logo.png",  grid=[0,0], align="left", command=run_move_menu, width=200, height=200)

box1= Box(app, layout = "grid", grid=[0,1], align="left")
box2= Box(app, layout = "grid", grid=[0,2], align="left")
spacing = Box(box1,grid=[0,0], width=150, height=15 )

row1 = Box(box1, layout="grid", grid=[0,1], align="left")
row2 = Box(box1, layout="grid", grid=[0,2], align="left")
row3 = Box(box1, layout="grid", grid=[0,3], align="left")
row4 = Box(box2, layout="grid", grid=[0,3], align="left")
row5 = Box(box2, layout="grid", grid=[0,4], align="left")
row6 = Box(box2, layout="grid", grid=[0,5], align="left")
row7 = Box(box2, layout="grid", grid=[0,6], align="left")


# Status Boxes
hoop_status = Picture(row1, image="NotCheck.png",grid=[0,0], width=45, height=45, align="left")
pos_status = Picture(row2, image="NotCheck.png",grid=[0,0], width=45, height=45, align="left")
dis_status = Picture(row3, image="NotCheck.png",grid=[0,0], width=45, height=45, align="left")
ang_status = Picture(row4, image="NotCheck.png", grid=[0,0], width=45, height=45, align="left")
vel_status = Picture(row5, image="NotCheck.png", grid=[0,0], width=45, height=45, align="left")
anom_status = Picture(row6, image="NotCheck.png", grid=[0,0], width=45, height=45, align="left")
ready_status = Picture(row7, image="NotCheck.png", grid=[0,0], width=45, height=45, align="left")
#check=Picture(box1, image="Check.png",grid=[0,0], width=50, height=50, align="left")
hoop = Text(row1, grid=[1,0], text="HOOP DETECTED", align="left")
pos = Text(row2, grid=[1,0], text="POSITION SET", align="left")
dis = Text(row3, grid=[1,0], text="DISTANCE CALCULATED", align="left")
ang = Text(row4, text="LAUCH ANGLE CALCULATED", grid=[1,0], align="left")
vel = Text(row5, text="VELOCITY CALCULATED", grid=[1,0], align="left")
anom = Text(row6, text="ANOMALY DETECTED", grid=[1,0], align="left")
ready = Text(row7, text="READY FOR LAUNCH", grid=[1,0], align="left")



def launch_countdown():
    if set_trig and ready_status.image == "Check.png":
        app.repeat(1000, update_timer)
    else:
        print("Not ready for launch. Set Hoopster first.")

def launch():
    global launched

    if set_trig and ready_status.image == "Check.png":

        global total
        total += 1
        print("Launching Basketball")
        
        
        launched = True
        window.show()
        app.hide()
        
    else:
        print("Not ready for launch. Set Hoopster first.")

def launch_ready():
    if (anom.value == 0):
        print("Ready for Launch...")
        ready.toggle()

def set():
    global set_trig

    print("Preparing for launch")
    set_trig = True

    dis_lab.clear()
    ang_lab.clear()
    vel_lab.clear()
    
    dis_lab.append("Distance: 4.2 m")
    ang_lab.append("Launch Angle: 65 deg")
    vel_lab.append("Velocity: 8.35 m/s")

    hoop_status.image = "Check.png"
    pos_status.image = "Check.png"
    dis_status.image = "Check.png"
    ang_status.image = "Check.png"
    vel_status.image = "Check.png"
    ready_status.image = "Check.png"
    print("Ready for launch")
   

def abort_fun():
    global launched
    if not launched:
        print("Launch Aborted.")

    dis_lab.clear()
    ang_lab.clear()
    vel_lab.clear()

    dis_lab.append("Distance:")
    ang_lab.append("Launch Angle:")
    vel_lab.append("Velocity:")
    hoop_status.image = "NotCheck.png"
    pos_status.image = "NotCheck.png"
    dis_status.image = "NotCheck.png"
    ang_status.image = "NotCheck.png"
    vel_status.image = "NotCheck.png"
    ready_status.image = "NotCheck.png"
    

def detect_anomaly():
    #implement function that detects anomaly through sensor
    #temporary code    
    if anom_status.image =="Check.png":
        anom_status.image = "NotCheck.png"
        app.warn("Warning","Anomaly Detected - Launch Aborted")
        abort_fun()

def calc_rate():
    global rateval
    
    if total != 0:
        rateval = (suc/total)*100
    else:
        rateval = 0
    return round(rateval,2)




pad1 = Box(app,  height=20, width=45, grid=[1,0])
launch_b = PushButton(app,text="Launch",image="LaunchButton.png", command=launch_countdown, grid=[2,0], align="right",width=215, height = 95)
launch_b.bg="green";
set = PushButton(app,text="Set",image="SetButton.png", command=set, grid=[2,1], align="right",width=215, height = 95)
set.bg = "#A17C04"
#set = PushButton(app,text="Set", command=set, grid=[1,1], align="right",width=10, height = 2)
#set.bg="yellow";
abort = PushButton(app,text="Abort",image="AbortButton.png", command=abort_fun, grid=[2,2], align="right",width=215, height = 95)

#abort = PushButton(app,text="Abort", command=abort_fun, grid=[1,2], align="right",width=10, height = 2)
abort.bg="#CC6600";

pad2 = Box(app,  height=20, width=65, grid=[3,0])

box3 = Box(app, layout = "grid", grid=[5,0], align="left")
#timer = Text(box3, grid=[0,0], text="Launch Countdown", align="right")
timer = Picture(box3, grid=[0,0], image="LaunchCountdown.png", align="right", width=275, height=40)

clock_dis = Text(box3, text="5", grid=[0,1])
clock_dis.text_size = 48
clock_dis.text_color = "#990000"
countdown = 5

box5 = Box(app, layout = "grid", grid=[5,1], align="left")
dis_lab = Text(box5, grid=[0,0], text="Distance:", align="left")
ang_lab= Text(box5, grid=[0,1], text = "Launch Angle:",  align="left")
vel_lab = Text(box5, grid=[0,2], text = "Velocity:",  align="left")



box6 = Box(app, layout= "grid", grid=[5,2], align="left")

def reset_stats():
    global suc
    global fail
    global total 
    global rateval

    suc = 0
    fail = 0
    total = 0
    rateval = 0

    update_stats()
#stats = Text(box5, grid=[0,0], text="CURRENT STATISTICS", align="left")
buff= Box(box6, grid=[0,0], width = 250, height=30)

stats = Picture(box6, grid=[0,1], image="CurrentStatistics.png", align="left", width=275, height=40)
stats.text_color="Orange"
successes = Text(box6, grid=[0,2], text="Successes: "+str(suc), align="left")
failures = Text(box6, grid=[0,3], text="Failures: "+str(fail), align="left")
rate = Text(box6, grid=[0,4], text="Success Rate: "+str(calc_rate())+"%", align="left")
#reset = PushButton(box5, grid=[0,5], text="Reset Statistics", align="left",width=13, height=1, pady=0, command=reset_stats)
reset = PushButton(box6, grid=[0,5],image="ResetButton.png", text="Reset Statistics", align="left",width=275, height=40, pady=0, command=reset_stats)
reset.bg="black"

#reset.text_size = 12

def update_timer():
    global countdown
    countdown -= 1
    timer.image = "BackUp.png"
    
    clock_dis.value = str(countdown)
    
    if countdown == 0:
        launch()
        app.cancel(update_timer)
        timer.image = "LaunchCountdown.png"
        clock_dis.value = "5"
        countdown = 5

        

def update_stats():
    successes.clear()
    failures.clear()
    rate.clear()

    successes.append("Successes: " + str(suc))
    failures.append("Failures: " + str(fail))
    rate.append("Success Rate: " + str(calc_rate()) + "%")

app.repeat(1000, detect_anomaly)

app.display()
