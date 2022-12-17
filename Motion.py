import serial
import time

class Motion:
    ser = None
    baudRate = None
    scp = None
    def __init__(self):
        self.scp = '/dev/ttyS0'
        self.baudRate = 9600
        self.ser = serial.Serial(self.scp, self.baudRate, timeout=1)

    ######################################################
    # Leg Servo Key
    # First letter: Side (R = Right, L = Left)
    # Second Letter: Leg (R = Rear, M = Middle, F = Front)
    # Third Letter: Servo (H = Hip, M = Middle, K = Knee)
    ######################################################
    ## Right Leg Definitions
    __LRH = 0
    __LRK = 1
    __LRA = 2
    __LMH = 4
    __LMK = 5
    __LMA = 6
    __LFH = 8
    __LFK = 9
    __LFA = 10
    ## Left Leg Definitions
    __RRH = 16
    __RRK = 17
    __RRA = 18
    __RMH = 20
    __RMK = 21
    __RMA = 22
    __RFH = 24
    __RFK = 25
    __RFA = 26

    ###############################################################################
    # Mandibles Servo Key
    # First letter: M = Mandibles
    # Second letter: Servo (R = Rotation, L = Left Grip, R = Right Grip, T = Tilt)
    ###############################################################################
    __MY = 12
    __MR = 13
    __MT = 14
    __MLG = 28
    __MRG = 29
    __MandibleServos = [__MY,__MR,__MT,__MLG,__MRG]

    ################################################
    # Tail Servo Key
    # First letter: T = Tail
    # Second letter: Servo (T = Tilt, R = Rotation)
    ################################################
    __TR = 30
    __TT = 31
    __TailServos = [__TR,__TT]

    # Stand Position
    __standPosition = {__LFH:1400, __LFK:1400, __LFA:1400, __LMH:1500, __LMK:1400, __LMA:1400, __LRH:1400, __LRK:1600, __LRA:1400, __RRH:1500, __RRK:1600, __RRA:1600, __RMH:1500, __RMK:1650, __RMA:1600, __RFH:1700, __RFK:1600, __RFA:1600  }
    __sitPosition = {__LFH:1500, __LFK:750, __LFA:750, __LMH:1500, __LMK:750, __LMA:750, __LRH:1500, __LRK:850, __LRA:750, __RRH:1500, __RRK:2300, __RRA:2300, __RMH:1500, __RMK:2300, __RMA:2300, __RFH:1500, __RFK:2300, __RFA:2300  }

    # Movement Positions
    __walkPositionOne = {__LFH:1100, __LFK:1000, __LFA:1400, __LMH:1900, __LMK:1700, __LMA:1400, __LRH:1200, __LRK:1000, __LRA:1200, __RRH:1100, __RRK:1600, __RRA:1700, __RMH:1500, __RMK:2000, __RMA:1600, __RFH:1500, __RFK:1600, __RFA:1600  }
    __walkPositionTwo = {__LFH:1100, __LFK:1800, __LFA:1400, __LMH:1900, __LMK:1700, __LMA:1400, __LRH:1200, __LRK:1800, __LRA:1200, __RRH:1100, __RRK:1600, __RRA:1700, __RMH:1500, __RMK:1200, __RMA:1600, __RFH:1500, __RFK:1600, __RFA:1600  }
    __walkPositionThree = {__LFH:1500, __LFK:1800, __LFA:1400, __LMH:1500, __LMK:1000, __LMA:1400, __LRH:1600, __LRK:1800, __LRA:1200, __RRH:1500, __RRK:2000, __RRA:1700, __RMH:1100, __RMK:1200, __RMA:1600, __RFH:1600, __RFK:2000, __RFA:1625  }
    __walkPositionFour = {__LFH:1500, __LFK:1800, __LFA:1400, __LMH:1500, __LMK:1800, __LMA:1400, __LRH:1600, __LRK:1800, __LRA:1200, __RRH:1500, __RRK:1200, __RRA:1700, __RMH:1100, __RMK:1200, __RMA:1600, __RFH:1600, __RFK:1200, __RFA:1625 }

    # Rotation Positions
    __rotateRightPosition = { __LFH:1800, __LRH:1800, __LMH:1800, __RMH:1800, __RRH:1800, __RFH:1800}
    __rotateLeftPosition = { __LFH:1100, __LRH:1100, __LMH:1100, __RMH:1100, __RRH:1100, __RFH:1100}
    __minimalRotateRightPosition = { __LFH:1700, __LRH:1700, __LMH:1700, __RMH:1700, __RRH:1700, __RFH:1700}
    __minimalRotateLeftPosition = { __LFH: 1400, __LRH: 1400, __LMH: 1400, __RMH: 1400, __RRH: 1400, __RFH: 1400}

    # Move Back to Center after Rotation
    __moveBackToCenterOne = { __LFK: 1000, __LFH: 1400, __RRK: 2000, __RRH: 1500}
    __moveBackToCenterTwo = { __LFK: 1400, __RRK: 1600, __LFA: 1400, __RRA: 1600}
    __moveBackToCenterThree = { __LMK: 1000, __LMH: 1500, __RMK: 2000, __RMH: 1500}
    __moveBackToCenterFour = { __LMK: 1400, __RMK: 1600, __LMA: 1400, __RMA: 1600}
    __moveBackToCenterFive = { __LRK: 1000, __LRH: 1400, __RFK: 2000, __RFH: 1700}
    __moveBackToCenterSix = { __LRK: 1400, __RFK: 1600, __LRA: 1400, __RRA: 1600}
    
    # Head Positions
    __openMandibles = {__MRG: 1300, __MLG: 1300}
    __reachDownPosition = {__MT:1900}
    __grabPosition = {__MLG: 600, __MRG: 1700}
    __liftPosition =  {__MT:1000}


    def __SetPos(self, motor, position):
        return f"#{motor} P{position} "

    def SetSinglePos(self, motor, position):
        self.ser.write(str.encode(self.__SetPos(motor, position) + "\r"))
    
    def CenterHeadAndTail(self):
        command = ""
        for servo in self.__MandibleServos:
            command += self.__SetPos(servo, 1500) + " "
        self.ser.write(str.encode(command + "\r"))

        for servo in self.__TailServos:
            command += self.__SetPos(servo, 1500) + " "
        command += self.__SetPos(self.__MT, 1500) + " "
        command += self.__SetPos(self.__MRG, 1700) + " "
        command += self.__SetPos(self.__MLG, 900) + " "
        command += self.__SetPos(self.__MY, 1500) + " "
        self.ser.write(str.encode(command + "\r"))

    def __CommandDictToPosition(self, dict, time= 200):
        command = ""
        for key in dict:
            command += self.__SetPos(key, dict[key])
        self.ser.write(str.encode(command + f"T{time}\r"))

    def __StandingPosition(self):
        self.__CommandDictToPosition(self.__standPosition, 200)

    def __MoveBackAfterRotation(self):
        self.__CommandDictToPosition(self.__moveBackToCenterOne, 50)
        time.sleep(.4)
        self.__CommandDictToPosition(self.__moveBackToCenterTwo, 50)
        time.sleep(.2)
        self.__CommandDictToPosition(self.__moveBackToCenterThree, 50)
        time.sleep(.2)
        self.__CommandDictToPosition(self.__moveBackToCenterFour, 50)
        time.sleep(.2)
        self.__CommandDictToPosition(self.__moveBackToCenterFive, 50)
        time.sleep(.2)
        self.__CommandDictToPosition(self.__moveBackToCenterSix, 50)


    def Sit(self):
        """_summary_: Moves the robot to a sitting position."""
        time.sleep(2)
        self.__CommandDictToPosition(self.__sitPosition, 200)
        time.sleep(2)

    def PickupManeuver(self, steps = 3):
        self.__CommandDictToPosition(self.__openMandibles, 200)
        for i in range(0, steps):
            self.WalkOneStep()
        self.ReachDownAndGrab()
        
    def ReachDownAndGrab(self):
        self.__CommandDictToPosition(self.__openMandibles, 200)
        time.sleep(1)
        self.__CommandDictToPosition(self.__reachDownPosition, 200)
        time.sleep(1)
        self.__CommandDictToPosition(self.__grabPosition, 200)
        time.sleep(1)
        self.__CommandDictToPosition(self.__liftPosition, 200)


    def Stand(self):
        # Move all legs towards body and then stand
        self.Sit()
        self.__StandingPosition()
        time.sleep(2)


    def LowerHead(self, extent = 1):
        extent *= 150
        self.__CommandDictToPosition({self.__MT: 1550 + extent}, 200)

    def WalkOneStep(self):
        self.__CommandDictToPosition(self.__walkPositionOne, 50)
        # time.sleep(5)
        self.__CommandDictToPosition(self.__walkPositionTwo, 50)
        # time.sleep(5)
        self.__CommandDictToPosition(self.__walkPositionThree, 50)
        # time.sleep(5)
        self.__CommandDictToPosition(self.__walkPositionFour, 50)
        # time.sleep(5)
        self.__StandingPosition()

    # Rotate the robot 19 degrees
    def RotateRightOne(self):
        self.__CommandDictToPosition(self.__rotateRightPosition, 50)
        time.sleep(.2)
        self.__MoveBackAfterRotation()
        time.sleep(.2)
        self.__CommandDictToPosition(self.__standPosition, 50)

    def RotateLeftOne(self):
        self.__CommandDictToPosition(self.__rotateLeftPosition, 50)
        # time.sleep(.1)
        self.__MoveBackAfterRotation()
        # time.sleep(.1)
        self.__CommandDictToPosition(self.__standPosition, 50)
        
    def MinimalRotateLeftOne(self):
        self.__CommandDictToPosition(self.__minimalRotateLeftPosition, 50)
        # time.sleep(.2)
        self.__MoveBackAfterRotation()
        # time.sleep(.2)
        self.__CommandDictToPosition(self.__standPosition, 50)

    def MinimalRotateRightOne(self):
        self.__CommandDictToPosition(self.__minimalRotateRightPosition, 50)
        # time.sleep(.2)
        self.__MoveBackAfterRotation()
        # time.sleep(.2)
        self.__CommandDictToPosition(self.__standPosition, 50)


def main():
    motion = Motion()
    motion.Stand()

# main()
