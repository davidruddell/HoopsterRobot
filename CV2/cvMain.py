import numpy as np
from scipy.integrate import solve_ivp
import math
import matplotlib.pyplot as plt
import numpy as np
from ComputerVision import import_torch as itorch
import cv2
import time


C_d = 0.47
#coefficient of lift https://www.physicsforums.com/threads/what-is-the-lift-coefficient-of-a-basketball.841296/
#very rough estimate
C_l = 0.3
D = 0.2413
R = D / 2
A = np.pi * R**2
m = 0.624

rho_air = 1.28
g = 9.81

k = 0.5 * C_d * rho_air * A
#bball hoop height minus camera height
y_goal = (3.05 - 1.0668)

def deriv(t,u):
    x, v_x, y, v_y = u
    speed = np.hypot(v_x,v_y)
    dv_x_dt = -k/m * speed * v_x - k/m * speed * v_y
    dv_y_dt = -k/m * speed * v_y + k/m * speed * v_y - g
    return v_x, dv_x_dt, v_y, dv_y_dt

t0, tf = 0, 50

def hit_target(t,u):
    return u[2]

hit_target.terminal = True

hit_target.direction = -1

def max_height(t,u):
    return u[3]

def radians_to_degrees(radians):
    degrees = radians * (180.0 / math.pi)
    return degrees

def calculate_auto(x_goal):
    theta_arr = []
    v_i_arr = []
    angle2 = []
    x_arr = []
    y_arr = []
    
    #testing, furthest out we can shoot with a v_i of 15m/s is roughly 11.5m
   #x_goal=4.57

    #elevation system physically is able to adjust between 60deg to 73deg

    #maximum launch angle in radians (73deg)
    theta = 1.27409
    
    #minimum launch angle in radians (60deg)
    calcLaunchAngle_startTime = time.time()
    while theta > 1.0472:
        #start at 15m/s
        v_i = 15
        #end at 5m/s
        while v_i > 5:
        #1409.8337975132788rpm w 4in radius
            
            u0 = 0, v_i * np.cos(theta), 1, v_i * np.sin(theta)
            
            soln = solve_ivp(deriv, (t0, tf), u0, dense_output=True, events=(hit_target, max_height))
            t = np.linspace(0, soln.t_events[0][0],100)
            
            sol = soln.sol(t)
            x, y = sol[0], sol[2]
            
            check = 0
            final_angle = math.atan((y[-1] - y[-2]) / (x[-1] - x[-2]))

            for i in range(0,len(t)):
                if (abs(x_goal-0.2286-x[i])**2 + abs(y[i]-y_goal)**2)**(1/2) <= 0.12065:
                    break
                elif abs(x_goal-x[i]) < 0.05 and abs(y_goal-y[i]) < 0.05 and y[i] < y[i-1]:
                    theta_arr.append(theta)
                    v_i_arr.append(v_i)
                    angle2.append(final_angle)
                    x_arr.append(x)
                    y_arr.append(y)
                    
                    # #fully stop once we get a value very close to 60 degree entry angle to basket
                    # #1.0472 is 60 degree optimal entry angle
                    # if abs(final_angle - 1.0472) < .05:
                    #     print("checked")
                    #     check = 1
                    check = 1
                    #print("ichecked")
                    break
                if abs(final_angle) <= 0.698132:  # 40 degrees in radians
                    break
                    
            #final angle of 36deg is minimum allowable angle, but we use 40 deg = 0.698132rad
            if check == 1 or abs(final_angle) <= 0.698132:
                break
            #we want to step by 2rpm, 0.021279104m/s
            v_i -= 0.021279104
        
        if check == 1 or abs(final_angle) <= 0.698132:
            break
        #the elevation system is able to move .3deg at a time, .005rad
        theta -= 0.00523599
    #if no velocity solutions found
    if not v_i_arr:
        print("ibrokehere...nopossiblev")
        return None, None, None, -2

    print("Final angle" + str(radians_to_degrees(final_angle)))
    calcLaunchAngle_endTime = time.time()
    print(f"The Launch Angle calculations took {calcLaunchAngle_endTime - calcLaunchAngle_startTime} seconds to complete.")
    min_v = min(v_i_arr)
    index = v_i_arr.index(min_v)
    return x_arr[index], y_arr[index], theta_arr[index], round(min_v,2)

def get_rpm(v_b):
    omega_b = 6.76
    r_w = 0.15
    r_b = 0.12065
    omega_a = (v_b - omega_b * r_b) / r_w
    omega_c = omega_b * 2 * r_b / r_w + omega_a
    rpm_a = omega_a * 60 / (2 * math.pi)
    rpm_c = omega_c * 60 / (2 * math.pi)
    
    return rpm_a, rpm_c     


def solve_for_x_goal(hypot, y_ax):
    # Calculate the length of the x-axis
    x_goal = math.sqrt(hypot**2 - y_ax**2)
    return x_goal


def main():

    hypotenuse = itorch.main()

    #if hoop not detected
    if (hypotenuse == -1):
        return (None, -1, -1, [-1, -1])

    #solve for x-axis
    x_goal = solve_for_x_goal(hypotenuse, y_goal)



    #x_goal = 4.57
    result = calculate_auto(x_goal)
    calcDistanceAndVelocity_endTime = time.time()
    print(f"The distance and velocity calculations took {calcDistanceAndVelocity_endTime - itorch.calcDistanceAndVelocity_startTime} seconds to complete.")
    x_result, y_result, theta_result, v_result = result
    
    #if no solution found
    if (v_result == -2):
        return (None, -2, -2, [-2, -2])


    rpm = get_rpm(v_result)

    # import matplotlib.pyplot as plt

    # Specify the value for x_goal
    # x_goal = 4.2

    # Find the index of the point on the trajectory closest to the target coordinates
    closest_index = np.argmin((x_result - x_goal)**2 + (y_result - 3.05)**2)

    # # Plot the trajectory
    # plt.plot(x_result, y_result, label='Projectile Path')
    # plt.scatter(x_result[0], y_result😂[0], color='red', marker='o')
    # plt.scatter(x_result[-1], y_result[-1], color='green', marker='o')

    # # Plot the target point on the trajectory
    # plt.scatter(x_result[closest_index], y_result[closest_index], color='black', marker='x')

    # plt.title('Projectile Motion')
    # plt.xlabel('X Position (m)')
    # plt.ylabel('Y Position (m)')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    print("Results:")
    print("Launch Angle (theta):", theta_result)
    print("Initial Velocity (v_i):", v_result)
    print("Required RPM 1:", rpm[0])
    print("Required RPM 2:", rpm[1])
    return (result, x_goal, hypotenuse, rpm)

if __name__ == "__main__":
    main()