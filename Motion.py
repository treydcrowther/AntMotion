import serial

######################################################
# Leg Servo Key
# First letter: Side (R = Right, L = Left)
# Second Letter: Leg (R = Rear, M = Middle, F = Front)
# Third Letter: Servo (H = Hip, M = Middle, K = Knee)
######################################################

## Right Leg Definitions
RRH = 0
RRM = 1
RRK = 2
RMH = 4
RMM = 5
RMK = 6
RFH = 8
RFM = 9
RFK = 10
## Left Leg Definitions
LRH = 16
LRM = 17
LRK = 18
LMH = 20
LMM = 21
LMK = 22
LFH = 24
LFM = 25
LFK = 26

###############################################################################
# Mandibles Servo Key
# First letter: M = Mandibles
# Second letter: Servo (R = Rotation, L = Left Grip, R = Right Grip, T = Tilt)
###############################################################################
MR = 11
ML = 12
MR = 13
MT = 14

################################################
# Tail Servo Key
# First letter: T = Tail
# Second letter: Servo (T = Tilt, R = Rotation)
################################################
TT = 27
TR = 28

# Serial Command Port
scp = '/dev/ttyS0'
baudRate = 9600


def SetPos(motor, position):
    return f"#{motor} P{position}"

def AllCentered(ser):
    command = ""
    for i in range(32):
        command += SetPos(i, 1500) + " "
    ser.write(str.encode(command + "\r"))

def Stand(ser):
    # Move all legs towards body and then stand
    x = 0


def main():
    ser = serial.Serial(scp, baudRate)
    AllCentered(ser)


main()