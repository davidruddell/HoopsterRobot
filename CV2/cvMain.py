'''
File: cvMain.py
Desc: This file is called in HoopsterGUI.py. It determines the optimal parameters for
      a successful shot based on the distance from the Hoopster to the basketball hoop
      determined by the computer vision. Applies the equations of motions and physics
      principles to calculate the x trajectory values, the y trajectory values, the
      optimal laucnh angle, the necessary velocity for the basketball, and the rpm values
      necessary for each pair of wheels in the flywheel.
'''
import numpy as np
from scipy.integrate import solve_ivp
import math
import matplotlib.pyplot as plt
import numpy as np
from ComputerVision import import_torch as itorch
import cv2

# CONSTANT:
C_d = 0.47                                   # rough estimate drag coefficient https://www.physicsforums.com/threads/what-is-the-lift-coefficient-of-a-basketball.841296/
C_l = 0.3                                    # lift coefficient
D = 0.2413                                   # diameter of the basketball
R = D / 2                                    # radius of the basketball
A = np.pi * R**2                             # area of a cross section of the basketball
m = 0.624                                    # mass of the basketball
rho_air = 1.28                               # density of air
g = 9.81                                     # acceleration due to gravity
FREE_THROW_HEIGHT = 3.05                     # height of the basketball hoop at regulation free throw conditions, m
CAMERA_HEIGHT = 1.08                         # height from the ground to the camera, m
y_goal = (FREE_THROW_HEIGHT - CAMERA_HEIGHT) # distance from the Hoopster to the basketball hoop, m
LAUNCH_ANGLE_LOWER = 60                      # lower bound for the possible launch angle
LAUNCH_ANGLE_UPPER = 62                    # upper bound for the possible launch angle
LAUNCH_VEL_LOWER = 6                        # lower bound for the possible launch velocity
LAUNCH_VEL_UPPER = 9                        # upper bound for the possible launch velocity
TOLERANCE = .05                              # tolerance for the shot to be off from the center of the hoop


def deriv(t, u):
    '''
    Defines the ODE that defines the motion of the basketball after being launched.

    t: in the solve_ivp populated with the range of t values to integrate over
    u: the initial values to consider when solving this initial value problem

    returns: v_x: the velocity in the x direction
             dv_x_dt: the acceleration in the x di
             rection
             v_y: velocity in the y direction
             dv_y_dt: the acceleration in the y direction.
    '''
    # variables in the ODE
    x, v_x, y, v_y = u
    speed = np.hypot(v_x, v_y)

    # first derivative we are solving for, x double dot = acceleration in x direction
    dv_x_dt = -(((rho_air * A * C_d)/(2 * m)) * speed * v_x) - (((rho_air * A * C_l)/(2 * m)) * speed * v_y)

    # second derivative we are solving for, y double dot = acceleration in y direction
    dv_y_dt = -(((rho_air * A * C_d)/(2 * m)) * speed * v_y) + (((rho_air * A * C_l)/(2 * m)) * speed * v_x) - g

    # returning x dot, x double dot, y dot, y double dot
    return v_x, dv_x_dt, v_y, dv_y_dt

# Integrate up to final t value unless we hit the target sooner
t0, tf = 0, 50

def hit_target(t,u):
    '''
    Returns when u[2] = y == 0.

    t: in the solve_ivp populated with the range of t values to integrate over
    u: the initial values to consider when solving this initial value problem

    returns: u[2]
    '''
    return u[2]

# Stop the integration when we hit the target (when u[2] == 0)
hit_target.terminal = True

# Continue the integration until the event function sign changes from positive to negative
hit_target.direction = -1

def max_height(t,u):
    '''
    Returns when u[3] = y velocity == 0 because the maximum height is obtained when
    the y-velocity is zero.

    t: in the solve_ivp populated with the range of t values to integrate over
    u: the initial values to consider when solving this initial value problem

    returns: u[3]
    '''
    return u[3]

