import serial
import time

######################################################
# Leg Servo Key
# First letter: Side (R = Right, L = Left)
# Second Letter: Leg (R = Rear, M = Middle, F = Front)
# Third Letter: Servo (H = Hip, M = Middle, K = Knee)
######################################################

## Right Leg Definitions
LRH = 0
LRK = 1
LRA = 2
LMH = 4
LMK = 5
LMA = 6
LFH = 8
LFK = 9
LFA = 10


## Left Leg Definitions
RRH = 16
RRK = 17
RRA = 18
RMH = 20
RMK = 21
RMA = 22
RFH = 24
RFK = 25
RFA = 26

leftAnkles = [LRA, LMA, LFA]
rightAnkles = [RRA, RMA, RFA]

leftHips = [LRH, LMH, LFH]
rightHips = [RFH, RMH, RRH]

leftKnees = [LRK, LMK, LFK]
rightKnees = [RFK, RMK, RRK]

frontHips = [[RFH], [LFH]]
middleHips = [[RMH], [LMH]]
backHips = [[RRH], [LRH]]

# [0] = hips [1] = knees [2] = ankles
# [][0] = leftside [][1] = rightside
leftWalkMotors = [[[LFH, LRH], [RMH]], [[LFK, LRK] , [RMK]], [[LFA, LRA],  [RMA]]]
rightWalkMotors = [[[LMH], [RFH, RRH]], [[LMK], [RFK, RRK]], [[LMA], [RFA, RRA]]]


###############################################################################
# Mandibles Servo Key
# First letter: M = Mandibles
# Second letter: Servo (R = Rotation, L = Left Grip, R = Right Grip, T = Tilt)
###############################################################################
MY = 12
MR = 13
MT = 14
ML = 28
MR = 29

MandibleServos = [MY,MR,MT,ML,MR]

################################################
# Tail Servo Key
# First letter: T = Tail
# Second letter: Servo (T = Tilt, R = Rotation)
################################################
TR = 30
TT = 31

TailServos = [TR,TT]

# Serial Command Port
scp = '/dev/ttyS0'
baudRate = 9600



def SetPos(motor, position):
    return f"#{motor} P{position} "

def MoveSingleMotor(ser, motor, position):
    ser.write(str.encode(SetPos(motor, position) + "T200\r"))

def AllCentered(ser):
    command = ""
    for i in range(32):
        command += SetPos(i, 1500)
    ser.write(str.encode(command + "\r"))

def CenterHeadAndTail(ser):
    command = ""

    for servo in MandibleServos:
        command += SetPos(servo, 1500) + " "
    ser.write(str.encode(command + "\r"))

    for servo in TailServos:
        command += SetPos(servo, 1500) + " "
    ser.write(str.encode(command + "\r"))


def ComputeRightPosition(position):
    if(position > 1500):
        adjustedPosition = 1500 - (position - 1500)
    else:
        adjustedPosition = 1500 + (1500 - position)
    return adjustedPosition

def SetAnklePosition(ser):
    command = ""
    for ankle in leftAnkles:
        command += SetPos(ankle,700)
    for ankle in rightAnkles:
        command += SetPos(ankle,2300)    
    ser.write(str.encode(command + "T200\r"))


def ControlBothSides(ser, leftArray, rightArray, position):
    CommandArrayToPosition(ser, leftArray, position)
    CommandArrayToPosition(ser, rightArray, ComputeRightPosition(position))

def CommandArrayToPosition(ser, array, position):
    command = ""
    for servo in array:
        command += SetPos(servo, position)
    ser.write(str.encode(command + "T1000\r"))   

def CommandDictToPosition(ser, dict, time= 200):
    command = ""
    for key in dict:
        command += SetPos(key, dict[key])
    ser.write(str.encode(command + f"T{time}\r"))

def Sit(ser):
    SittingPosition(ser)
    time.sleep(2)


standPosition = {LFH:1400, LFK:1400, LFA:1400, LMH:1500, LMK:1400, LMA:1400, LRH:1400, LRK:1600, LRA:1400, RRH:1500, RRK:1600, RRA:1600, RMH:1500, RMK:1650, RMA:1600, RFH:1700, RFK:1600, RFA:1600  }
sitPosition = {LFH:1500, LFK:750, LFA:750, LMH:1500, LMK:750, LMA:750, LRH:1500, LRK:850, LRA:750, RRH:1500, RRK:2300, RRA:2300, RMH:1500, RMK:2300, RMA:2300, RFH:1500, RFK:2300, RFA:2300  }

def Stand(ser):
    # Move all legs towards body and then stand
    Sit(ser)
    StandingPosition(ser)
    # time.sleep(2)
    # ControlBothSides(ser, leftAnkles, rightAnkles, 1600)    
    # ControlBothSides(ser, leftKnees, rightKnees, 1600) 
    time.sleep(2)


