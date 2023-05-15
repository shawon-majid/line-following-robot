import sys, os
desiredPath = "C:/Users/SHAWON/Downloads/Assignment/CoppeliaScripts" # set this path to your working folder
os.chdir(desiredPath)
print("Current working directory: {}".format(os.getcwd()))   # sanity checktry:

try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time

class LineTracerRobot:

    def __init__(self, sim, clientID):
        self._sim = sim
        self.clientID = clientID
        errCode = [0] * 5
        ## attach actuators and sensors
        errCode[0], self.leftMotor = sim.simxGetObjectHandle(clientID, "DynamicLeftJoint", sim.simx_opmode_oneshot_wait )
        errCode[1], self.rightMotor = sim.simxGetObjectHandle(clientID, "DynamicRightJoint", sim.simx_opmode_oneshot_wait )

        ## attach sensors 
        errCode[2], self.leftSensor = sim.simxGetObjectHandle(clientID, "LeftSensor", sim.simx_opmode_oneshot_wait )
        errCode[3], self.midSensor = sim.simxGetObjectHandle(clientID, "MiddleSensor", sim.simx_opmode_oneshot_wait )
        errCode[4], self.rightSensor = sim.simxGetObjectHandle(clientID, "RightSensor", sim.simx_opmode_oneshot_wait )

    def _set_two_motor(self, left: float, right: float):
        ## set the left motor to the to the value in left
        errCode = sim.simxSetJointTargetVelocity(self.clientID , self.leftMotor, left, sim.simx_opmode_streaming ) 
        ## the right motor to the value in right
        errCode = sim.simxSetJointTargetVelocity(self.clientID , self.rightMotor, right, sim.simx_opmode_streaming ) 

    def right_sensor(self):
        ## return the value from the rigth sensor
        return self._sim.simxReadVisionSensor(self.clientID, self.rightSensor, self._sim.simx_opmode_oneshot_wait)[1]

    def mid_sensor(self):
        ## return the value from the middle sensor
        return self._sim.simxReadVisionSensor(self.clientID,self.midSensor,self._sim.simx_opmode_oneshot_wait)[1]

    def left_sensor(self):
        ## return the value from the left sensor
        return self._sim.simxReadVisionSensor(self.clientID, self.leftSensor,self._sim.simx_opmode_oneshot_wait)[1]

        
    def rotate_right(self, speed=2.0):
        ## turn the robot right
        self._set_two_motor(speed, -speed)

    def rotate_left(self, speed=2.0):
        ## turn the robot left
        self._set_two_motor(-speed, speed)

    def move_forward(self, speed=2.0):
        ## move the robot forward
        self._set_two_motor(speed, speed)


    def move_backward(self, speed=2.0):
        ## move the robot backwards
        self._set_two_motor(-speed, -speed)

    def stop(self):
        self._set_two_motor(0.0, 0.0)



print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections

clientID=sim.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to CoppeliaSim

if clientID != -1:
    print ('Connected to remote API server')
else:
    print('Connection failed!!')
    sys.exit('Could not connect')

# This is just to ensure that the loop will end after 
# a fixed time. 
TimeOutLimit = 60 

## Create the robot object
bot = LineTracerRobot(sim, clientID)

startTime=time.time()

while time.time()-startTime < TimeOutLimit:
    ## Read the sensors:
    sensorReading = [bot.left_sensor(),bot.mid_sensor(),bot.right_sensor()]
    print(sensorReading)  ## display the sensor data


    if sensorReading[1] == False and sensorReading[0] == False and sensorReading[2] == False:
        bot.move_forward(1)
    elif sensorReading[2] == False and sensorReading[1] == False and sensorReading[0] == True:
        bot.rotate_right(0.2)
    
    elif sensorReading[2] == False and sensorReading[1] == True and sensorReading[0] == True:
        bot.rotate_right(0.5)
    
    elif sensorReading[0] == False and sensorReading[1] == False and sensorReading[2] == True:
        bot.rotate_left(0.2)
    elif sensorReading[0] == False and sensorReading[1] == True and sensorReading[2] == True:
        bot.rotate_left(0.5)
    else:
        bot.move_forward(1)
        
    time.sleep(0.2) ## wait

## Stop the robot
bot.stop()
time.sleep(0.5)    ## delay to execute the command
sim.simxFinish(-1) ## just in case, close all opened connections
print("...done")