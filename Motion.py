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
MLG = 28
MRG = 29

MandibleServos = [MR,MT,MLG,MRG]

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
    command += SetPos(MR, 1450) + " "
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
openMandibles = {MRG: 1500, MLG: 1500}
reachDownPosition = {MT:1900}
grabPosition = {MLG: 600, MRG: 1700}
liftPosition =  {MT:1000}

def PickupManeuver(ser):
    for i in range(0, 10):
        WalkOneStep(ser)
    ReachDownAndGrab(ser)
    
def ReachDownAndGrab(ser):
    CommandDictToPosition(ser, openMandibles, 200)
    time.sleep(1)
    CommandDictToPosition(ser, reachDownPosition, 200)
    time.sleep(1)
    CommandDictToPosition(ser, grabPosition, 200)
    time.sleep(1)
    CommandDictToPosition(ser, liftPosition, 200)


def Stand(ser):
    # Move all legs towards body and then stand
    Sit(ser)
    StandingPosition(ser)
    # time.sleep(2)
    # ControlBothSides(ser, leftAnkles, rightAnkles, 1600)    
    # ControlBothSides(ser, leftKnees, rightKnees, 1600) 
    time.sleep(2)


# Move the right leg farther forward on the step to counteract right movement
walkPositionOne = {LFH:1000, LFK:1000, LFA:1400, LMH:1900, LMK:1700, LMA:1400, LRH:1200, LRK:1000, LRA:1200, RRH:1100, RRK:1600, RRA:1700, RMH:1500, RMK:2000, RMA:1600, RFH:1400, RFK:1600, RFA:1600  }
walkPositionTwo = {LFH:1000, LFK:1800, LFA:1400, LMH:1900, LMK:1700, LMA:1400, LRH:1200, LRK:1800, LRA:1200, RRH:1100, RRK:1600, RRA:1700, RMH:1500, RMK:1200, RMA:1600, RFH:1400, RFK:1600, RFA:1600  }
walkPositionThree = {LFH:1500, LFK:1800, LFA:1400, LMH:1500, LMK:1000, LMA:1400, LRH:1600, LRK:1800, LRA:1200, RRH:1500, RRK:2000, RRA:1700, RMH:1100, RMK:1200, RMA:1600, RFH:1700, RFK:2000, RFA:1600  }
walkPositionFour = {LFH:1500, LFK:1800, LFA:1400, LMH:1500, LMK:1800, LMA:1400, LRH:1600, LRK:1800, LRA:1200, RRH:1500, RRK:1200, RRA:1700, RMH:1100, RMK:1200, RMA:1600, RFH:1700, RFK:1200, RFA:1600  }

rotateRightPosition = { LFH:1800, LRH:1800, LMH:1800, RMH:1800, RRH:1800, RFH:1800}
rotateLeftPosition = { LFH:1100, LRH:1100, LMH:1100, RMH:1100, RRH:1100, RFH:1100}
minimalRotateRightPosition = { LFH:1600, LRH:1600, LMH:1600, RMH:1600, RRH:1600, RFH:1600}
minimalRotateLeftPosition = { LFH: 1400, LRH: 1400, LMH: 1400, RMH: 1400, RRH: 1400, RFH: 1400}

standPosition = {LFH:1400, LFK:1400, LFA:1400, LMH:1500, LMK:1400, LMA:1400, LRH:1400, LRK:1600, LRA:1400, RRH:1500, RRK:1600, RRA:1600, RMH:1500, RMK:1650, RMA:1600, RFH:1700, RFK:1600, RFA:1600  }


moveBackToCenterOne = { LFK: 1000, LFH: 1400, RRK: 2000, RRH: 1500}
moveBackToCenterTwo = { LFK: 1400, RRK: 1600}
moveBackToCenterThree = { LMK: 1000, LMH: 1500, RMK: 2000, RMH: 1500}
moveBackToCenterFour = { LMK: 1400, RMK: 1600}
moveBackToCenterFive = { LRK: 1000, LRH: 1400, RFK: 2000, RFH: 1700}
moveBackToCenterSix = { LRK: 1400, RFK: 1600}



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
    CommandDictToPosition(ser, standPosition, 200)

def SittingPosition(ser):
    time.sleep(2)
    CommandDictToPosition(ser, sitPosition, 200)


def WalkOneStep(ser):
    CommandDictToPosition(ser, walkPositionOne, 50)
    CommandDictToPosition(ser, walkPositionTwo, 50)
    # StandingPosition(ser)
    CommandDictToPosition(ser, walkPositionThree, 50)
    CommandDictToPosition(ser, walkPositionFour, 50)
    StandingPosition(ser)

# Rotate the robot 19 degrees
def RotateRightOne(ser):
    CommandDictToPosition(ser, rotateRightPosition, 50)
    time.sleep(.2)
    MoveBackAfterRotation(ser)
    time.sleep(.2)
    CommandDictToPosition(ser, standPosition, 50)

def RotateLeftOne(ser):
    CommandDictToPosition(ser, rotateLeftPosition, 50)
    time.sleep(.2)
    MoveBackAfterRotation(ser)
    time.sleep(.2)
    CommandDictToPosition(ser, standPosition, 50)

def MoveBackAfterRotation(ser):
    CommandDictToPosition(ser, moveBackToCenterOne, 50)
    time.sleep(.5)
    CommandDictToPosition(ser, moveBackToCenterTwo, 50)
    time.sleep(.5)
    CommandDictToPosition(ser, moveBackToCenterThree, 50)
    time.sleep(.5)
    CommandDictToPosition(ser, moveBackToCenterFour, 50)
    time.sleep(.5)
    CommandDictToPosition(ser, moveBackToCenterFive, 50)
    time.sleep(.5)
    CommandDictToPosition(ser, moveBackToCenterSix, 50)
    


def MinimalRotateLeftOne(ser):
    CommandDictToPosition(ser, minimalRotateLeftPositionOne, 50)
    CommandDictToPosition(ser, minimalRotateLeftPositionTwo, 50)
    CommandDictToPosition(ser, minimalRotateLeftPositionThree, 50)
    CommandDictToPosition(ser, minimalRotateLeftPositionFour, 50)
    CommandDictToPosition(ser, minimalRotateLeftPositionFive, 50)
    CommandDictToPosition(ser, standPosition, 50)

def MinimalRotateRightOne(ser):
    CommandDictToPosition(ser, minimalRotateRightPositionOne, 50)
    CommandDictToPosition(ser, minimalRotateRightPositionTwo, 50)
    CommandDictToPosition(ser, minimalRotateRightPositionThree, 50)
    CommandDictToPosition(ser, minimalRotateRightPositionFour, 50)
    CommandDictToPosition(ser, minimalRotateRightPositionFive, 50)
    CommandDictToPosition(ser, standPosition, 50)

# def Rotate(ser):
    


def main():
    ser = serial.Serial(scp, baudRate)
    # CenterHeadAndTail(ser)
    # Stand(ser)

    # MoveSingleMotor(ser, LRK, 1000)
    RotateLeftOne(ser)
    RotateRightOne(ser)
    # ReachDownAndGrab(ser)
    # Sit(ser)
    # Stand(ser)

    # CenterHeadAndTail(ser)

    # MoveSingleMotor(ser, RMK, 1800)    
    # for i in range(0, 10):
    #     MinimalRotateLeftOne(ser)
    # for i in range(0, 14):
    #     RotateRightOne(ser)

    # for i in range(0, 3):
    #     RotateLeftOne(ser)

    # for i in range(0, 30):
    #     WalkOneStep(ser)
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