# Move the right leg farther forward on the step to counteract right movement
walkPositionOne = {LFH:1300, LFK:1000, LFA:1400, LMH:1700, LMK:1700, LMA:1400, LRH:1300, LRK:1000, LRA:1400, RRH:1300, RRK:1600, RRA:1600, RMH:1700, RMK:2000, RMA:1600, RFH:1300, RFK:1600, RFA:1600  }
walkPositionTwo = {LFH:1300, LFK:1800, LFA:1400, LMH:1700, LMK:1700, LMA:1400, LRH:1300, LRK:1800, LRA:1400, RRH:1300, RRK:1600, RRA:1600, RMH:1700, RMK:1200, RMA:1600, RFH:1300, RFK:1600, RFA:1600  }
walkPositionThree = {LFH:1700, LFK:1800, LFA:1400, LMH:1300, LMK:1000, LMA:1400, LRH:1700, LRK:1800, LRA:1400, RRH:1700, RRK:2000, RRA:1600, RMH:1300, RMK:1200, RMA:1600, RFH:1700, RFK:2000, RFA:1600  }
walkPositionFour = {LFH:1700, LFK:1800, LFA:1400, LMH:1300, LMK:1800, LMA:1400, LRH:1700, LRK:1800, LRA:1400, RRH:1700, RRK:1200, RRA:1600, RMH:1300, RMK:1200, RMA:1600, RFH:1700, RFK:1200, RFA:1600  }

def CommandThreeLeg(ser, left):
    if(left):
        moveLegs = leftWalkMotors
        liftLegs = rightWalkMotors
    else:
        liftLegs = leftWalkMotors
        moveLegs  = rightWalkMotors
    
    # Lift knees and rotate hip
    ControlBothSides(ser, moveLegs[0][0], moveLegs[0][1], 1300)
    ControlBothSides(ser, moveLegs[1][0], moveLegs[1][1], 1000)
    ControlBothSides(ser, liftLegs[0][0], liftLegs[0][1], 1700)
    time.sleep(1)
    # Replace leg on ground
    ControlBothSides(ser, moveLegs[1][0], moveLegs[1][1], 1800)
    # time.sleep(1)
    # ControlBothSides(ser, moveLegs[0][0], moveLegs[0][1], 1700)
    # ControlBothSides(ser, liftLegs[1][0], liftLegs[1][1], 1300)

def StandingPosition(ser):
    time.sleep(2)
    CommandDictToPosition(ser, standPosition, 200)

def SittingPosition(ser):
    time.sleep(2)
    CommandDictToPosition(ser, sitPosition, 200)

def WalkOneStep(ser):
    CommandDictToPosition(ser, walkPositionOne, 200)
    CommandDictToPosition(ser, walkPositionTwo, 200)
    CommandDictToPosition(ser, walkPositionThree, 200)
    CommandDictToPosition(ser, walkPositionFour, 200)


def main():
    ser = serial.Serial(scp, baudRate)
    Sit(ser)
    Stand(ser)

    for i in range(0, 3):
        WalkOneStep(ser)
    # CommandThreeLeg(ser, True)
    # CommandThreeLeg(ser, False)
    # CommandThreeLeg(ser, True)
    # StandingPosition(ser)
    # for i in range(100):
    #     CommandThreeLeg(ser, False)
    #     CommandThreeLeg(ser, True)
    #     CommandThreeLeg(ser, False)
    #     CommandThreeLeg(ser, True)
    #     CommandThreeLeg(ser, False)
    #     CommandThreeLeg(ser, True)
    #     CommandThreeLeg(ser, False)
    #     CommandThreeLeg(ser, True)
    #     CommandThreeLeg(ser, False)
    # StandingPosition(ser)
    # CommandThreeLeg(ser, True)
    # CommandThreeLeg(ser, False)
    # StandingPosition(ser)
    # CommandThreeLeg(ser, True)
    # CommandThreeLeg(ser, False)
    # StandingPosition(ser)
    #MoveSingleMotor(ser, LFK, 1400)
    #MoveSingleMotor(ser, RFK , 1500)
    #MoveSingleMotor(ser, RFH, 1550)
    #MoveSingleMotor(ser, LFH, 1450)
    #MoveSingleMotor(ser, LFA, 1350)
    #MoveSingleMotor(ser, RFA, 1650)
    #MoveSingleMotor(ser, RMK, 1350)
    #MoveSingleMotor(ser, LMK, 1300)
    #MoveSingleMotor(ser, RRK, 1700)
    #MoveSingleMotor(ser, RMH, 1500)

main()
