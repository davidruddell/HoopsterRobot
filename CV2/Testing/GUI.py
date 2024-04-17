import tkinter
import tkinter.messagebox
import customtkinter
import cv2
from PIL import Image

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt

from Hoopster_Calculations import calculate_auto, calculate_manual, hoop_width, distance_finder, get_rpm

import numpy as np
import collections

#import serial

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        # configure window
        #self.iconphoto(False, tkinter.PhotoImage(file = 'original - Copy.jpg'))
        self.title("ball_e_gui.py")
        self.geometry(f"{800}x{480}")


        # configure grid layout
        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure((0,1), weight=1)


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=120, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        logo = customtkinter.CTkImage(light_image=Image.open("photo.jpg"),
                                  dark_image=Image.open("photo.jpg"), size=(220, 60))
        self.logo_label = customtkinter.CTkButton(self.sidebar_frame, state="disabled", image=logo, text='', fg_color="#003153")
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))


        self.switch_1 = customtkinter.CTkSwitch(master=self.sidebar_frame, text="Power: off", command=self.switch_1_event)
        self.switch_1.grid(row=1, column=0, pady=10, padx=20, sticky="n")
        self.switch_2 = customtkinter.CTkSwitch(master=self.sidebar_frame, text="Camera: off", command=self.switch_2_event)
        self.switch_2.grid(row=2, column=0, pady=10, padx=20, sticky="n")

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_optionemenu.set("Dark")
       
        self.tabview1 = customtkinter.CTkTabview(self)
        self.tabview1.grid(row=0, column=1, columnspan=1, padx=(20, 0), pady=(0, 0), sticky="nsew")
        self.tabview1.add("Trajectory")
        self.tabview1.add("RPM")

        # create matplot frame
        self.fig,self.ax = plt.subplots(figsize=(4,2.5))
        self.ax.set_xlabel('x [m]')
        self.ax.set_ylabel('y [m]')
        plt.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tabview1.tab("Trajectory"))  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # create rpm plot frame
        self.fig1,self.ax1 = plt.subplots(figsize=(4,2.5))
        self.ax1.set_xlabel('t [s]')
        self.ax1.set_ylabel('RPM')
        plt.tight_layout()
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.tabview1.tab("RPM"))  # A tk.DrawingArea.
        self.canvas1.draw()
        self.change_appearance_mode_event("Light")
        self.canvas1.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.exp_rpm1_que = collections.deque(np.zeros(20))
        self.exp_rpm2_que = collections.deque(np.zeros(20))
        self.rpm1_que = collections.deque(np.zeros(20))
        self.rpm2_que = collections.deque(np.zeros(20))
       
        # set default data
        self.width = None
        self.angle_offset = 0
        self.velocity_offset = 0
        self.angle = 0
        self.rpm1 = 0
        self.rpm2 = 0
        self.exp_rpm1 = 0
        self.exp_rpm2 = 0

        # create camera footage frame
        self.cam = customtkinter.CTkFrame(self.sidebar_frame)
        self.cam.grid(row=3, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")

        # access local webcam or server camera footage
        #inp = input("Enter Server:")
        #if inp == '0':
        self.cap = cv2.VideoCapture(0)
        #else:
        #    server = "http://" + inp + "/video"
        #    self.cap = cv2.VideoCapture(server)
       
        # set camera frame
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
        self.label_widget = customtkinter.CTkLabel(self.cam, text="Camera Off")
        self.label_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # create data frame
        self.data_frame = customtkinter.CTkFrame(self, width = 100)
        self.data_frame.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsw")
        self.label_data_1 = customtkinter.CTkLabel(master=self.data_frame, text="Distance:")
        self.label_data_1.grid(row=0, column=0, columnspan=1, padx=10, pady=5, sticky="w")
        self.label_data_2 = customtkinter.CTkLabel(master=self.data_frame, text="RPM1:")
        self.label_data_2.grid(row=1, column=0, columnspan=1, padx=10, pady=5, sticky="w")
        self.label_data_3 = customtkinter.CTkLabel(master=self.data_frame, text="RPM2:")
        self.label_data_3.grid(row=2, column=0, columnspan=1, padx=10, pady=5, sticky="w")
        self.label_data_4 = customtkinter.CTkLabel(master=self.data_frame, text="Exp. RPM1:")
        self.label_data_4.grid(row=3, column=0, columnspan=1, padx=10, pady=5, sticky="w")
        self.label_data_5 = customtkinter.CTkLabel(master=self.data_frame, text="Exp. RPM2:")
        self.label_data_5.grid(row=4, column=0, columnspan=1, padx=10, pady=5, sticky="w")
        self.label_data_6 = customtkinter.CTkLabel(master=self.data_frame, text="Exp. Velocity:")
        self.label_data_6.grid(row=5, column=0, columnspan=1, padx=10, pady=5, sticky="w")
        self.label_data_7 = customtkinter.CTkLabel(master=self.data_frame, text="Angle:")
        self.label_data_7.grid(row=6, column=0, columnspan=1, padx=10, pady=5, sticky="w")

        # create aim tab frames
        self.tabview2 = customtkinter.CTkTabview(self)
        self.tabview2.grid(row=1, column=1, columnspan=2, rowspan=2, padx=(20, 20), pady=(0, 20), sticky="nsew")
        self.tabview2.add("Manual Aim")
        self.tabview2.add("Automatic Aim")
        self.tabview2.add("Calibration")
       
        # Manual Aim tab
        self.slider_1 = customtkinter.CTkSlider(self.tabview2.tab("Manual Aim"), from_=1.00, to=7.00, number_of_steps=600, command=self.get_manual_distance)
        self.slider_1.grid(row=0, column=1, padx=(10, 10), pady=(0, 10), sticky="ew")
        self.label_1 = customtkinter.CTkLabel(self.tabview2.tab("Manual Aim"), text=("Distance:", self.slider_1.get(), "m"))
        self.label_1.grid(row=0, column=0, padx=(20, 10), pady=(0, 10), sticky="w")
        self.slider_2 = customtkinter.CTkSlider(self.tabview2.tab("Manual Aim"), from_=0.87, to=1.38, number_of_steps=51, command=self.get_v_angle)
        self.slider_2.grid(row=1, column=1, padx=(10, 10), pady=(0, 10), sticky="ew")
        self.label_2 = customtkinter.CTkLabel(self.tabview2.tab("Manual Aim"), text=("Angle:", self.slider_2.get(), "rad"))
        self.label_2.grid(row=1, column=0, padx=(20, 10), pady=(0, 10), sticky="w")
        self.slider_3 = customtkinter.CTkSlider(self.tabview2.tab("Manual Aim"), from_=6.8, to=10.3, number_of_steps=35, command=self.get_velocity)
        self.slider_3.grid(row=2, column=1, padx=(10, 10), pady=(0, 10), sticky="ew")
        self.label_3 = customtkinter.CTkLabel(self.tabview2.tab("Manual Aim"), text=("Velocity:", self.slider_3.get(), "m/s"))
        self.label_3.grid(row=2, column=0, padx=(20, 10), pady=(0, 10), sticky="w")
        self.button_aim = customtkinter.CTkButton(master=self.tabview2.tab("Manual Aim"), text="Aim", command=self.manual_aim)
        self.button_aim.grid(row=3, column=0, padx=(20, 10), pady=(0, 10), sticky="se")
        self.launch_button_1 = customtkinter.CTkButton(master=self.tabview2.tab("Manual Aim"), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Launch")
        self.launch_button_1.grid(row=3, column=1, padx=(20, 10), pady=(0, 10), sticky="se")
       
        # Automatic Aim tab
        self.sidebar_button_2 = customtkinter.CTkButton(self.tabview2.tab("Automatic Aim"), text="Auto Aim", command=self.auto_aim)
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)
        self.progressbar_2 = customtkinter.CTkProgressBar(self.tabview2.tab("Automatic Aim"))
        self.progressbar_2.grid(row=0, column=1, padx=(10, 10), pady=(0, 10), sticky="ew")
        self.label_4 = customtkinter.CTkLabel(self.tabview2.tab("Automatic Aim"), text=("Distance:", self.slider_1.get(), "m"))
        self.label_4.grid(row=0, column=0, padx=(20, 10), pady=(0, 10), sticky="w")
        self.progressbar_3 = customtkinter.CTkProgressBar(self.tabview2.tab("Automatic Aim"))
        self.progressbar_3.grid(row=1, column=1, padx=(10, 10), pady=(0, 10), sticky="ew")
        self.label_5 = customtkinter.CTkLabel(self.tabview2.tab("Automatic Aim"), text=("Angle:", self.slider_2.get(), "rad"))
        self.label_5.grid(row=1, column=0, padx=(20, 10), pady=(0, 10), sticky="w")
        self.progressbar_4 = customtkinter.CTkProgressBar(self.tabview2.tab("Automatic Aim"))
        self.progressbar_4.grid(row=2, column=1, padx=(10, 10), pady=(0, 0), sticky="ew")
        self.label_6 = customtkinter.CTkLabel(self.tabview2.tab("Automatic Aim"), text=("Velocity:", self.slider_3.get(), "m/s"))
        self.label_6.grid(row=2, column=0, padx=(20, 10), pady=(0, 0), sticky="w")
        self.launch_button_2 = customtkinter.CTkButton(master=self.tabview2.tab("Automatic Aim"), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Launch")
        self.launch_button_2.grid(row=3, column=1, padx=(20, 10), pady=(0, 10), sticky="se")
       
        # Calibration tab
        self.slider_4 = customtkinter.CTkSlider(self.tabview2.tab("Calibration"), from_=-0.2, to=0.2, number_of_steps=40, command=self.get_added_angle)
        self.slider_4.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")
        self.label_7 = customtkinter.CTkLabel(self.tabview2.tab("Calibration"), text=("Added", "Angle:", self.slider_4.get(), "rad"))
        self.label_7.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="w")
        self.slider_5 = customtkinter.CTkSlider(self.tabview2.tab("Calibration"), from_=-2, to=2, number_of_steps=40, command=self.get_added_velocity)
        self.slider_5.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")
        self.label_8 = customtkinter.CTkLabel(self.tabview2.tab("Calibration"), text=("Added", "Velocity:", self.slider_5.get(), "m/s"))
        self.label_8.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="w")
        self.button_adjust = customtkinter.CTkButton(master=self.tabview2.tab("Calibration"), text="Adjust", command=self.calibrate)
        self.button_adjust.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="se")

        self.change_appearance_mode_event("Dark")
       
        # serial communication
        #self.obj = serial.Serial()
        #self.obj.baudrate = 9600
        #self.obj.bytesize = 8
        #self.obj.parity = 'N'
        #self.obj.stopbits = 1
       
        self.plot_rpm()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        if new_appearance_mode == "Dark":
            self.ax.set_facecolor("#333333")
            self.fig.set_facecolor("#333333")
            self.ax.xaxis.label.set_color('white')
            self.ax.yaxis.label.set_color('white')
            self.ax.tick_params(axis='x', colors='#DCE4EE')  
            self.ax.tick_params(axis='y', colors='#DCE4EE')
            self.ax.spines[:].set_color('#DCE4EE')
            self.ax1.set_facecolor("#292929")
            self.fig1.set_facecolor("#292929")
            self.ax1.xaxis.label.set_color('white')
            self.ax1.yaxis.label.set_color('white')
            self.ax1.tick_params(axis='x', colors='#DCE4EE')  
            self.ax1.tick_params(axis='y', colors='#DCE4EE')
            self.ax1.spines[:].set_color('#DCE4EE')
            plt.style.use("dark_background")

        else:
            self.ax.set_facecolor("#d9d9d9")
            self.fig.set_facecolor("#d9d9d9")
            self.ax.xaxis.label.set_color('black')
            self.ax.yaxis.label.set_color('black')
            self.ax.tick_params(axis='x', colors='black')  
            self.ax.tick_params(axis='y', colors='black')
            self.ax.spines[:].set_color('black')
            self.ax1.set_facecolor("#d9d9d9")
            self.fig1.set_facecolor("#d9d9d9")
            self.ax1.xaxis.label.set_color('black')
            self.ax1.yaxis.label.set_color('black')
            self.ax1.tick_params(axis='x', colors='black')  
            self.ax1.tick_params(axis='y', colors='black')
            self.ax1.spines[:].set_color('black')
            plt.style.use("default")
        self.canvas.draw()

    def switch_1_event(self):
        if self.switch_1.get() == 1:
            self.switch_1.configure(text="Power: on")
        else:
            self.switch_1.configure(text="Power: off")

    def switch_2_event(self):
        self.open_camera()

    def get_manual_distance(self, dist):
        self.label_1.configure(text=("Distance:", round(dist, 2), "m"))
        self.label_data_1.configure(text=("Distance:", round(dist, 2), "m"))

    def get_v_angle(self, angle):
        self.label_2.configure(text=("Angle:", round(angle, 2), "rad"))
        self.label_data_7.configure(text = ("Angle:", round(angle, 2), "rad"))
        self.angle = angle

    def get_velocity(self, v):
        self.label_3.configure(text=("Velocity:", round(v, 2), "m/s"))
        self.label_data_6.configure(text = ("Velocity", round(v, 2), "m/s"))

    def get_added_angle(self, angle):
        self.label_7.configure(text=("Added", "Angle:", round(angle, 2), "rad"))

    def get_added_velocity(self, v):
        self.label_8.configure(text=("Added", "Velocity:", round(v, 2), "m/s"))
       
    def calibrate(self):
        print("d")
   
    def open_camera(self):
        print("d")

    def manual_aim(self):
        x, y = calculate_manual(self.slider_2.get(), self.slider_3.get())
        self.plot(x, y, self.slider_1.get())
        self.label_data_1.configure(text=("Distance:", round(self.slider_1.get(), 2), "m"))
        self.label_data_7.configure(text = ("Angle:", round(self.slider_2.get(), 2), "rad"))
        self.label_data_6.configure(text = ("Exp.", "Velocity:", round(self.slider_3.get(), 2), "m/s"))
        self.exp_rpm1, self.exp_rpm2 = get_rpm(self.slider_3.get())
        self.label_data_4.configure(text = ("Exp.", "RPM1:", round(self.exp_rpm1, 2)))
        self.label_data_5.configure(text = ("Exp.", "RPM2:", round(self.exp_rpm2, 2)))

    def auto_aim(self):
        if self.width:
            distance = distance_finder(self.width) * 0.567
            x, y, theta, v_i = calculate_auto(distance)
            theta = theta + self.angle_offset
            self.angle = theta
            v_i = v_i + self.velocity_offset
            self.plot(x, y, distance)
            self.progressbar_2.set((distance/100-1)/6)
            self.progressbar_3.set((theta-0.87)/0.51)
            self.progressbar_4.set((v_i-6.8)/3.5)
            self.label_4.configure(text=("Distance:", round(distance, 2), "m"))
            self.label_5.configure(text=("Angle:", round(theta, 2), "rad"))
            self.label_6.configure(text=("Velocity:", round(v_i, 2), "m/s"))
            self.label_data_1.configure(text=("Distance:", round(distance, 2), "m"))
            self.label_data_7.configure(text = ("Angle:", round(theta, 2), "rad"))
            self.label_data_6.configure(text = ("Exp.", "Velocity:", round(v_i, 2), "m/s"))
            self.exp_rpm1, self.exp_rpm2 = get_rpm(v_i)
            self.label_data_4.configure(text = ("Exp.", "RPM1:", round(self.exp_rpm1, 2)))
            self.label_data_5.configure(text = ("Exp.", "RPM2:", round(self.exp_rpm2, 2)))
   
    def plot(self, x, y, distance):
        # plot trajectory
        self.ax.clear()
        self.ax.plot(x ,y,"#3a7ebf", label='Quadratic Drag')
        self.ax.errorbar([distance], [3.05], xerr=[0.2286], ecolor="orange")
        self.ax.set_xlabel('x [m]')
        self.ax.set_ylabel('y [m]')
        self.ax.legend()
        self.canvas.draw()
   
    def plot_rpm(self):
        print("d")
   
    def serial_com(self):
        print("d")

if __name__ == "__main__":
    app = App()
    app.mainloop()