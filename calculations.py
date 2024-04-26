#!/usr/bin/env python3
import numpy as np
from scipy.integrate import solve_ivp
import math
from scipy.interpolate import interp1d

# Drag coefficient, projectile radius (m), area (m2) and mass (kg).
C_d = 0.47
D = 0.2413  # m
R = D / 2  # m
A = np.pi * R**2
m = 0.624
# Air density (kg.m-3), acceleration due to gravity (m.s-2).
rho_air = 1.28
g = 9.81
# For convenience, define  this constant.
k = 0.5 * C_d * rho_air * A
y_goal = 3.05  # m


def deriv(t, u):
    '''
    Defines the ODE that defines the motion of the basketball after being launched.

    t: in the solve_ivp populated with the range of t values to integrate over
    u: the initial values to consider when solving this initial value problem

    returns: v_x: the velocity in the x direction
             dv_x_dt: the acceleration in the x direction
             v_y: velocity in the y direction
             dv_y_dt: the acceleration in the y direction.
    '''

    # variables in the ODE
    x, v_x, y, v_y = u
    speed = np.hypot(v_x, v_y)

    # first derivate we are solving for, x double dot = acceleration in x direction
    dv_x_dt = -(k/m * speed * v_x) - (k/m * speed * v_y)

    # second derivate we are solving for, y double dot = acceleration in y direction
    dv_y_dt = -(k/m * speed * v_y) + (k/m * speed * v_x) - g

    # returning x dot, x double dot, y dot, y double dot
    return v_x, dv_x_dt, v_y, dv_y_dt

# Integrate up to final t value unless we hit the target sooner.
t0, tf = 0, 50

def hit_target(t, u):
    '''
    Returns when u[2] = y == 0. 
    '''
    return u[2]

# Stop the integration when we hit the target (when u[2] == 0)
hit_target.terminal = True

# Continue the integration until the event function sign changes from positive to negative
hit_target.direction = -1

def max_height(t, u):
    '''
    Returns when u[3] = y acceleration == 0
    '''
    # The maximum height is obtained when the y-velocity is zero.
    return u[3]

def calculate_manual(theta_degrees, v_i):
    '''
    Returns an array of x values and an array of y values (each length = 100) 
    representing the different points along the trajectory. Also, returns the
    x-distance to the basketball hoop.

    theta_degrees: the launch angle in degrees
    v_i: initial velocity of the basketball

    return: x: array of x values along the trajectory (size = 100)
            y: array of y values along the trajectory (size = 100)
            x_at_y_3_05: x distance when the basketball swishes through the center of the hoop
    '''

    theta = np.radians(theta_degrees)

    # initial_conditions = x_0, v_x_0, y_0, v_y_0
    initial_conditions = 0, v_i * np.cos(theta), 1, v_i * np.sin(theta)

    # solv_ivp(function, time span, initial state)
    soln = solve_ivp(deriv, (t0, tf), initial_conditions, dense_output=True, events=(hit_target, max_height))

    # time array with 100 points from 0 to the time of the first event
    print("t events", soln.t_events[0][0])
    t = np.linspace(0, soln.t_events[0][0], 100)

    # interpolates the soln at the time valn def above and gets the x and y pos vals at these times
    sol = soln.sol(t)
    x, y = sol[0], sol[2]

    # Find the index of the maximum y value
    max_y_idx = np.argmax(y)

    # Get the x coordinate at the maximum y value
    max_x = x[max_y_idx]

    # Initialize x_at_y_3_05
    x_at_y_3_05 = -100

    # try different distance thresholds to find the x value in our calculated trajectory that corresponds
    # with the y value closest to 3.05; this value will be passed as our distance to the hoop
    # evaluate at increasing larger thresholds until the closest value is found
    for threshold in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]:
        # Find the indices of the y-values that are closest to 3.05 in the range from max_x to the end
        indices = np.where((x >= max_x) & (np.abs(y - 3.05) < threshold))[0]

        # If there are no indices, continue to the next threshold
        if len(indices) == 0:
            continue

        # If there are multiple indices, take the first one
        if len(indices) > 1:
            idx = indices[0]
        else:
            idx = indices[0]

        # Use the index to get the corresponding x value
        x_at_y_3_05 = x[idx]

        # Break the loop as we found a value
        break

    return x, y, x_at_y_3_05

# distance from camera to hoop measured (cm)
Known_distance = (457.2**2 + 305**2)**(1/2)

# width of face in the real world or Object Plane (cm)
Known_width = 24.13