def radians_to_degrees(radians):
    '''
    Converts the angle from radians to degrees.
    FIXME: is there a np function that does this?

    radians: an angle provided in radians

    returns: degrees: the angle provided converted to degrees
    '''
    degrees = radians * (180.0 / math.pi)
    return degrees

def solve_trajectory_ODE(theta_degrees, v_i):
    '''
    Solves the Initial Value Problem (IVP) defined by the system of ODEs in deriv. Guesses
    for theta_degrees and v_i are passed in to solve the IVP.

    theta_degrees: the current launch angle guess in degrees
    v_i: the current launch velocity guess

    returns: sol: the solution to the IVP
    '''
    theta = np.radians(theta_degrees)

    # initial_conditions = x_0, v_x_0, y_0, v_y_0
    initial_conditions = 0, v_i * np.cos(theta), CAMERA_HEIGHT, v_i * np.sin(theta)

    # solv_ivp(function, time span, initial state)
    soln = solve_ivp(deriv, (t0, tf), initial_conditions, dense_output=True, events=(hit_target, max_height))

    # time array with 100 points from 0 to the time of the first event
    #print("t events", soln.t_events[0][0])
    t = np.linspace(0, soln.t_events[0][0], 100)

    # interpolates the soln at the time valn def above and gets the x and y pos vals at these times
    sol = soln.sol(t)
    return sol

def is_possible__successful_shot(sol, x):
    '''
    Determines if the provided trajectory solution has a solution appropriately close to
    the desired x distance and y distance of the hoop from Hoopster.

    sol: the solution to the IVP
    x: the distance from Hoopster to the center of the basketball hoop

    returns: boolean specifying whether these parameters create a successful shot
    '''
    # Find index of closest x value to target x
    idx = np.abs(sol[0] - x).argmin()

    # Check if y distance at target x is within tolerance
    actual_y = sol[2][idx]
    return abs(actual_y - FREE_THROW_HEIGHT) <= TOLERANCE

def find_all_launch_angle_and_vel_solns(x_goal):
    '''
    Determine all possible combinations of launch angle and launch velocity within the appropriate
    ranges that will result in the ball reaching the hoop.

    x_goal: the distance from Hoopster to the center of the basketball hoop

    returns: TODO
    '''
    possible_solutions = []
    # get the ranges for the possible launch angles and velocity
    # TODO: what is the resolution of each...I can adjust the num' parameter to refelct this
    theta_range_degrees = np.arange(LAUNCH_ANGLE_LOWER, LAUNCH_ANGLE_UPPER, 0.00523599)
    v_i_range = np.arange(LAUNCH_VEL_LOWER, LAUNCH_VEL_UPPER, 0.021279104)

    #  iterate through all possible values of launch angle = theta
    for theta_degrees in theta_range_degrees:
        # iterate through all possible values of launch velocity
        for v_i in v_i_range:
            sol = solve_trajectory_ODE(theta_degrees, v_i)

            # successful shot is possible
            possible__successful_shot = is_possible__successful_shot(sol, x_goal)
            if (possible__successful_shot):
                possible_solutions.append([sol, theta_degrees, v_i])

    return possible_solutions

def calculate_entry_angle(sol):
    '''
    Calculates the entry angle for a shot specified by a specific launch angle and launch
    velocity. Entry angle = tan^-1[(hoop height - ground)/(x intercept - x val at the hoop)

    sol: the solution to the IVP

    returns: entry_engle_degrees: the entry angle of the shot in degrees
    '''
    # Find the index of the point in the trajectory closest to y_target
    idx = np.argmin(np.abs(sol[2] - FREE_THROW_HEIGHT))

    # Calculate the x-value when y = y_target
    x_target = sol[2][idx]

    # Find the index of the x-intercept (where y = 0)
    idx_x_intercept = np.argmin(np.abs(sol[2]))

    # Calculate the x-value at the x-intercept
    x_intercept = sol[2][idx_x_intercept]

    # Calculate the distance between the x-intercept and the x-value at y = y_target
    distance = np.abs(x_intercept - x_target)

    entry_angle = np.arctan2(FREE_THROW_HEIGHT/distance)
    
    return np.degrees(entry_angle)

