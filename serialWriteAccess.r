


heres how to change rpm1, rpm2, azimuth, launch angle


RPM1

data = f"{8}{' '}{RPM[0]}\n"
print(data)
ser.write(data.encode())
time.sleep(0.1)


RPM2

data = f"{9}{' '}{RPM[1]}\n"
print(data)
ser.write(data.encode())
time.sleep(0.1)


AZIMUTH

data = f"{5}{' '}{AZIMUTH}\n"
print(data)
ser.write(data.encode())
time.sleep(0.1)


LAUNCH ANGLE
theta degrees needs to become + or - value
0.005

data = f"{1}{' '}{THETA_DEGREES}\n"
print(data)
ser.write(data.encode())
time.sleep(0.1)


LAUNCH  -- prolly dont need, use rpm1 and rpm2

data = f"{2}{' '}{default_rpm}\n"
print(data)
ser.write(data.encode())
time.sleep(0.1)


BALL DELIVERY

data = f"{3}{' '}\n"
print(data)
ser.write(data.encode())
time.sleep(0.1)


CANCEL

data = f"{3}{' '}\n"
print(data)
ser.write(data.encode())
time.sleep(0.1)