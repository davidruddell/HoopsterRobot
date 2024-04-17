import time
import serial
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

# Define start and end characters
START_CHAR = '<'
END_CHAR = '>'

# Create a serial object
try:
    mySerial = serial.Serial('COM6')
    mySerial.baudrate = 9600
    mySerial.timeout = 0.01
    mySerial.bytesize = 8
    mySerial.parity = 'N'
    mySerial.stopbits = 1
except:
    print("COM Port not available")


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


def testCommands():
    # Test DRIVE command
    transmitCommandDrive(Command.DRIVE, 12345, -4269, 3, 69)
    time.sleep(1)

    # Test CHANGE_AZIMUTH command
    transmitCommand(Command.CHANGE_AZIMUTH, 0, 132.69345)
    time.sleep(1)

    # Test CHANGE_AIM command
    transmitCommand(Command.CHANGE_AIM, 0, 42.123)
    time.sleep(1)

    # Test CHANGE_MOTOR1_RPM command
    transmitCommand(Command.CHANGE_MOTOR1_RPM, 651)
    time.sleep(1)

    # Test CHANGE_MOTOR2_RPM command
    transmitCommand(Command.CHANGE_MOTOR2_RPM, 1234)
    time.sleep(1)

    # Test LAUNCH command
    transmitCommand(Command.LAUNCH)

while True:
    time.sleep(1)
    testCommands()
    # Use a non-blocking approach to read from the serial port
    if mySerial.in_waiting > 0:
        ReceivedString = mySerial.readline()
        print(ReceivedString.decode("utf-8"))
    else:
        # If there's nothing to read, yield control to allow other tasks to run
        time.sleep(1)