def calculate_auto(x_goal):
    '''
    TODO
    '''
    possible_solutions_array = find_all_launch_angle_and_vel_solns(x_goal)

    # determine which solution gives the best entry angle
    optimal_entry_angle = 0
    print("iamhere!!!!!")
    best_sol = None 
    best_launch_angle_degrees = None
    best_launch_velocity = None
    for array in possible_solutions_array:
        cur_sol = array[0]
        print("helloKATELYN!")
        print(cur_sol)
        print("helloKATELYN2!")
        cur_launch_angle_degrees = array[1]
        cur_launch_velocity = array[2]
        cur_entry_angle = calculate_entry_angle(cur_sol)

        if (abs(60 - cur_entry_angle) < abs(60 - optimal_entry_angle)):
            optimal_entry_angle = cur_entry_angle
            best_sol = cur_sol
            best_launch_angle_degrees = cur_launch_angle_degrees
            best_launch_velocity = cur_launch_velocity

    if (best_sol == None):
        return (-2, -2, -2, -2)
    #      x vals,      y vals,      
    return best_sol[0], best_sol[2], best_launch_angle_degrees, best_launch_velocity
                    
def get_rpm(v_b):
    '''
    Calculate the necessary rpm for each pair of wheels for the shot.

    v_b: velocity of the basketball

    returns: rpm_a: rpm of the front pair of wheels FIXME: is this right?
             rpm_b: rpm of the back pair of wheels FIXME: which is which?
    '''
    # angular velocity of the basketball FIXME: is this right?
    # TODO: where did we get this value?
    omega_b = 6.76

    # raidus of the wheels
    r_w = 0.1016

    # radius of the basketball
    r_b = 0.12065

    # calculate the angular velocities of the two pairs of wheels
    # TODO: what is this calculating exactly?
    omega_a = (v_b - omega_b * r_b) / r_w
    print("OMEGA_A = ", omega_a)
    omega_c = omega_b * 2 * r_b / r_w + omega_a

    # calculate the rpm of the two pairs of wheels
    rpm_a = omega_a * 60 / (2 * math.pi)
    rpm_c = omega_c * 60 / (2 * math.pi)
    return rpm_a, rpm_c     

def solve_for_x_goal(hypotenuse, y_goal):
    '''
    Calculate the distance in the x direction from the Hoopster to the center of the
    basektball hoop.

    hypotenuse: total distance from the Hoopster to the center of the basketball hoop
    y_goal: distance in the y direction from the Hoopster camera to the center of the
            basketball hoop

    returns: x_goal: distance in the x direction from the Hoopster camera to the
            center of the basketball hoop
    '''
    x_goal = math.sqrt(hypotenuse**2 - y_goal**2)
    return x_goal


def main():
    '''
    Called in the HoopsterGUI file. Calculates the parameters for an optimal shot.

    returns: x_result: array of x values along the trajectory
             y_result: array of y values along the trajectory
             theta_result: the launch angle necessary for an optimal shot
             v_result: the velocity required for the optimal shot
             x_goal: the horizontal distance from the Hoopster to the center of the basketball hoop
             hypotenuse: the total distance from the Hoopster to the basketball goop
             rpm: a length = 2 array storing the required rpm for the first and second pairs of wheels respectively FIXME: is this the right order for the wheels?
    '''

    hypotenuse = itorch.main()
    print("Hypotenuse: ", hypotenuse)

    # if hoop not detected
    if (hypotenuse == -1):
        print("Hoop not detected.")
        # FIXME:              rpm value array
        return (None, -1, -1, [-1,-1])

    # x distance from Hoopster to the center of the basketball hoo[]
    x_goal = solve_for_x_goal(hypotenuse, y_goal)

    result = calculate_auto(x_goal)
    x_result, y_result, theta_result, v_result = result
    
    # if no solution found
    if (v_result == -2):
        print("No solution found.")
        return (None, -2, -2, [-2, -2])

    # determine the rpm of the pairs of wheels to power the shot
    rpm = get_rpm(v_result)

    print("Results:")
    print("Launch Angle (theta):", theta_result)
    print("Initial Velocity (v_i):", v_result)
    print("Required RPM 1:", rpm[0])
    print("Required RPM 2:", rpm[1])
    return (result, x_goal, hypotenuse, rpm)

if __name__ == "__main__":
    main()

# def calculate_auto(x_goal):
#     '''
#     Know the x distance from Hoopster to the center of the basketball hoop
#     Know the y distance from Hoopster to the center of the basketball hoop

#     Brute Force method:
#         - Iterate through the possible launch angle values
#             - Iterate through the possible launch velocity values
#                 - Determine which is closest to the shot we are looking for
#     '''
    
#     theta_arr = []
#     v_i_arr = []
#     angle2 = []
#     x_arr = []
#     y_arr = []
    
#     #testing, furthest out we can shoot with a v_i of 15m/s is roughly 11.5m
#    #x_goal=4.57

#     #elevation system physically is able to adjust between 60deg to 73deg

#     #minimum launch angle in radians (73deg)
#     theta = 1.27409
    
#     #maximum launch angle in radians (60deg)
#     while theta > 1.0472:
#         #start at 15m/s
#         v_i = 15
#         #end at 5m/s
#         while v_i > 5:
#         #1409.8337975132788rpm w 4in radius
            
#             u0 = 0, v_i * np.cos(theta), 1, v_i * np.sin(theta)
            
#             soln = solve_ivp(deriv, (t0, tf), u0, dense_output=True, events=(hit_target, max_height))
#             t = np.linspace(0, soln.t_events[0][0],100)
            
#             sol = soln.sol(t)
#             x, y = sol[0], sol[2]
            
#             check = 0
#             final_angle = math.atan((y[-1] - y[-2]) / (x[-1] - x[-2]))

#             for i in range(0,len(t)):
#                 if (abs(x_goal-0.2286-x[i])**2 + abs(y[i]-y_goal)**2)**(1/2) <= 0.12065:
#                     break
#                 elif abs(x_goal-x[i]) < 0.05 and abs(y_goal-y[i]) < 0.05 and y[i] < y[i-1]:
#                     theta_arr.append(theta)
#                     v_i_arr.append(v_i)
#                     angle2.append(final_angle)
#                     x_arr.append(x)
#                     y_arr.append(y)
                    
#                     # #fully stop once we get a value very close to 60 degree entry angle to basket
#                     # #1.0472 is 60 degree optimal entry angle
#                     # if abs(final_angle - 1.0472) < .05:
#                     #     print("checked")
#                     #     check = 1
#                     check = 1
#                     #print("ichecked")
#                     break
#                 if abs(final_angle) <= 0.698132:  # 40 degrees in radians
#                     break
                    
#             #final angle of 36deg is minimum allowable angle, but we use 40 deg = 0.698132rad
#             if check == 1 or abs(final_angle) <= 0.698132:
#                 break
#             #we want to step by 2rpm, 0.021279104m/s
#             v_i -= 0.021279104
        
#         if check == 1 or abs(final_angle) <= 0.698132:
#             break
#         #the elevation system is able to move .3deg at a time, .005rad
#         theta -= 0.00523599
#     #if no velocity solutions found
#     if not v_i_arr:
#         print("ibrokehere...nopossiblev")
#         return None, None, None, -2

#     print("Final angle" + str(radians_to_degrees(final_angle)))
#     min_v = min(v_i_arr)
#     index = v_i_arr.index(min_v)
#     return x_arr[index], y_arr[index], theta_arr[index], round(min_v,2) # supposed to give us the optimal shot but right now it is giving us the first index...